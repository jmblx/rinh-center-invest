import fastapi

router = fastapi.APIRouter(prefix="", tags=["homepage"])


@router.get("/")
def homepage():
    return "127.0.0.1:8000/docs"
