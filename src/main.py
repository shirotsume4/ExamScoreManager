from fastapi import FastAPI
import controller.endpoints.user_controller, controller.endpoints.examscore_controller
from models.dbengine.dbengine import Base, engine
# table作成
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(controller.endpoints.user_controller.router)
app.include_router(controller.endpoints.examscore_controller.router)
