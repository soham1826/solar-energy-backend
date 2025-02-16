import httpx

async def GetSolarData(cityName:str):
    url = f"https://solar-anywhere-api.onrender.com/api/v2/GetSolarData?cityName={cityName}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        return  response.json()
    else:
        return {"error": f"Failed to fetch data, status code: {response.status_code}"}

