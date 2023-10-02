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
         How many grams of protein and calories have I eaten? Show your work and do not include any disclaimers.Be succinct."""


        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = completion.choices[0].message['content'].replace('\n','<br>')

        #answer= "To calculate the grams of protein and calories, we need to look up the nutrition information for each food item you mentioned. Here are the approximate values:<br><br>1 serving of cheesy grits: <br>- Protein: 3 grams<br>- Calories: 130<br><br>2 eggs: <br>- Protein: 12 grams (6 grams per egg)<br>- Calories: 140 (70 calories per egg)<br><br>1/2 cup of white rice:<br>- Protein: 2 grams<br>- Calories: 100<br><br>1/4 bag of Trader Joe's orange chicken:<br>- Protein: 15 grams<br>- Calories: 200<br><br>Now, let's calculate the total grams of protein and calories:<br><br>Protein:<br>3 grams (cheesy grits) + 12 grams (eggs) + 2 grams (white rice) + 15 grams (orange chicken) = 32 grams of protein<br><br>Calories:<br>130 calories (cheesy grits) + 140 calories (eggs) + 100 calories (white rice) + 200 calories (orange chicken) = 570 calories<br><br>Therefore, you have consumed approximately 32 grams of protein and 570 calories."


        return templates.TemplateResponse('index.html', {"request": request, 'answer':answer})

    except Exception as e:
        print(e)
        return templates.TemplateResponse('error.html', {"request": request})

if __name__ == '__main__':
    if os.environ['MODE'] == 'dev':
        uvicorn.run(app, port=1212, host='0.0.0.0')