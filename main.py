from fastapi import FastAPI

from database import Base, engine
import tasks
import users

app = FastAPI()
app.include_router(tasks.router)

Base.metadata.create_all(bind=engine)
app.include_router(users.router)
