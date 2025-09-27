from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from contextlib import asynccontextmanager

from .db import get_session, AsyncSessionLocal
from .models import User, APIKey, SQLModel
from .auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
    get_api_key,
)

from . import routes

app = FastAPI()
app.include_router(routes.about, tags=['About'])
app.include_router(routes.user, tags=['User'])


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup 逻辑
    print("Application startup", flush=True)
    yield
    # Shutdown 逻辑
    print("Application shutdown", flush=True)

admin = FastAPI(lifespan=lifespan)
admin.include_router(routes.admin, tags=['Admin'])

@app.on_event("startup")
async def on_startup():
    async with AsyncSessionLocal() as session:
        # breakpoint()
        result = await session.execute(select(User))
        if not result.scalars().first():
            user = User(username="alice", hashed_password=get_password_hash("secret"), secret_name='aa')
            session.add(user)

            # 查询 APIKey
        result = await session.execute(select(APIKey))
        api_key = result.scalars().first()
        if not api_key:
            session.add(APIKey(
                key="partner-token-123",
                owner="PartnerA"
            ))

        # 提交事务
        await session.commit()



@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/user-data")
async def read_user_data(user: User = Depends(get_current_user)):
    return {"msg": f"Hello {user.username}, protected user data"}


@app.get("/external-data", tags=["External"])
async def read_external(api_key: APIKey = Depends(get_api_key)):
    return {"msg": f"Hello {api_key.owner}, external API access granted"}
