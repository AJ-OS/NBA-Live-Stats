import React, { useEffect, useState } from "react";
import { RiGithubLine } from "react-icons/ri";

import Coins from './Search/Coins';
import SearchCoins from './Search/SearchCoins';

function Home() {

  // live game scores
  const [message2, setMessage2] = useState("Loading");
  const [home, setHome] = useState("Loading");
  const [away, setAway] = useState("Loading");
  const [homeScore, setHomeScore] = useState(0);
  const [awayScore, setAwayScore] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      fetch("http://localhost:8080/api/scoreboard")
        .then(response => response.json())
        .then(data => {
          if (data.length > 0) {
            setHome(data[0].category);
            setAway(data[0].away_team_tricode);
            setHomeScore(data[0].home_team_score);
            setAwayScore(data[0].away_team_score);
            setMessage2("");
          } else {
            setMessage2("No current games");
          }
        })
        .catch(error => {
          console.error("Error getting data", error);
          setMessage2("Failed");
        });
    }, 20000); // 20sec wait time |  rewrite with socket connection?

    // Cleanup function to clear interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  // end of live game scores


  // ----------------------------
  // needs a rewrite to sort through all league leaders 
  // ----------------------------
  // start of league leaders
  const [leagueLeaders, setLeagueLeaders] = useState({
    points: { id: '', name: 'loading', score: 0 },
    rebounds: { id: '', name: 'loading', score: 0 },
    assists: { id: '', name: 'loading', score: 0 },
    blocks: { id: '', name: 'loading', score: 0 },
    steals: { id: '', name: 'loading', score: 0 }
  });

  useEffect(() => {
    fetch("http://localhost:8080/api/leaders")
      .then(response => response.json())
      .then(data => {
        if (data.length >= 4) {
          const categories = ['points', 'rebounds', 'assists', 'blocks', 'steals'];
          const updatedLeaders = categories.reduce((acc, category, index) => {
            const details = data[index].split(',');
            // need implement interface to stop type error 
            acc[category] = { id: details[3], name: details[1], score: parseInt(details[2], 10) };
            return acc;
          }, {});

          setLeagueLeaders(prevState => ({
            ...prevState,
            ...updatedLeaders
          }));
        } else {
          setLeagueLeaders(prevState => ({ ...prevState, name: "Error fetching player data" }));
        }
      })
      .catch(error => {
        console.error("Error getting player data", error);
        setLeagueLeaders(prevState => ({ ...prevState, name: "Failed!" }));
      });
  }, []);

  // end of league leaders

  const [coins, setCoins] = useState([]);

  useEffect(() => {
    const getCoins = async () => {
      const response = await fetch('/api/coins');
      const coins = await response.json();
      setCoins(coins.data.coins);
    }

    getCoins();
  }, []);

  return (
    <div>

      <div className="text-center">
        <h1 className="font-bold text-6xl mt-14">NBA Players</h1>
        <SearchCoins getSearchResults={(results) => setCoins(results)} />
        <Coins coins={coins} />
      </div>

      <div className="today-game">
        <strong>Live Games</strong>
        {message2 !== "Loading" ? (
          <div className="scores">
            {message2 === "No current games" ? (
              <p>No current games</p>
            ) : (
              <>
                <strong>Home Team:</strong> {home} - <strong>Score:</strong> {homeScore}
                <strong> | </strong>
                <strong>Away Team:</strong> {away} - <strong>Score:</strong> {awayScore}
              </>
            )}
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </div>




      <div className="league-title">
        <strong>2023-2024 NBA Regular Season Leaders</strong> <p></p>
        {new Date().toDateString()}
      </div>


      <div className="league-stats-container">
        <div className="league-stats">

          {/* Points Leader */}
          <div className="PTS-lead">
            <p>Points</p>
            <img src={`https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/${leagueLeaders.points.id}.png`} alt="pts-lead" />
            {leagueLeaders.points.name}
            <p></p>
            <strong>{leagueLeaders.points.score}</strong> Points
          </div>

          {/* Rebounds Leader */}
          <div className="PTS-lead">
            Assists
            <img src={`https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/${leagueLeaders.rebounds.id}.png`} alt="Assists-lead" />
            {leagueLeaders.rebounds.name}
            <p></p>
            <strong>{leagueLeaders.rebounds.score}</strong> Assists
          </div>

          {/* Rebounds Leader */}
          <div className="PTS-lead">
            Rebounds
            <img src={`https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/${leagueLeaders.assists.id}.png`} alt="Rebounds-lead" />
            {leagueLeaders.assists.name}
            <p></p>
            <strong>{leagueLeaders.assists.score}</strong> Rebounds
          </div>

          {/* Blocks Leader */}
          <div className="PTS-lead">
            Blocks
            <img src={`https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/${leagueLeaders.blocks.id}.png`} alt="Blocks-lead" />
            {leagueLeaders.blocks.name}
            <p></p>
            <strong>{leagueLeaders.blocks.score}  </strong> Blocks
          </div>

          {/* Steals Leader */}
          <div className="PTS-lead">
            Steals
            <img src={`https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/${leagueLeaders.steals.id}.png`} alt="Steals-lead" />
            {leagueLeaders.steals.name}
            <p></p>
            <strong>{leagueLeaders.steals.score}</strong> Steals
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
