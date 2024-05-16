import re

from pydantic import EmailStr, Field, field_validator

from src.models import CustomModel
from src.auth.RolePermission.config import permission_conf
STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


class RolePermission(CustomModel):
    name: str
    permissions:dict

    @field_validator("permissions", mode="after")
    @classmethod
    def valid_password(cls, permissions: dict) -> dict:
        for (permission,actions) in permissions.items():
            if permission not in permission_conf:
                raise ValueError(
                    "permission not found"
                )
            for action in actions:
                if action not in permission_conf[permission].actions:
                    actions = permission_conf[permission].actions.join(",")
                    raise ValueError(
                    f"{permission} actions are [{actions}]"
                    )   
                

        return permissions


class RolePermissionDB(RolePermission):
    id: int
    class Config:
        orm_mode = True


# class RoleTable(Base):
#     __tablename__ = "roles"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True)

#     permissions = relationship(PermissionTable, secondary_table="role_permissions")

#     email: EmailStr

# class PermissionTable(Base):
#     __tablename__ = "permissions"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True)

#     roles = relationship(RoleTable, secondary_table="role_permissions")


# role_permissions = Table(
#     "role_permissions",
#     Base.metadata,
#     Column("role_id", ForeignKey("roles.id"), primary_key=True),
#     Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
# )