import { React, useEffect, useState } from 'react'
import '../styles/PlayerCard.css'

export default function PlayerCard({ playerName }) {

    // state of the card while fetching data
    const [rendered, setRendered] = useState(false);
    
    // state of the card if it is either flipped or unflipped
    const [flipped, setFlipped] = useState(false);

    // information string for the players profile image
    const [profileImage, setProfileImage] = useState('');

    // information strings for the heading under the name of the card
    const [team, setTeam] = useState('');
    const [jerseyNumber, setJerseyNumber] = useState('');
    const [position, setPosition] = useState('');

    // information strings for the career statistics section
    const [ppg, setPpg] = useState('');
    const [apg, setApg] = useState('');
    const [fgpct, setFgpct] = useState('');
    const [rpg, setRpg] = useState('');
    const [spg, setSpg] = useState('');
    const [bpg, setBpg] = useState('');

    // grab the list of awards as key --> value pairs
    const [awards, setAwards] = useState({});


    const fetchPlayerInfo = async () => {
        const apiRequest = await fetch(`http://127.0.0.1:8000/playercard?player_name=${playerName}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const res = await apiRequest.json();   
        
        // extract the profile image
        setProfileImage(res.IMG);
        
        // set all name card information
        setTeam(res.TEAM);
        setJerseyNumber(res.JERSEY);
        setPosition(res.POSITION);

        // set all career statistics information
        setPpg(res.PPG);
        setApg(res.APG);
        setFgpct(res.FG);
        setRpg(res.RPG);
        setSpg(res.SPG);
        setBpg(res.BPG);

        // set awards list
        setAwards(res.AWARDS);

        // change the state of the card so it can load
        setRendered(true);
    }

    useEffect(() => {
        fetchPlayerInfo();
    }, []);

    return(
        <div className="playerCardDiv">
            {!rendered ? (
                <div className="unflippedDiv">
                    <h1>Fetching Player Data...</h1>
                </div>
            ) : (
                !flipped ? (
                    <div className="unflippedDiv">
                        <button className="flipButton" onClick={() => setFlipped(true)}>See Card</button>
                    </div>
                ) : (
                    <>
                    <div className="profileDiv">
                        <img src={profileImage} className="playerPicture"></img>
                    </div>
                    <div className="accomplishmentsDiv">
                        <div className="nameSection">
                            <h1 className="nameSectionName">{playerName}</h1>
                            <p className="nameSectionDescription">{team} | {jerseyNumber} | {position}</p>
                        </div>
                        <div className="accomplishmentsSubWrapper">
                            <div className="statsSection">
                                <h2>Career Statistics</h2>
                                <div className="statsGrid">
                                    <div className="statsGridCell">
                                        <p>PPG</p>
                                        <b>{ppg}</b>
                                    </div>
                                    <div className="statsGridCell">
                                        <p>APG</p>
                                        <b>{apg}</b>
                                    </div>
                                    <div className="statsGridCell">
                                        <p>FG %</p>
                                        <b>{fgpct}</b>
                                    </div>
                                    <div className="statsGridCell">
                                        <p>RPG</p>
                                        <b>{rpg}</b>
                                    </div>
                                    <div className="statsGridCell">
                                        <p>SPG</p>
                                        <b>{spg}</b>
                                    </div>
                                    <div className="statsGridCell">
                                        <p>BPG</p>
                                        <b>{bpg}</b>
                                    </div>
                                </div>
                            </div>
                            <div className="awardsSection">
                                <h2>Awards</h2>
                                <ul className="awardsList">
                                    {Object.entries(awards).map(([awardName, frequency]) => (
                                        <li>
                                            {frequency}x {awardName}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>
                    </>
                )
            )}
        </div>
    )
}