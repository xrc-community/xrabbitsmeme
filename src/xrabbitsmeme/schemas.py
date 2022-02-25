from pydantic import BaseModel


class PagModel(BaseModel):
    page: int
    per_page: int
    total: int
    has_next: bool
