from fastapi import APIRouter

from .router_deposit import router as router_deposit

router_api = APIRouter(prefix='/api', tags=['Api'])

router_api.include_router(router_deposit)
