# Client to pandas server

import httpx


class PandasClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    async def get_data(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/data/")
            return response.json()

    async def update_data(self, data: list[dict]):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/data/update/", json=data)
            return response.json()

    async def modify_data(self, modifications: list[dict]):
        async with httpx.AsyncClient() as client:
            response = await client.patch(f"{self.base_url}/data/modify/", json=modifications)
            return response.json()

    async def describe_data(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/data/describe/")
            return response.json()

    async def save_data(self, path: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/data/save/", json={"path": path})
            return response.json()



class AppState:
    def __init__(self):
        self.df = None
        self.loading = False
        self.error = None

    async def fetch_data(self, client: PandasClient):
        self.loading = True
        try:
            self.df = await client.get_data()
        except Exception as e:
            self.error = str(e)
        finally:
            self.loading = False