from fastapi import FastAPI
print(f'xxxxx __file__ is {__file__}')
import sys 
print(f'yyyyyyyyyy  {sys.argv}')

# breakpoint()

from app.db import Base, engine
from app.routes import user

# 创建表（第一次用）
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app",
                host="0.0.0.0",
                port=5000,
                reload=False,
                use_colors=True,

    )




