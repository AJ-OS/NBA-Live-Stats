from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:smash@localhost:5432/nba-stats' #local db in postgress
db = SQLAlchemy(app)


class LeagueLeader(db.Model):
    __tablename__ = 'league_leaders'
    player_id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    player = db.Column(db.String(100))
    team_id = db.Column(db.Integer)
    team = db.Column(db.String(10))
    gp = db.Column(db.Integer)
    min = db.Column(db.Integer)
    fgm = db.Column(db.Integer)
    fga = db.Column(db.Integer)
    fg_pct = db.Column(db.Float)
    fg3m = db.Column(db.Integer)
    fg3a = db.Column(db.Integer)
    fg3_pct = db.Column(db.Float)
    ftm = db.Column(db.Integer)
    fta = db.Column(db.Integer)
    ft_pct = db.Column(db.Float)
    oreb = db.Column(db.Integer)
    dreb = db.Column(db.Integer)
    reb = db.Column(db.Integer)
    ast = db.Column(db.Integer)
    stl = db.Column(db.Integer)
    blk = db.Column(db.Integer)
    tov = db.Column(db.Integer)
    pf = db.Column(db.Integer)
    pts = db.Column(db.Integer)
    eff = db.Column(db.Integer)
    ast_tov = db.Column(db.Float)
    stl_tov = db.Column(db.Float)

# Create the table
with app.app_context():
    db.create_all()

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    with app.app_context():
        for row in data['resultSet']['rowSet']:
            league_leader = LeagueLeader(
                player_id=row[0],
                rank=row[1],
                player=row[2],
                team_id=row[3],
                team=row[4],
                gp=row[5],
                min=row[6],
                fgm=row[7],
                fga=row[8],
                fg_pct=row[9],
                fg3m=row[10],
                fg3a=row[11],
                fg3_pct=row[12],
                ftm=row[13],
                fta=row[14],
                ft_pct=row[15],
                oreb=row[16],
                dreb=row[17],
                reb=row[18],
                ast=row[19],
                stl=row[20],
                blk=row[21],
                tov=row[22],
                pf=row[23],
                pts=row[24],
                eff=row[25],
                ast_tov=row[26],
                stl_tov=row[27]
            )
            db.session.add(league_leader)
        
        db.session.commit()

if __name__ == '__main__':
    load_data('C:/Users/morri/Desktop/db-py-testing/league_leaders.json') #change to local in vercel
