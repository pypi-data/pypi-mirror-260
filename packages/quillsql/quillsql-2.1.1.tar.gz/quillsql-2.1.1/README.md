# Quill Python SDK

## Quickstart

First, install the quillsql package by running:

```bash
$ pip install quillsql
```

Then, add a `/quill` endpoint to your existing python server. For example, if
you were running a FASTAPI app, you would just add the endpoint like this:

```python
from quillsql import Quill
from fastapi import FastAPI, Request

app = FastAPI()

quill = Quill(
    private_key=<YOUR_PRIVATE_KEY_HERE>,
    database_connection_string=<YOUR_DB_CONNECTION_STRING_HERE>,
)

# ... your existing endpoints here ...

@app.post("/quill")
async def quill_post(data: Request):
    body = await data.json()
    return quill.query(org_id="2", data=body)
```

Then you can run your app like normally. Pass in this route to our react library
on the frontend and you all set!

## For local testing (dev purposes only)

```
pipenv install
pipenv shell
uvicorn examples.fastapi-server.app:app --reload --port 3000
```

You are now ready to ping your local server at http://localhost:3000.

## Troubleshooting

If you run into issues with `Library not loaded: @rpath/libpq.5.dylib` or `no LC_RPATH's found`, try uninstalling and reinstalling postgres on your machine. For example, using homebrew:

```bash
$ brew uninstall c
$ brew update
$ brew install postgresql
```

If you're still having this issue, this resource might also be useful for you: https://www.psycopg.org/docs/install.html.
