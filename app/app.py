from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from .db import get_session, engine
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

@app.on_event("startup")
def on_startup():
    # alembic 负责建表迁移，不再这里自动创建
    with Session(engine) as session:
        # 初始化数据
        if not session.exec(select(User)).first():
            user = User(username="alice", hashed_password=get_password_hash("secret"), secret_name='aa')
            session.add(user)

        if not session.exec(select(APIKey)).first():
            api_key = APIKey(key="partner-token-123", owner="PartnerA")
            session.add(api_key)

        session.commit()


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
