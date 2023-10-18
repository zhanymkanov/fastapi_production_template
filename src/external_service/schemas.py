from pydantic import BaseModel, Field


class EntryResponse(BaseModel):
    api: str = Field(alias="API")
    description: str = Field(alias="Description")
    auth: str = Field(alias="Auth")
    https: bool = Field(alias="HTTPS")
    cors: str = Field(alias="Cors")
    link: str = Field(alias="Link")
    category: str = Field(alias="Category")


class PublicAPIsResponse(BaseModel):
    count: int
    entries: list[EntryResponse]
