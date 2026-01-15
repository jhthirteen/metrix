import { React, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/ResponseCard.css'
import BarChartWrapper from '../components/BarWrapper'
import PieChartWrapper from '../components/PieChartWrapper'

export default function ResponseCard({ playerName, playerImg, responseText, visualData }){

    const navigate = useNavigate();
    const switchToProfile = () => {
        navigate(`/player/${encodeURIComponent(playerName)}`)
    }
    const [hovering, setHovering] = useState(false);

    // API string passed in with [b] tags --> use regex to replace those and wrap the string in bold / colored tags
    // we can trust this string to be rendered as React 'dangerous' HTML 
    const responseTextFormatted = responseText.replace(
        /\[b\](.*?)\[\/b\]/g,
        '<span style="color:#4169E1; font-weight:bold;">$1</span>'
      );

      // hashmap to map API graph type identifier string --> the graph components that they are supposed to represent
      const graphMap = {
        'bar' : BarChartWrapper,
        'pie' : PieChartWrapper
      }

      // state information for which visualization the user is viewing
      const [activeIndex, setActiveIndex] = useState(0);
      const activeChartData = visualData[activeIndex];
      const ChartComponent = graphMap[activeChartData.chart_type];

      // handler for clicking through our chart's, ensure we cycle back to the beginning
      const nextChart = () => {
        setActiveIndex((prevIndex) => (prevIndex + 1) % visualData.length);
      }

      const prevChart = () => {
        if( activeIndex > 0 ){
            setActiveIndex((prevIndex) => (prevIndex - 1) % visualData.length);
        }
      }

    return(
        <div className="responseCardDiv">
            <div className="profileResponseDiv">
                <div className="profileImageContainer" onMouseEnter={() => setHovering(true)} onMouseLeave={() => setHovering(false)} onClick={switchToProfile}>
                    <img src={playerImg} className="profilePicture"></img>
                    {hovering && 
                        <div className="tooltip">
                            <p>Click to view full player profile.</p>
                        </div>
                    }
                </div>
                <div className="answerDiv">
                    <div className="nameDiv">
                        <h2>{playerName}</h2>
                    </div>
                    <div className="responseDiv">
                        <p dangerouslySetInnerHTML={{ __html: responseTextFormatted }} />
                    </div>
                </div>
            </div>
            <div className="additionalQueriesDiv">
                <div style={{width: "90%", height: 225}}>
                    <ChartComponent chartData={activeChartData.chart_data} />
                    {/* Handle the ability to move through charts IF there is more available */}
                    {visualData.length > 1 && (
                        <div>
                            <button onClick={prevChart}>←</button>
                            <button onClick={nextChart}>→</button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}