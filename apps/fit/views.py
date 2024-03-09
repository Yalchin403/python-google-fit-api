import json
from typing import Annotated, Optional
from fastapi import APIRouter, Cookie, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


from apps.conf import get_settings
from apps.utils.fit_helper import FitnessDataFetcher

templates = Jinja2Templates(directory="apps/fit/templates")
router = APIRouter()
fit_api_fetcher = FitnessDataFetcher()
SETTINGS = get_settings()


@router.get("/", tags=["home"])
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.get("/dashboard", tags=["home"])
async def read_root(request: Request, access_token: Optional[str] = Cookie(None)):
    if not access_token:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"heart_rate_data": {}, "steps_data": {}},
    )


@router.post("/dashboard", tags=["home"])
async def read_root(
    request: Request,
    access_token: Optional[str] = Cookie(None),
    start_date: Annotated[str, Form()] = None,
    end_date: Annotated[str, Form()] = None,
):

    if not access_token:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)

    try:
        await fit_api_fetcher.validate_google_access_token(access_token)
    except Exception as e:
        print(e)
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)

    if not start_date or not end_date:
        return {"error": "Start date and end date are required"}

    heart_rate_data = await fit_api_fetcher.fetch_heart_rate_data(
        start_date, end_date, access_token
    )
    steps_data = await fit_api_fetcher.fetch_steps_data(
        start_date, end_date, access_token
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "heart_rate_data": heart_rate_data,
            "steps_data": steps_data,
        },
    )
