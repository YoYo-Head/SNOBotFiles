import os

import requests

import config as cng


USERNAME_LOOKUP_URL = "https://users.roblox.com/v1/usernames/users"
USER_GROUP_ROLES_URL = "https://groups.roblox.com/v2/users/{user_id}/groups/roles"


class RobloxAPIError(Exception):
    pass


def _resolve_user(username: str) -> tuple[str, int]:
    try:
        lookup_response = requests.post(
            USERNAME_LOOKUP_URL,
            json={"usernames": [username], "excludeBannedUsers": True},
            timeout=15,
        )
        lookup_response.raise_for_status()
        lookup_data = lookup_response.json()
    except requests.RequestException as exc:
        raise RobloxAPIError(f"Roblox username lookup failed: {exc}") from exc
    except ValueError as exc:
        raise RobloxAPIError("Roblox returned an invalid username lookup response.") from exc

    if not isinstance(lookup_data, dict):
        raise RobloxAPIError("Roblox returned an invalid username lookup response.")
    users = lookup_data.get("data", [])
    if not users:
        raise RobloxAPIError(f"Roblox username '{username}' was not found.")
    if not isinstance(users[0], dict):
        raise RobloxAPIError("Roblox returned an invalid username lookup response.")

    user_id = users[0].get("id")
    canonical_username = users[0].get("name")
    if not isinstance(user_id, int) or not isinstance(canonical_username, str):
        raise RobloxAPIError("Roblox returned invalid user information.")
    return canonical_username, user_id


def get_group_rank(username: str) -> tuple[str, str, int]:
    canonical_username, user_id = _resolve_user(username)
    try:
        response = requests.get(
            USER_GROUP_ROLES_URL.format(user_id=user_id),
            timeout=15,
        )
        response.raise_for_status()
        group_data = response.json()
    except requests.RequestException as exc:
        raise RobloxAPIError(f"Roblox group lookup failed: {exc}") from exc
    except ValueError as exc:
        raise RobloxAPIError("Roblox returned an invalid group lookup response.") from exc

    if not isinstance(group_data, dict) or not isinstance(group_data.get("data"), list):
        raise RobloxAPIError("Roblox returned an invalid group lookup response.")

    for membership in group_data["data"]:
        if not isinstance(membership, dict):
            continue
        group = membership.get("group")
        role = membership.get("role")
        if not isinstance(group, dict) or group.get("id") != cng.Roblox_Group_ID:
            continue
        if not isinstance(role, dict) or not isinstance(role.get("id"), int):
            raise RobloxAPIError("Roblox returned an invalid group role.")
        rank_name = cng.Roblox_Role_Rank_Names.get(role["id"])
        if rank_name is None:
            raise RobloxAPIError(
                f"{canonical_username} has a Roblox group rank that is not configured for XP."
            )
        return canonical_username, rank_name, user_id

    raise RobloxAPIError(f"{canonical_username} is not a member of the configured Roblox group.")


def assign_user_role(user_id: int, rank_name: str) -> tuple[bool, str]:
    api_key = os.getenv("RBLX_API_KEY")
    if not api_key:
        return False, "RBLX_API_KEY is not configured."

    role_id = cng.Roblox_Rank_Role_IDs.get(rank_name)
    if role_id is None:
        return False, f"No Roblox role is configured for {rank_name}."

    try:
        assignment_response = requests.post(
            cng.get_ADD_ROLE_RBLX_API_URL(cng.Roblox_Group_ID, user_id),
            headers={"x-api-key": api_key},
            json={
                "role": f"groups/{cng.Roblox_Group_ID}/roles/{role_id}",
            },
            timeout=15,
        )
        assignment_response.raise_for_status()
    except requests.RequestException as exc:
        return False, f"Roblox API request failed: {exc}"
    except ValueError:
        return False, "Roblox returned an invalid response."

    return True, f"Roblox role set to {rank_name}."


def promote_user(username: str, rank_name: str) -> tuple[bool, str]:
    try:
        _, user_id = _resolve_user(username)
    except RobloxAPIError as exc:
        return False, str(exc)
    return assign_user_role(user_id, rank_name)
