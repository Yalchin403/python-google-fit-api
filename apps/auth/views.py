from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests

from apps.conf import get_settings
from apps.auth.models.users import User
from apps.utils.db import DBSession

SETTINGS = get_settings()
templates = Jinja2Templates(directory="apps/auth/templates")
router = APIRouter()
flow = Flow.from_client_secrets_file(
    client_secrets_file=SETTINGS.GOOGLE_CLIENT_SECRET_FILE,
    scopes=SETTINGS.GOOGLE_SCOPES,
    redirect_uri=SETTINGS.GOOGLE_REDIRECT_URL,
)


@router.get("/auth/login", tags=["auth"])
def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@router.get("/auth/google/login", tags=["auth"])
def google_login():
    authorization_url, _ = flow.authorization_url()
    return RedirectResponse(authorization_url)


@router.get("/auth/google/callback")
async def google_callback(request: Request, response: Response):
    flow.fetch_token(authorization_response=request.url._url)
    credentials = flow.credentials
    token_request = google.auth.transport.requests.Request()
    user_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=SETTINGS.GOOGLE_CLIENT_ID,
    )
    username = user_info.get("given_name", user_info.get("email").split("@")[0])
    email = user_info.get("email")

    with DBSession() as session:
        if not (user := session.query(User).filter(User.email == email).first()):
            user = User(
                email=email,
                username=username,
            )
            session.add(user)
            session.commit()

    response = RedirectResponse(
        url=SETTINGS.DASHBOARD_URL, status_code=status.HTTP_302_FOUND
    )
    response.set_cookie(
        key="access_token", value=credentials.token, httponly=True, expires=60 * 60
    )

    return response
