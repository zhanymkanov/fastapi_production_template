import re
from pydantic import EmailStr, Field, validator

from src.models import ORJSONModel

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


class UserBase(ORJSONModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr


class UserDetail(UserBase):
    password: str

    @validator("password")
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password


class UserResponse(UserBase):
    is_admin: bool


class JWTData(ORJSONModel):
    user_id: int = Field(alias="sub")
    is_admin: bool = False


class AccessTokenResponse(ORJSONModel):
    access_token: str
    refresh_token: str
