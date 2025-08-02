from __future__ import annotations

import json
from pathlib import Path

from faker import Faker
# The fastmcp package provides a quick way to build MCP servers in Python.
# It is not installed in this environment, but this server demonstrates how it
# would be used.
from fastmcp import FastMCP, StdioServerTransport

DATA_FILE = Path(__file__).resolve().parent.parent / "src" / "data" / "users.json"

mcp = FastMCP(name="test-video", version="1.0.0")


def _read_users() -> list[dict]:
    return json.loads(DATA_FILE.read_text())


def _write_users(users: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(users, indent=2))


@mcp.resource(
    "users",
    "users://all",
    description="Get all users data from the database",
    mime_type="application/json",
)
async def get_users() -> dict:
    users = _read_users()
    return {
        "contents": [
            {
                "uri": "users://all",
                "text": json.dumps(users),
                "mimeType": "application/json",
            }
        ]
    }


@mcp.resource(
    "user-details",
    "users://{userId}/profile",
    description="Get a user's details from the database",
    mime_type="application/json",
)
async def get_user_details(userId: str) -> dict:
    users = _read_users()
    user = next((u for u in users if u.get("id") == int(userId)), None)
    payload = user if user is not None else {"error": "User not found"}
    return {
        "contents": [
            {
                "uri": f"users://{userId}/profile",
                "text": json.dumps(payload),
                "mimeType": "application/json",
            }
        ]
    }


@mcp.tool(
    "create-user",
    "Create a new user in the database",
    name=str,
    email=str,
    address=str,
    phone=str,
)
async def create_user(name: str, email: str, address: str, phone: str) -> dict:
    users = _read_users()
    new_id = len(users) + 1
    users.append({"id": new_id, "name": name, "email": email, "address": address, "phone": phone})
    _write_users(users)
    return {"content": [{"type": "text", "text": f"User {new_id} created successfully"}]}


fake = Faker()


@mcp.tool(
    "create-random-user",
    "Create a random user with fake data",
)
async def create_random_user() -> dict:
    fake_user = {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address().replace("\n", ", "),
        "phone": fake.phone_number(),
    }
    users = _read_users()
    new_id = len(users) + 1
    users.append({"id": new_id, **fake_user})
    _write_users(users)
    return {"content": [{"type": "text", "text": f"User {new_id} created successfully"}]}


@mcp.prompt(
    "generate-fake-user",
    "Generate a fake user based on a given name",
    name=str,
)
async def generate_fake_user(name: str) -> dict:
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": (
                        f"Generate a fake user with the name {name}. "
                        "The user should have a realistic email, address, and phone number."
                    ),
                },
            }
        ]
    }


def main() -> None:
    transport = StdioServerTransport()
    mcp.run(transport)


if __name__ == "__main__":  # pragma: no cover
    main()
