# import uvicorn
# from app.api import app
#
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8076, log_level='info')
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import uvicorn
from typing import List

from starlette.middleware.cors import CORSMiddleware

from backend.app.api import app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
