import httpx
import asyncio
import json

#write json data and save to local machine

url = "https://stats.nba.com/stats/leagueleaders?ActiveFlag=&LeagueID=00&PerMode=Totals&Scope=S&Season=2023-24&SeasonType=Regular+Season&StatCategory=PTS"
headers = {"User-Agent": "Mozilla/5.0"}

async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status() 
        return response.json()

async def main():
    data = await fetch_data()
    with open('league_leaders.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Data saved to league_leaders.json")

if __name__ == '__main__':
    asyncio.run(main())
