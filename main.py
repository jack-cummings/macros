import pandas as pd
from fastapi import FastAPI, Request, BackgroundTasks, Response, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn
import os
import openai



# Launch app and mount assets
app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates/webapp")
openai.api_key = os.environ['oaik']



@app.get("/")
async def home(request: Request):
    try:
        answer = ''
        return templates.TemplateResponse('index.html', {"request": request, 'answer':answer})

    except Exception as e:
        print(e)
        return templates.TemplateResponse('error.html', {"request": request})

@app.post('/query')
async def query(request: Request):
    try:
        body = await request.body()
        base = body.decode('UTF-8').split('&')[0].split('=')[1].replace('+',' '
                                                                        ).replace('%2C',',').replace('%0D',''
                                                                                                     ).replace('%0A','')
        print(base)
        prompt = f"""Today I've eaten {base}.
         How many grams of protein and calories have I eaten? Show your work"""


        # completion = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": prompt}
        #     ]
        # )
        #
        # answer = completion.choices[0].message

        answer=prompt

        return templates.TemplateResponse('index.html', {"request": request, 'answer':answer})

    except Exception as e:
        print(e)
        return templates.TemplateResponse('error.html', {"request": request})

if __name__ == '__main__':
    if os.environ['MODE'] == 'dev':
        uvicorn.run(app, port=4242, host='0.0.0.0')