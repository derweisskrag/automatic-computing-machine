from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from tomodachi_core.tomodachi.services.pandas_service import PandasService
from contextlib import asynccontextmanager
import pandas as pd

"""
This module sets up the FastAPI application and its lifespan context manager.
It initializes the PandasService and loads the initial DataFrame.

It also configures CORS middleware to allow requests from specified origins.

"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pandas_service = PandasService("") # Tomorrow: hot fix 

    # Uncomment the next line if you want to load a DataFrame from a CSV file at startup
    # app.state.data_frame = app.state.pandas_service.get_df().unwrap_or(pd.DataFrame())
    yield

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/data/")
def get_data(request: Request):
    """
    Endpoint to retrieve the current DataFrame.
    """
    service: PandasService = request.app.state.pandas_service
    df = service.get_df().unwrap_or(pd.DataFrame())
    return df.to_dict(orient='records')


@app.post("/data/update/")
def update_data(request: Request, new_data: list[dict]):
    """
    Endpoint to update the DataFrame with new data.
    """
    service: PandasService = request.app.state.pandas_service
    new_df = pd.DataFrame(new_data)
    
    if service.update_dataframe(new_df).is_err():
        return {"error": "Failed to update DataFrame."}
    
    return {"message": "DataFrame updated successfully."}


@app.post("/data/save/")
def save_data(request: Request, path: str):
    """
    Endpoint to save the current DataFrame to a specified path.
    """
    service: PandasService = request.app.state.pandas_service
    
    if service.save_dataframe(path).is_err():
        return {"error": "Failed to save DataFrame."}
    
    return {"message": f"DataFrame saved successfully to {path}."}


# PATCH method
@app.patch("/data/modify/")
def modify_data(request: Request, modifications: list[dict]):
    """
    Endpoint to modify the DataFrame based on provided modifications.
    """
    service: PandasService = request.app.state.pandas_service
    df = service.get_df().unwrap_or(pd.DataFrame())
    
    for mod in modifications:
        if 'index' in mod and 'column' in mod and 'value' in mod:
            df.at[mod['index'], mod['column']] = mod['value']
    
    service.update_dataframe(df)
    
    return {"message": "DataFrame modified successfully."}


@app.get("/data/describe/")
def describe_data(request: Request):
    """
    Endpoint to get a statistical description of the DataFrame.
    """
    service: PandasService = request.app.state.pandas_service
    df = service.get_df().unwrap_or(pd.DataFrame())
    
    if df.empty:
        return {"error": "DataFrame is empty."}
    
    description = df.describe().to_dict()
    return description

