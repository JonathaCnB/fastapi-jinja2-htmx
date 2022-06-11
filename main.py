from typing import Optional

from fastapi import FastAPI, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title='API',
    description='Fist API with FastAPI',
    version='1.0',
    docs_url='/api/docs',
)

templates = Jinja2Templates(directory="templates")


@app.get("/index/", response_class=HTMLResponse)
async def movielist(
    request: Request, hx_request: Optional[str] = Header(None)
):
    films = [
        {'name': 'Blade Runner', 'director': 'Ridley Scott'},
        {'name': 'Pulp Fiction', 'director': 'Quentin Tarantino'},
        {'name': 'Mulholland Drive', 'director': 'David Lynch'},
    ]
    context = {"request": request, 'films': films}
    if hx_request:
        return templates.TemplateResponse("partials/table.html", context)
    return templates.TemplateResponse("index.html", context)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8010,
        log_level='info',
        reload=True,
        debug=True,
    )
