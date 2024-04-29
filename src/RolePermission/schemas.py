import re

from pydantic import EmailStr, Field, field_validator

from src.models import CustomModel

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")



class Role(CustomModel):
    id: int = None
    name: str


class Permission(CustomModel):
    id: int = None
    name: str


class RolePermission(CustomModel):
    role_id: int
    permission_id: int


class RoleDB(CustomModel):
    id: int
    name: str
    permissions: list[Permission] = []

    class Config:
        orm_mode = True


class PermissionDB(CustomModel):
    id: int
    name: str
    roles: list[Role] = []

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