from flask import Flask, jsonify, request
from flask_cors import CORS
from nba_api.stats.static import players
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import playercareerstats
import requests


""" all set params below
'PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 
'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 
'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'
"""


# fix currently only showing stats for first year of play
def searchDictJson(player_dict, ID_Header):
    # find players team abbreviation
    temp = None
    if player_dict["resultSets"]:
        for resultSet in player_dict["resultSets"]:
            if ID_Header in resultSet["headers"]:
                index = resultSet["headers"].index(ID_Header)
                temp = resultSet["rowSet"][0][index]
                break
    return temp


app = Flask(__name__)
CORS(app)


# --------------------------------
# function needs rewrite with dict
# --------------------------------
# search player by full name NBA
@app.route("/api/search", methods=["POST"])
def search_player():
    # get users input from tsx
    data = request.json
    player_name = data.get("name", "")

    findPlayer = players.find_players_by_full_name(player_name)

    inputId = findPlayer[0]["id"]

    # get players stats
    career = playercareerstats.PlayerCareerStats(player_id=inputId)

    # dictionary
    player_dict = career.get_dict()

    team_abb = searchDictJson(player_dict, "GP")






# get live game scores NBA
@app.route("/api/scoreboard", methods=["GET"])
def search_scoreboard():
    games = scoreboard.ScoreBoard()
    games_dict = games.get_dict()
    currentGames = []

    # go over game in dict and display 1 game for now
    for game in games_dict["scoreboard"]["games"]:
        # init
        home = game["homeTeam"]
        away = game["awayTeam"]
        status = game["gameStatus"]

        # check if game is on/live
        if status == 2:
            gameInfo = {
                "home_team_tricode": home["teamTricode"],
                # setHome(data[0].home_team_tricode);
                "home_team_score": home["score"],
                "away_team_tricode": away["teamTricode"],
                "away_team_score": away["score"],
            }
            currentGames.append(gameInfo)

    # return list of live games
    if currentGames:
        return jsonify(currentGames), 200
    else:
        return (
            jsonify(
                {"message": "There are currently no games live.", "status": "info"}
            ),
            200,
        )


# get stats leaders for 23-24 NBA season through request/url response
@app.route("/api/leaders", methods=["GET"])
def search_leaders():
    stats_categories = ["PTS", "AST", "REB", "BLK", "STL"]
    results = []

    for i, category in enumerate(stats_categories):
        url = f"https://stats.nba.com/stats/leagueleaders?ActiveFlag=&LeagueID=00&PerMode=Totals&Scope=S&Season=2023-24&SeasonType=Regular+Season&StatCategory={category}"

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        if response.status_code == 200:
            data = response.json()
            players = data.get("resultSet", {}).get("rowSet", [])

            #rewrite?
            if players:
                top_player = players[0]
                player_id = top_player[0]
                player_name = top_player[2]
                if category == "PTS":
                    player_stat_value = top_player[24]
                elif category == "AST":
                    player_stat_value = top_player[19]
                elif category == "REB":
                    player_stat_value = top_player[18]
                elif category == "BLK":
                    player_stat_value = top_player[21]
                elif category == "STL":
                    player_stat_value = top_player[20]
                results.append(
                    f"{category},{player_name},{player_stat_value},{player_id},{category.lower()}"
                )
            else:
                results.append(f"No data available for {category}.")
        else:
            results.append(f"Failed to retrieve data for {category}.")

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, port="8080")


'''

    # get users input from tsx
    data = request.json
    player_name = data.get("name", "")

    findPlayer = players.find_players_by_full_name(player_name)

    inputId = findPlayer[0]["id"]

    # get players stats
    career = playercareerstats.PlayerCareerStats(player_id=inputId)

    # dictionary
    player_dict = career.get_dict()

    team_abb = searchDictJson(player_dict, "GP")

    # testing case results
    if findPlayer:
        first_name = findPlayer[0][
            "first_name"
        ]  # use findPlayer for some reason dict does not show name?
        last_name = findPlayer[0]["last_name"]
        test = team_abb
        return (
            jsonify(
                {"message": f"{first_name} {last_name}, {test}", "status": "success"}
            ),
            200,
        )
    else:
        return jsonify({"message": "Player not found!", "status": "error"}), 404

'''