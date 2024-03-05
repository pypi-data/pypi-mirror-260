"""callable.py."""

from fastapi import APIRouter, Request

from .handler import execute_request
from .middleware import RequestParams
from .types import SubmitRequest

router: APIRouter = APIRouter(prefix="/jobs", tags=["Callables"])


@router.post("/submit")
async def run_callable(request: Request, submit_request: SubmitRequest):
    params: RequestParams = request.state.params
    return execute_request(
        ctx=params.ctx,
        app_fn=params.callable_fn,
        estimator_fn=params.estimator_fn,
        cost_fn=params.calculator_fn,
        submit_request=submit_request,
    )
