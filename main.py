from fastapi import FastAPI, HTTPException, Form,Query
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from DataPipeline.ParseHtml import get_text
from DataPipeline.ValidateInput import validate_url
from DataPipeline.DataChunking import chunking
from DataPipeline.QueryData import data_query
from fastapi import FastAPI, HTTPException, Form,Query
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from DataPipeline.ParseHtml import get_text
from DataPipeline.ValidateInput import validate_url
from DataPipeline.DataChunking import chunking
from DataPipeline.QueryData import data_query

app = FastAPI(debug=True, title="Khirrki")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change to specific origins for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)



@app.get("/scraip")
async def run_pipeline(url: str = Query(...), query: str = Query(...)):

    if not validate_url.validate_url(url=url):
        raise HTTPException(status_code=400, detail="Failed to validate url, please enter a valid url")

    try:
        text = await get_text.get_page_text(url=url)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting text: "+e.__str__())


    # TEMPORARY CODE FOR PRESENTATION
    # try:
    #     # Example usage
    #     file_path = "ParseHtml/shortened_mobile.txt"
    #     text = read_string_from_file(file_path)
    # except:
    #     raise HTTPException(status_code=400, detail="Failed to retrieve sample text")

    try:
        data = await chunking.chunk(text=text)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error chunking data: "+e.__str__())

    try:
        result = await data_query.run_query(query=query, data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error running query on data: "+e.__str__())

    return result




def read_string_from_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

app = FastAPI(debug=True, title="Khirrki")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change to specific origins for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)



@app.get("/scraip")
async def run_pipeline(url: str = Query(...), query: str = Query(...)):

    if not validate_url.validate_url(url=url):
        raise HTTPException(status_code=400, detail="Failed to validate url, please enter a valid url")

    try:
        text = await get_text.get_page_text(url=url)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting text: "+e.__str__())


    # TEMPORARY CODE FOR PRESENTATION
    # try:
    #     # Example usage
    #     file_path = "ParseHtml/shortened_mobile.txt"
    #     text = read_string_from_file(file_path)
    # except:
    #     raise HTTPException(status_code=400, detail="Failed to retrieve sample text")

    try:
        data = await chunking.chunk(text=text)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error chunking data: "+e.__str__())

    try:
        result = await data_query.run_query(query=query, data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error running query on data: "+e.__str__())

    return result




def read_string_from_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


uvicorn.run(app,port=10000)
