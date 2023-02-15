from fastapi import FastAPI

from apps.site.routes.user_routes import user_router
from apps.site.routes.post_routes import post_router
from database.db_connection import db


app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)

# app.mount(
#     "/static",
#     StaticFiles(directory="apps/site/static/"),
#     name="static",
# )


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()