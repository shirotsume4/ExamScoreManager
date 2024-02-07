from fastapi import FastAPI
import controller.user_controller, controller.examscore_controller
from db.dbengine import Base, engine
# table作成
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(controller.user_controller.router)
app.include_router(controller.examscore_controller.router)
