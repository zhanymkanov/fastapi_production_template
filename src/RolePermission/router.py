from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from schemas import Role,RoleDB
router = APIRouter()

# CRUD operations for roles

@router.post("/roles/", response_model=RoleDB)
async def create_role(role: Role):
    try:
        db_role = RoleTable(name=role.name)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return RoleDB.from_orm(db_role)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/roles/{role_id}", response_model=RoleDB)
async def get_role(role_id: int, db: Session = Depends(get_session)):
    db_role = db.query(RoleTable).filter(RoleTable.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return RoleDB.from_orm(db_role)


@router.put("/roles/{role_id}", response_model=RoleDB)
async def update_role(role_id: int, role: Role, db: Session = Depends(get_session)):
    try:
        db_role = db.query(RoleTable).filter(RoleTable.id == role_id).first()
        if db_role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        db_role.name = role.name
        db.commit()
        db.refresh(db_role)
        return RoleDB.from_orm(db_role)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str())
@router.delete("/roles/{role_id}")
async def delete_role(role_id: int, db: Session = Depends(get_session)):
    db_role = db.query(RoleTable).filter(RoleTable.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    db.delete(db_role)
    db.commit()
    return {"message": "Role deleted successfully"}


# CRUD operations for permissions

@router.post("/permissions/", response_model=PermissionDB)
async def create_permission(permission: Permission, db: Session = Depends(get_session)):
    try:
        db_permission = PermissionTable(name=permission.name)
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return PermissionDB.from_orm(db_permission)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/permissions/{permission_id}", response_model=PermissionDB)
async def get_permission(permission_id: int, db: Session = Depends(get_session)):
    db_permission = db.query(PermissionTable).filter(PermissionTable.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return PermissionDB.from_orm(db_permission)



# CRUD for role-permission assignments

@router.post("/roles/{role_id}/permissions/{permission_id}")
async def assign_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_session)):
    db_role = db.query(RoleTable).filter(RoleTable.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    db_permission = db.query(PermissionTable).filter(PermissionTable.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    if db_permission not in db_role.permissions:
        db_role.permissions.append(db_permission)
        db.commit()
        return {"message": "Permission assigned to role successfully"}


@router.delete("/roles/{role_id}/permissions/{permission_id}")
async def remove_permission_from_role(role_id: int, permission_id: int, db: Session = Depends(get_session)):
    db_role = db.query(RoleTable).filter(RoleTable.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    db_permission = db.query(PermissionTable).filter(PermissionTable.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    if db_permission in db_role.permissions:
        db_role.permissions.remove(db_permission)
        db.commit()
        return {"message": "Permission removed from role successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission is not assigned to this role")