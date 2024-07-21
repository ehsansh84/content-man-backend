from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


module_name = 'pages'
# module_text = ''
router = APIRouter(
    prefix=f"/{module_name}",
    tags=[module_name]
)

templates = Jinja2Templates(directory="templates")


@router.get("/privacy_policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse("privacy_policy.html", {"request": request})


@router.get("/terms_conditions", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse("terms_conditions.html", {"request": request})

