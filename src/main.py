from api.app.init import xlr8
import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.app.init:xlr8", port=8000, reload=True)
