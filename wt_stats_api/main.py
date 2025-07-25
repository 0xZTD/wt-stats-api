from fastapi import FastAPI

from wt_stats_api.api import endpoitns

app = FastAPI()
app.include_router(endpoitns.router)
