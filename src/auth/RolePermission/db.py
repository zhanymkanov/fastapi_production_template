
from sqlalchemy import (
    Boolean,
    Column,
    CursorResult,
    DateTime,
    ForeignKey,
    Identity,
    Insert,
    Integer,
    LargeBinary,
    MetaData,
    Select,
    String,
    Table,
    Update,
    func,
    select,
    insert,
    update,
    delete,
    JSON
)
from src.database import metadata
from schemas import RolePermission,RoleDB,roles
from src.database import auth_user, execute, fetch_one,fetch_all, refresh_tokens
from typing import Any


role_permissionsT = Table(
    "role_permissions",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)
user_rolesT = Table(
    "user_roles",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("permissions.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)

async def get_role_permission_by_id(id:int):
    select_query=(select(role_permissionsT).where(role_permissionsT.id == id))
    return await fetch_one(select_query)
async def update_role_permission_by_id(id:int,rp:RolePermission):
    update_query=(update(role_permissionsT).values(rp.serializable_dict()).where(role_permissionsT.id == id))
    return await fetch_one(update_query)

async def create_role_permissions(rp:RolePermission) -> dict[str, Any] | None:
    insert_query= (insert(role_permissionsT)
                   .value(rp.serializable_dict())
                   .returning(role_permissionsT)
                   )
    return await fetch_one(insert_query)
def paginate_role_permissions(table:Table, page=1, per_page=10):
  """
  This function retrieves a paginated list of role_permissions.

  Args:
      page (int, optional): The current page number (defaults to 1).
      per_page (int, optional): The number of items per page (defaults to 10).

  Returns:
      dict: A dictionary containing the following keys:
          data (list): A list of role_permission objects for the current page.
          total (int): The total number of role_permissions.
  """
  # Get the total number of role_permissions
  total = fetch_one(select(table,func.count(table.id))).scalar()

  # Calculate the offset for the current page
  offset = (page - 1) * per_page

  # Query for role_permissions with pagination
  query = select(role_permissionsT).order_by(role_permissionsT.id).limit(per_page).offset(offset)

  # Fetch the data for the current page
  data = fetch_all(query)

  return {
      "data": data,
      "total": total
  }
async def create_role_permissions(rp:RolePermission) -> dict[str, Any] | None:
    insert_query= (insert(role_permissionsT)
                   .value(rp.serializable_dict())
                   .returning(role_permissionsT)
                   )
    return await fetch_one(insert_query)