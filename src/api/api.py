from fastapi import FastAPI

import uvicorn

from api.routes.routes import Routes


class Api:
    def serve(self):
        app = FastAPI()
        Routes.register(app)
        uvicorn.run(app, host="0.0.0.0", port=8000)
