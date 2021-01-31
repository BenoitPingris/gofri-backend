from fastapi import APIRouter

router = APIRouter(prefix='/foods', tags=['foods'])


@router.get('')
def ping():
    return "foods"


@router.post('')
def lol():
    return "??"
