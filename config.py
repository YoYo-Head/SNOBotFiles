# Channel ID for the promotions channel when a personal needs to get promoted
Promotions_Channel = 1273488646967791646

# The main officers you trust most role ID in the division
Main_Leaders_ID = 1273659380214005762

# The high commanding officer role ID in the division
High_Commanding_Officer_ID = 1273649427688591510

# The officer / high ranking officers role ID in your division
High_Rank_Officer_ID = 1273649427688591510

# My discord ID :D
MyID = 1121379165195747328

# Roblox group and role IDs for SEA Scuba Operations.
Roblox_Group_ID = 15118555
Roblox_Rank_Role_IDs = {
    "[OR-1] Initiative": 107292141,
    "[OR-2] Junior Operative": 107292160,
    "[OR-3] Operative": 107318767,
    "[OR-4] Senior Operative": 107294561,
    "[OR-5] Scuba Diver": 107424416,
    "[OR-6] Open Water Diver": 107508280,
    "[OR-7] Advanced Open Water Diver": 107508417,
    "[OR-8] Master Scuber Diver": 107508285,
}
Roblox_Role_Rank_Names = {
    role_id: rank_name for rank_name, role_id in Roblox_Rank_Role_IDs.items()
}


def get_ADD_ROLE_RBLX_API_URL(group_id, membership_id):
    return f"https://apis.roblox.com/cloud/v2/groups/{group_id}/memberships/{membership_id}:assignRole"


def get_REMOVE_ROLE_RBLX_API_URL(group_id, membership_id):
    return f"https://apis.roblox.com/cloud/v2/groups/{group_id}/memberships/{membership_id}:unassignRole"


def get_SEE_ROLES_RBLX_API_URL(group_id):
    return f"https://apis.roblox.com/cloud/v2/groups/{group_id}/memberships"