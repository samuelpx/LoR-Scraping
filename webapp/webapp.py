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
    rows = df.head(30).values.tolist()

    average = df.groupby('name')['rank'].mean().reset_index()

    average_columns = average.columns
    average_rows = average.sort_values(by="rank", ascending=True).head(30).values.tolist()

    return templates.TemplateResponse("table.html", {"request": request,
                                                     "columns": columns,
                                                     "rows": rows,
                                                     "average_rows": average_rows,
                                                     "average_columns": average_columns})

