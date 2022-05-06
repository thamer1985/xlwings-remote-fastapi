import datetime as dt
import asyncio
import xlwings as xw
import yfinance as yf
from fastapi import Body
from app import app


from crunchbase import get_data

@app.post("/crunchbase")
def hello(data: dict = Body):
    # Instantiate a Book object with the deserialized request body
    book = xw.Book(json=data)

    if "Crunchbase" not in [sheet.name for sheet in book.sheets]:
        # Insert and prepare the sheet for first use
        sheet = book.sheets.add("Crunchbase")
        sheet["A1"].value = [
            "Crunchbase Scraper",
            "Date:",
            dt.date.today(),
        ]
        
        sheet.activate()
    else:
        # Query Yahoo! Finance
        sheet = book.sheets["Crunchbase"]

    start_cell = sheet['A3']    
    urls = start_cell.options(expand='down', ndim=1).value
    print(urls)
    for ix, url in enumerate(urls):
        data=asyncio.run(get_data(url))
        print(data)
        destination_cell = start_cell.offset(row_offset=ix, column_offset=1)
        destination_cell.value = data

    # Pass the following back as the response
    return book.json()

    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
