from typing import Optional

from fastapi import Depends, FastAPI, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine
from deps import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='API',
    description='Fist API with FastAPI',
    version='1.0',
    docs_url='/api/docs',
)

templates = Jinja2Templates(directory="templates")


@app.on_event('startup')
def startup_populate_db():
    db = SessionLocal()
    num_courses = db.query(models.Course).count()
    if num_courses == 0:
        couses = [
            {'name': 'Django', 'lessons': 160, 'hours': 80},
            {'name': 'Node.JS', 'lessons': 90, 'hours': 55},
            {'name': 'Docker', 'lessons': 30, 'hours': 12},
            {'name': 'Microservices', 'lessons': 60, 'hours': 22},
            {'name': 'React', 'lessons': 140, 'hours': 98}
        ]
        for couse in couses:
            db.add(models.Course(**couse))
        db.commit()
        db.close()
    else:
        print(f'{num_courses} Cursos no seu banco de dados')


@app.get("/index/", response_class=HTMLResponse)
async def courseslist(
    request: Request,
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db),
    page: int = 1
):
    N = 2
    OFFSET = (page - 1) * N
    courses = db.query(models.Course).offset(OFFSET).limit(N)
    context = {"request": request, 'courses': courses, 'page': page}
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
