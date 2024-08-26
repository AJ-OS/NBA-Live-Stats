import { NextResponse } from "next/server";

async function fetchCoins() {
    const response = await fetch('/api/league-stats', {
        "method": "GET",
        })
        
        const coins = await response.json();
        return coins;

}

export async function GET(request) {
    const coins = await fetchCoins();
    const { searchParams } = new URL(request.url);
    console.log(searchParams.get('query'))
    const query = searchParams.get('query');

    const filteredCoins = coins.data.coins.filter((coin) => {
        return coin.name.toLowerCase().includes(query.toLowerCase()) || coin.symbol.toLowerCase().includes(query.toLowerCase())
    })

    return NextResponse.json(filteredCoins);
}