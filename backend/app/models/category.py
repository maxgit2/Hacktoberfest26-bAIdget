from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, model_validator

CategoryName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=40)
]


class CategoryCreate(BaseModel):
    name: CategoryName
    icon: str | None = None
    color: str | None = None


class CategoryUpdate(BaseModel):
    name: CategoryName | None = None
    icon: str | None = None
    color: str | None = None

    @model_validator(mode="after")
    def validate_fields(self) -> "CategoryUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one field is required")
        if "name" in self.model_fields_set and self.name is None:
            raise ValueError("Name cannot be null")
        return self


class OnboardingRequest(BaseModel):
    catalog_ids: list[str] = Field(default_factory=list)
    custom: list[CategoryCreate] = Field(default_factory=list)


class CategoryResponse(BaseModel):
    id: str
    name: str
    icon: str | None
    color: str | None
    catalog_id: str | None
    is_other: bool


class CategoryListResponse(BaseModel):
    items: list[CategoryResponse]


class OnboardingResponse(BaseModel):
    categories: list[CategoryResponse]


class CatalogItem(BaseModel):
    id: str
    name: str
    icon: str


class CatalogPreset(BaseModel):
    id: str
    name: str
    catalog_ids: list[str]


class CatalogResponse(BaseModel):
    items: list[CatalogItem]
    presets: list[CatalogPreset]
