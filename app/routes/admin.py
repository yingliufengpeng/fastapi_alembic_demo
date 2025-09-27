from typing import Annotated
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get('/admin')
def about():
    return 'admin'