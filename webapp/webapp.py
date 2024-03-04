from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/table", response_class=HTMLResponse)
async def show_table(request: Request):


    df = pd.read_csv("transformed_data.csv")

    columns = df.columns
    rows = df.values.tolist()

    return templates.TemplateResponse("table.html", {"request": request, "columns": columns, "rows": rows})

