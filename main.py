import pandas as pd
from fastapi import FastAPI, Request, BackgroundTasks, Response, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn
import os




# Launch app and mount assets
app = FastAPI()
app.mount("macros/assets", StaticFiles(directory="macros/assets"), name="assets")
templates = Jinja2Templates(directory="templates/webapp")



@app.get("/")
async def home(request: Request):
    try:
        # rest card template
        out_html = ''

        return templates.TemplateResponse('index_inset.html', {"request": request, 'card_inserts':out_html})

    except Exception as e:
        print(e)
        return templates.TemplateResponse('error.html', {"request": request})



if __name__ == '__main__':
    if os.environ['MODE'] == 'dev':
        uvicorn.run(app, port=4242, host='0.0.0.0')