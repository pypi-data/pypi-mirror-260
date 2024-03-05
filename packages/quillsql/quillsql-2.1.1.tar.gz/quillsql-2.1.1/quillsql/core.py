import os
from dotenv import load_dotenv

import requests
import redis


from quillsql.db.cached_connection import CachedConnection
from quillsql.db.db_helper import get_db_credentials, get_schema_column_info_by_db, get_schema_tables_by_db
from quillsql.utils.schema_conversion import convert_type_to_postgres
from quillsql.utils.run_query_processes import (
    array_to_map,
    remove_fields,
)

load_dotenv()

ENV = os.getenv("PYTHON_ENV")
DEV_HOST = "http://localhost:8080"
PROD_HOST = "https://quill-344421.uc.r.appspot.com"
HOST = DEV_HOST if ENV == "development" else PROD_HOST


## Quill - Fullstack API Platform for Dashboards and Reporting.
class Quill:
    def __init__(
        self,
        private_key,
        database_type,
        database_connection_string=None,
        database_config=None,
        metadataServerURL=None,
        cache=None,
    ):
        # Handles both dsn-style connection strings (eg. "dbname=test password=secret" )
        # as well as url-style connection strings (eg. "postgres://foo@db.com")
        self.baseUrl = metadataServerURL if metadataServerURL != None else HOST
        if database_connection_string != None:
          self.target_connection = CachedConnection(database_type, get_db_credentials(database_type, database_connection_string), cache, True)
        else:
          self.target_connection = CachedConnection(database_type, database_config, cache, False)
        self.private_key = private_key

    def get_cache(self, cache_config):
        cache_type = cache_config and cache_config.get("cache_type")
        if cache_type and cache_type == "redis" or cache_type == "rediss":
            return redis.Redis(
                host=cache_config.get("host", "localhost"),
                port=cache_config.get("port", 6379),
                username=cache_config.get("username", "default"),
                password=cache_config.get("password"),
            )
        return None

    def query(self, org_id, data):
        metadata = data.get("metadata")
        if not metadata:
            return {"error": "400", "errorMessage": "Missing metadata."}

        task = metadata.get("task")
        if not task:
            return {"error": "400", "errorMessage": "Missing task."}

        try:
            pre_query_results = self.run_queries(
                metadata.get("preQueries"),
                self.target_connection.database_type,
                metadata.get('databaseType'),
                metadata,
                metadata.get("runQueryConfig"),
            )  # used by the view task to get non-sensitive data
            if metadata.get("runQueryConfig") and metadata.get("runQueryConfig").get('overridePost'):
                return {
                    "data": pre_query_results ,
                    "status": "success"
                }
            view_query = None
            if (metadata.get("preQueries")):
                view_query = metadata.get("preQueries")[0]
            payload = {
                **metadata,
                "orgId": org_id,
                "preQueryResults": pre_query_results,
                "viewQuery": view_query
            }
            quill_results = self.post_quill(metadata.get("task"), payload)
            if quill_results.get("error"):
                return {"error": quill_results.get("error"), "status": "error"}
            # If there is no metedata in the quill results, create one
            if not quill_results.get("metadata"):
                quill_results["metadata"] = {}
            metadata = quill_results.get("metadata")
            final_query_results = self.run_queries(
                quill_results.get("queries"),  self.target_connection.database_type, metadata.get('databaseType'), metadata, metadata.get("runQueryConfig")
            )
            # Quick hack to make the sdk work with the Frontend
            if len(final_query_results.get("queryResults")) == 1:
                query_result = final_query_results.get("queryResults")[0]
                quill_results["metadata"]["rows"] = query_result.get("rows")
                quill_results["metadata"]["fields"] = query_result.get("fields")
            return {
                "data": quill_results.get("metadata"),
                "queries": final_query_results,
                "status": "success",
            }

        except Exception as err:
            return {"error": str(err), "status": "error"}

    def run_queries(self, queries, pkDatabaseType, databaseType, metadata=None, runQueryConfig=None):
        results = {}
        if not queries:
            return {"queryResults": []}
        if databaseType and databaseType.lower() != pkDatabaseType.lower():
            return {"dbMismatched": True, "backendDatbaseType": pkDatabaseType}
        if runQueryConfig and runQueryConfig.get("arrayToMap"):
            array_to_map(
                queries, runQueryConfig.get("arrayToMap"), metadata, self.target_connection
            )
            return {"queryResults": []}
        elif runQueryConfig and runQueryConfig.get("getColumns"):
            query_results = self.target_connection.query(queries[0].strip().rstrip(";") + ' limit 1')
            results["columns"] = [{'name': result['name'], 'dataTypeID': convert_type_to_postgres(result['dataTypeID'])} for result in query_results['fields']]
        elif runQueryConfig and runQueryConfig.get("getTables"):
            tables = get_schema_tables_by_db(
              self.target_connection.database_type,
              self.target_connection.connection,
              runQueryConfig['schemaNames']
            )
            schema = get_schema_column_info_by_db(
              self.target_connection.database_type,
              self.target_connection.connection,
              runQueryConfig['schemaNames'],
              tables
            )
            results["queryResults"] = schema
        else:
            if runQueryConfig and runQueryConfig.get("limitThousand"):
                queries = [query.strip().rstrip(";") + " limit 1000" for query in queries]
            elif runQueryConfig and runQueryConfig.get("limitBy"):
                queries = [query.strip().rstrip(";") + " limit " + runQueryConfig.get("limitBy") for query in queries]
            query_results = [self.target_connection.query(query) for query in queries]
            results["queryResults"] = query_results
            if runQueryConfig and runQueryConfig.get("removeFields"):
                results["queryResults"] = remove_fields(
                    query_results, runQueryConfig.get("removeFields")
                )
            if runQueryConfig and runQueryConfig.get("convertDatatypes"):
                for query_result in results["queryResults"]:
                    query_result["fields"] = [
                        {
                            "name": field["name"],
                            "displayName": field["name"],
                            "field": field["name"],
                            "isVisible": True,
                            "dataTypeID": field["dataTypeID"],
                            "fieldType": convert_type_to_postgres(field["dataTypeID"]),
                        }
                        for field in query_result["fields"]
                    ]

        return results

    def post_quill(self, path, payload):
        url = f"{self.baseUrl}/sdk/{path}"
        headers = {"Authorization": f"Bearer {self.private_key}"}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
