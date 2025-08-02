# FastMCP Python Server

This directory contains a simple MCP server implemented with the
[fastmcp](https://pypi.org/project/fastmcp/) library.  It mirrors the
functionality of the TypeScript server in `src/server.ts` and exposes:

* **Resources**
  * `users://all` – returns the list of all users.
  * `users://{userId}/profile` – returns details for a single user.
* **Tools**
  * `create-user` – stores a user in the JSON database.
  * `create-random-user` – generates fake user data using `faker` and stores it.
* **Prompts**
  * `generate-fake-user` – generates a prompt to create a fake user for a given name.

The server reads and writes from the existing JSON data file located at
`src/data/users.json`.

## Running

```bash
pip install -r requirements.txt
python server.py
```
