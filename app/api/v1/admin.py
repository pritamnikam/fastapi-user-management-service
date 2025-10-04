from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/admin", response_class=HTMLResponse)
def admin_portal(request: Request):
    # Placeholder HTML for admin portal
    return """
    <html>
        <head><title>Prompt Catalog Admin</title></head>
        <body>
            <h1>Prompt Catalog Admin Portal</h1>
            <p>Manage your AI prompts here.</p>
        </body>
    </html>
    """