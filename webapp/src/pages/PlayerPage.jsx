import { React } from 'react'
import { useParams } from 'react-router-dom'
import PlayerCard from '../components/PlayerCard'
import '../styles/Search.css'

export default function PlayerPage() {
    const { playerName } = useParams();
    console.log(playerName)
    const nameFormatted = decodeURIComponent(playerName)
    console.log(nameFormatted)

    return (
        <div className="container">
            <div className="searchContainer">
                <PlayerCard playerName={nameFormatted} />
            </div>
        </div>
    )
}