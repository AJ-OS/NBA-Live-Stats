from flask import Flask, jsonify, request
from flask_cors import CORS
from nba_api.stats.static import players

# app instance
app = Flask(__name__)
CORS(app)

# /receive_data/home
@app.route('/receive_data/home', methods=['POST'])
def receive_data():
    data = request.json 
    print("Data received:", data) 
    return jsonify({'status': 'success', 'receivedData': data}), 200


# /api/home
@app.route("/api/home", methods=['GET'])
def return_home():
    player_list = players.find_players_by_first_name('LeBron')
    
    if player_list:
        first_name = player_list[0]['first_name']
        last_name = player_list[0]['last_name']
    else:
        first_name = "error | not found!"
        last_name = "error | not found!"
    
    #player_list = "debug"
    return jsonify({
        'message': first_name + " " + last_name
    })


if __name__ == "__main__":
    app.run(debug=True, port="8080")