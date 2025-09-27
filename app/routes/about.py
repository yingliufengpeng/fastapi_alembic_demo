from typing import Annotated
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get('/about')
def about():
    return 'v1'