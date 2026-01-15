import { React, useState } from 'react'
import '../styles/Search.css'
import ResponseCard from '../components/ResponseCard'

export default function Search() {

    const [searchQuery, setSearchQuery] = useState('');
    const [queryAnswer, setQueryAnswer] = useState('');
    const [foundAnswer, setFoundAnswer] = useState(false);

    // state variables for building response card
    const [responseName, setResponseName] = useState('');
    const [responseImg, setResponseImg] = useState('');
    const [responseVisuals, setResponseVisuals] = useState([]);

    const updateQuery = (e) => {
        setSearchQuery(e.target.value);
    }

    const processQuery = async (e) => {
        // prevent the submit form event from reloading the browser
        e.preventDefault();
        const apiRequest = await fetch(`http://127.0.0.1:8000/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'q': searchQuery
            })
        });
        const res = await apiRequest.json();
        const query_category = res.query_type

        // call the tool endpoint w/ the query and the query category to fetch answer
        answerQuery(query_category);
    }

    const answerQuery = async (query_category) => {
        // prevent the submit form event from reloading the browser
        const apiRequest = await fetch(`http://127.0.0.1:8000/usetool`, {
            method: 'POST',
            headers: {
                'Content-Type' : 'application/json',
            },
            body: JSON.stringify({
                'q' : searchQuery,
                'q_type' : query_category
            })
        });
        const res = await apiRequest.json();

        setFoundAnswer(true);
        setResponseName(res.player_name);
        setQueryAnswer(res.stat_formatted);
        setResponseImg(res.player_image);
        setResponseVisuals(res.visuals);
    }

    return (
        <div className="container">
            <div className="searchContainer">
                {!foundAnswer ? (
                    <form className="formContainer" onSubmit={processQuery}>
                    <input
                        className="searchBar"
                        type="text"
                        placeholder="Break down Kyrie Irving's 3 point shooting in the playoffs"
                        value={searchQuery}
                        onChange={updateQuery}
                    />
                    </form>
                ) : (
                    <>
                        <ResponseCard playerName={responseName} playerImg={responseImg} responseText={queryAnswer} visualData={responseVisuals}/>
                    </>
                )}
            </div>
        </div>
    )
}