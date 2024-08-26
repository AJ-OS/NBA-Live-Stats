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
    return NextResponse.json(coins);
}