from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status,HTTPException
from src.auth.RolePermission.schemas import RolePermission,RolePermissionDB
import src.auth.RolePermission.db  as db
router = APIRouter()

# CRUD operations for roles

@router.get("/roles/" )
async def create_rolepermision(page:int=1,per_page:int=10):
    return db.paginate_role_permissions(page=page,per_page=per_page)
@router.post("/roles/")
async def create_rolepermision(roleP: RolePermission):
    return db.create_role_permissions(roleP)
@router.put("/roles/")
async def update_rolepermision(db_role: RolePermissionDB):
    db_role = db.get_role_permission_by_id(db_role.id)
    if db_role in None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    db.update_role_permission(db_role)
@router.delete("/roles/{role_id}")
async def get_role(role_id: int):
    db_role = db.get_role_permission_by_id(role_id)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return db.delete_role_permissions(role_id)


# @router.put("/roles/{role_id}", response_model=RoleDB)
# async def update_role(role_id: int, role: Role, db: Session = Depends(get_session)):
#     try:
#         db_role = db.query(RoleTable).filter(RoleTable.id == role_id).first()
#         if db_role is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
#         db_role.name = role.name
#         db.commit()
#         db.refresh(db_role)
#         return RoleDB.from_orm(db_role)
#     except ValidationError as e:
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str())
# @router.delete("/roles/{role_id}")
# async def delete_role(role_id: int, db: Session = Depends(get_session)):
#     db_role = db.query(RoleTable).filter(RoleTable.id == role_id).first()
#     if db_role is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
#     db.delete(db_role)
#     db.commit()
#     return {"message": "Role deleted successfully"}


# # CRUD operations for permissions

# @router.post("/permissions/", response_model=PermissionDB)
# async def create_permission(permission: Permission, db: Session = Depends(get_session)):
#     try:
#         db_permission = PermissionTable(name=permission.name)
#         db.add(db_permission)
#         db.commit()
#         db.refresh(db_permission)
#         return PermissionDB.from_orm(db_permission)
#     except ValidationError as e:
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# @router.get("/permissions/{permission_id}", response_model=PermissionDB)
# async def get_permission(permission_id: int, db: Session = Depends(get_session)):
#     db_permission = db.query(PermissionTable).filter(PermissionTable.id == permission_id).first()
#     if db_permission is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
#     return PermissionDB.from_orm(db_permission)



# # CRUD for role-permission assignments

# @router.post("/roles/{role_id}/permissions/{permission_id}")
# async def assign_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_session)):
#     db_role = db.query(RoleTable).filter(RoleTable.id == role_id).first()
#     if db_role is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

#     db_permission = db.query(PermissionTable).filter(PermissionTable.id == permission_id).first()
#     if db_permission is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

#     if db_permission not in db_role.permissions:
#         db_role.permissions.append(db_permission)
#         db.commit()
#         return {"message": "Permission assigned to role successfully"}


# @router.delete("/roles/{role_id}/permissions/{permission_id}")
# async def remove_permission_from_role(role_id: int, permission_id: int, db: Session = Depends(get_session)):
#     db_role = db.query(RoleTable).filter(RoleTable.id == role_id).first()
#     if db_role is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

#     db_permission = db.query(PermissionTable).filter(PermissionTable.id == permission_id).first()
#     if db_permission is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

#     if db_permission in db_role.permissions:
#         db_role.permissions.remove(db_permission)
#         db.commit()
#         return {"message": "Permission removed from role successfully"}
#     else:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission is not assigned to this role")