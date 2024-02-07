import uvicorn

from controller.main import app

if __name__ == "__main__":
    uvicorn.run(app)
