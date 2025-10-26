from typing import Annotated

from fastapi import Depends

from schemas.links import PaginationParams


PaginationParamsDep = Annotated[PaginationParams, Depends(PaginationParams)]
