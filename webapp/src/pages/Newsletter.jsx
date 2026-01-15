import React, { useState, useEffect } from 'react';
import { ChartNoAxesCombined, BarChart3, Calendar, TrendingUp, ArrowLeft, Sun, Moon, Share2, Timer, Star, ChevronLeft, ChevronRight, Newspaper } from 'lucide-react';
import MetrixLogoBlack from '../assets/Metrix.png'
import MetrixLogoWhite from '../assets/MetrixWhite.png'

export default function Newsletter() {
  const [darkMode, setDarkMode] = useState(false);
  // state information to be populated with newsletter content from Metrix API
  const [summaries, setSummaries] = useState([]);
  const [newsStories, setNewsStories] = useState([]);
  const [highlights, setHighlights] = useState([]);
  const [eastStandings, setEastStandings] = useState({});
  const [westStandings, setWestStandings] = useState({});
  // date for display & fetching relevant data. Need ISO format to communicate with backend
  const today = new Date();
  const isoToday = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().split('T')[0];
  const displayDate = today.toDateString().split(' ').slice(1).join(' ');

  // mapping of Team ID --> team name (for clean display of standing information)
  const TEAMS = {
    1610612737: { name: "Hawks", abbr: "ATL" },
    1610612738: { name: "Celtics", abbr: "BOS" },
    1610612739: { name: "Cavaliers", abbr: "CLE" },
    1610612740: { name: "Pelicans", abbr: "NOP" },
    1610612741: { name: "Bulls", abbr: "CHI" },
    1610612742: { name: "Mavericks", abbr: "DAL" },
    1610612743: { name: "Nuggets", abbr: "DEN" },
    1610612744: { name: "Warriors", abbr: "GSW" },
    1610612745: { name: "Rockets", abbr: "HOU" },
    1610612746: { name: "Clippers", abbr: "LAC" },
    1610612747: { name: "Lakers", abbr: "LAL" },
    1610612748: { name: "Heat", abbr: "MIA" },
    1610612749: { name: "Bucks", abbr: "MIL" },
    1610612750: { name: "Timberwolves", abbr: "MIN" },
    1610612751: { name: "Nets", abbr: "BKN" },
    1610612752: { name: "Knicks", abbr: "NYK" },
    1610612753: { name: "Magic", abbr: "ORL" },
    1610612754: { name: "Pacers", abbr: "IND" },
    1610612755: { name: "76ers", abbr: "PHI" },
    1610612756: { name: "Suns", abbr: "PHX" },
    1610612757: { name: "Blazers", abbr: "POR" },
    1610612758: { name: "Kings", abbr: "SAC" },
    1610612759: { name: "Spurs", abbr: "SAS" },
    1610612760: { name: "Thunder", abbr: "OKC" },
    1610612761: { name: "Raptors", abbr: "TOR" },
    1610612762: { name: "Jazz", abbr: "UTA" },
    1610612763: { name: "Grizzlies", abbr: "MEM" },
    1610612764: { name: "Wizards", abbr: "WAS" },
    1610612765: { name: "Pistons", abbr: "DET" },
    1610612766: { name: "Hornets", abbr: "CHA" },
  };

  // main API call. One main call populates all relevant newsletter fields. This request should only run once upon load.
  useEffect(() => {
    const fetchSummaries = async (e) => {
      const req = await fetch(`http://127.0.0.1:8000/fetchsummaries?games_date=${isoToday}`);
      const result = await req.json();

      setSummaries(result.summaries);
      setNewsStories(result.news);
      setHighlights(result.highlights);
      setEastStandings(result.standings.eastern_conference_deltas);
      setWestStandings(result.standings.western_conference_deltas);
    };

    fetchSummaries();
  }, []);

  // state elements that control what highlight the user is looking at 
  const [highlightIndex, setHighlightIndex] = useState(0);

  // move to the next highlight (loop back to the beginning if we reach the end)
  const nextHighlight = () => {
    setHighlightIndex((prevIndex) => (prevIndex + 1) % highlights.length);
  }
  // move to the previous highlight
  const prevHighlight = () => {
    // check to make sure the user can't go past the 0th highlight
    if (highlightIndex > 0) {
      setHighlightIndex((prevIndex) => (prevIndex - 1) % highlights.length);
    }
  }
  const currentHighlight = highlights[highlightIndex];

  // newsletter styling. TODO: clean this up signifcantly, maybe move to a seperate stylesheet
  const s = {
    container: { minHeight: '100vh', width: '100%', backgroundColor: darkMode ? '#000' : '#fff', color: darkMode ? '#fff' : '#000', transition: 'all 0.3s ease', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' },
    nav: { position: 'fixed', top: 0, left: 0, right: 0, backgroundColor: darkMode ? 'rgba(0,0,0,0.95)' : 'rgba(255,255,255,0.95)', backdropFilter: 'blur(8px)', borderBottom: `1px solid ${darkMode ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.2)'}`, zIndex: 50 },
    navContent: { maxWidth: '1280px', margin: '0 auto', padding: '1rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
    logo: { display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' },
    logoIcon: { width: '43px', height: '43px', border: `2px solid ${darkMode ? '#fff' : '#000'}`, borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' },
    logoText: { fontSize: '1.5rem', fontWeight: 'bold' },
    navActions: { display: 'flex', alignItems: 'center', gap: '1rem' },
    themeToggle: { background: 'none', border: 'none', color: darkMode ? '#fff' : '#000', cursor: 'pointer', padding: '0.5rem', borderRadius: '8px', display: 'flex', alignItems: 'center' },
    backBtn: { backgroundColor: 'transparent', color: darkMode ? '#fff' : '#000', border: `2px solid ${darkMode ? '#fff' : '#000'}`, padding: '0.5rem 1rem', borderRadius: '8px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem' },
    main: { paddingTop: '5rem', paddingBottom: '3rem', maxWidth: '1100px', margin: '0 auto', padding: '5rem 1.5rem 3rem' },
    header: { marginTop: '2rem', textAlign: 'center' },
    dateInput: { display: 'inline-flex', alignItems: 'center', gap: '0.5rem', color: darkMode ? '#9ca3af' : '#666', marginBottom: '1rem', fontSize: '0.95rem', padding: '0.5rem 1rem', border: `1px solid ${darkMode ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.2)'}`, borderRadius: '20px', backgroundColor: 'transparent' },
    title: { fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 'bold', lineHeight: '1.2' },
    subtitle: { fontSize: '1.15rem', color: darkMode ? '#9ca3af' : '#666', maxWidth: '700px', margin: '0 auto 1.5rem', lineHeight: '1.6' },
    shareBtn: { backgroundColor: 'transparent', color: darkMode ? '#fff' : '#000', border: `2px solid ${darkMode ? '#fff' : '#000'}`, padding: '0.75rem 1.5rem', borderRadius: '8px', fontWeight: '600', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '0.5rem' },
    section: { marginBottom: '4rem' },
    sectionHeader: { display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '2rem', paddingBottom: '0.75rem', borderBottom: `2px solid ${darkMode ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.2)'}` },
    sectionTitle: { fontSize: '2rem', fontWeight: 'bold' },
    recapCard: { marginBottom: '2.5rem', padding: '2rem', border: `2px solid ${darkMode ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.2)'}`, borderRadius: '12px', transition: 'all 0.3s' },
    headline: { fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: darkMode ? '#fff' : '#000' },
    description: { color: darkMode ? '#d1d5db' : '#333', lineHeight: '1.6', marginBottom: '1.5rem' },
    statsGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))', gap: '1rem', marginBottom: '1.5rem' },
    statBox: { textAlign: 'center', padding: '1rem', backgroundColor: darkMode ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)', borderRadius: '8px' },
    statValue: { fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '0.25rem' },
    statLabel: { fontSize: '0.85rem', color: darkMode ? '#9ca3af' : '#666' },
    playerSection: { backgroundColor: darkMode ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)', padding: '1.25rem', borderRadius: '8px', borderLeft: `3px solid ${darkMode ? '#fff' : '#000'}` },
    playerTitle: { fontWeight: 'bold', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' },
    playerItem: { fontSize: '0.95rem', lineHeight: '1.6', color: darkMode ? '#d1d5db' : '#333', marginBottom: '0.5rem', paddingLeft: '0.5rem' },
    loading: { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '4rem', gap: '1rem' },
    footer: { borderTop: `1px solid ${darkMode ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.2)'}`, padding: '2rem 1.5rem', textAlign: 'center', alignItems: 'center', color: darkMode ? '#9ca3af' : '#666' },
    mediaContainer: {
      position: 'relative',
      paddingBottom: '56.25%', /* 16:9 Aspect Ratio (9 / 16 = 0.5625) */
      height: 0,
      overflow: 'hidden',
      borderRadius: '8px',
      marginTop: '16px',
      background: '#000', // Optional: looks better while loading
    },
    iframe: {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      border: 'none',
    },
    standingsContainer: { 
      display: 'grid', 
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
      gap: '2rem' 
    },
    confCard: { 
      padding: '1.5rem', 
      border: `2px solid ${darkMode ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.1)'}`, 
      borderRadius: '12px', 
      backgroundColor: darkMode ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.02)' 
    },
    confTitle: { 
      fontSize: '1.25rem', 
      fontWeight: 'bold', 
      marginBottom: '1rem', 
      borderBottom: `1px solid ${darkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`, 
      paddingBottom: '0.5rem' 
    },
    table: { width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' },
    th: { 
      textAlign: 'left', 
      padding: '0.5rem', 
      color: darkMode ? '#9ca3af' : '#666', 
      fontWeight: 'normal', 
      fontSize: '0.8rem' 
    },
    tr: { borderBottom: `1px solid ${darkMode ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)'}` },
    td: { padding: '0.75rem 0.5rem' },
    rankCell: { fontWeight: 'bold', width: '30px', color: darkMode ? '#6b7280' : '#9ca3af' },
    teamCell: { fontWeight: '600' },
    deltaCell: { textAlign: 'right', display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '4px' },
    deltaPos: { color: '#10b981' }, // Green for moving up
    deltaNeg: { color: '#ef4444' }, // Red for moving down
    deltaNeu: { color: darkMode ? '#4b5563' : '#9ca3af' }, // Grey for no change
    highlightNav: {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '1rem',
      marginTop: '1.5rem',
    }
  };

  return (
    <div style={s.container}>
      {/* Top-Level nav bar */}
      <nav style={s.nav}>
        <div style={s.navContent}>
          <div style={s.logo}>
            <div style={s.logoIcon}>
              {darkMode ? (<img src={MetrixLogoBlack} widht={40} height={40}></img>) : (<img src={MetrixLogoWhite} widht={40} height={40}></img>)}
            </div>
            <span style={s.logoText}>METRIX</span>
          </div>
          
          <div style={s.navActions}>
            <button 
              onClick={() => setDarkMode(!darkMode)}
              style={s.themeToggle}
            >
              {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>
            <button style={s.backBtn}>
              <ArrowLeft size={18} />
              Back to Home
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main style={s.main}>
        {/* Header */}
        <header style={s.header}>
          <div style={s.dateInput}>
            <Calendar size={16} />
            <span>{displayDate}</span>
          </div>
          <h1 style={s.title}>Around the Arc</h1>
          <p style={s.subtitle}>
            Daily recaps, insights, and updates from around the NBA, powered by Artifical Intelligence
          </p>
          <button style={s.shareBtn}>
            <Share2 size={16} />
            Share Newsletter
          </button>
        </header>

        {/* Recaps from Last Night */}
        <section style={s.section}>
          <div style={s.sectionHeader}>
            <Timer size={28} />
            <h2 style={s.sectionTitle}>Scoreboard</h2>
          </div>
          {/* FIX THIS CODE */}
          {summaries.map(game => {
              const players = game.key_player_descriptions;

              return (
                <div key={game.id} style={s.recapCard} onMouseEnter={(e) => { e.currentTarget.style.transform = 'translateY(-4px)'; e.currentTarget.style.boxShadow = darkMode ? '0 10px 40px rgba(255,255,255,0.1)' : '0 10px 40px rgba(0,0,0,0.1)'; }} onMouseLeave={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; }}>
                  <h3 style={s.headline}>{game.headline}</h3>
                  <p style={s.description}>{game.game_description}</p>
                  {players.length > 0 && (
                    <div style={s.playerSection}>
                      <div style={s.playerTitle}><Star size={16} />Key Performers</div>
                      {players.map((p, i) => <p key={i} style={s.playerItem}>{p}</p>)}
                    </div>
                  )}
                </div>
              );
            })
          }
        </section>

        {/* Highlights Section */}
        <section style={s.section}>
          <div style={s.sectionHeader}>
            {/* Left side: Icon + Title */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Star size={28} />
              <h2 style={s.sectionTitle}>Highlights</h2>
            </div>
          </div>

          {/* Single Card Render */}
          {currentHighlight && (
            <div 
              key={currentHighlight.id} 
              style={s.recapCard}
              onMouseEnter={(e) => { 
                e.currentTarget.style.transform = 'translateY(-4px)'; 
                e.currentTarget.style.boxShadow = darkMode ? '0 10px 40px rgba(255,255,255,0.1)' : '0 10px 40px rgba(0,0,0,0.1)'; 
              }} 
              onMouseLeave={(e) => { 
                e.currentTarget.style.transform = 'translateY(0)'; 
                e.currentTarget.style.boxShadow = 'none'; 
              }}
            >
              <h3 style={s.headline}>{currentHighlight.title}</h3>
              
              <div style={s.mediaContainer}>
                <iframe
                  style={s.iframe} 
                  src={currentHighlight.media.replace('streamable.com/', 'streamable.com/e/')} 
                  title={currentHighlight.title}
                  allowFullScreen
                />
              </div>
            </div>
          )}

            {/* Right side: Navigation Controls */}
            {highlights.length > 1 && (
              <div style={s.highlightNav}>
                <button onClick={prevHighlight} style={s.navButton}>
                  <ChevronLeft size={20} />
                </button>
                <span style={s.pageIndicator}>
                  {highlightIndex + 1} / {highlights.length}
                </span>
                <button onClick={nextHighlight} style={s.navButton}>
                  <ChevronRight size={20} />
                </button>
              </div>
            )}
        </section>

        {/* Stories */}
        <section style={s.section}>
          <div style={s.sectionHeader}>
            <Newspaper size={28} />
            <h2 style={s.sectionTitle}>Featured Stories</h2>
          </div>
          {newsStories.length > 0 ? (
            newsStories.map(story => (
              <div 
                key={story.id} 
                style={s.storyCard}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-4px)';
                  e.currentTarget.style.boxShadow = darkMode ? '0 10px 40px rgba(255, 255, 255, 0.1)' : '0 10px 40px rgba(0, 0, 0, 0.1)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                <h3 style={s.storyTitle}>{story.headline}</h3>
                <p style={s.storyExcerpt}>{story.story}</p>
              </div>
            ))
          ) : (
            <div
              style={s.storyCard}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.boxShadow = darkMode ? '0 10px 40px rgba(255, 255, 255, 0.1)' : '0 10px 40px rgba(0, 0, 0, 0.1)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              <h3 style={s.storyTitle}>No stories to report as of now.</h3>
              <p style={s.storyExceprt}>Metrix will be updated as news breaks around the NBA.</p>
            </div>
          )}
        </section>

        {/* Standings Section */}
        <section style={s.section}>
          <div style={s.sectionHeader}>
            <ChartNoAxesCombined size={28} />
            <h2 style={s.sectionTitle}>Conference Standings</h2>
          </div>
          
          <div style={s.standingsContainer}>
            {/* Helper function to render a single conference table */}
            {[
              { title: "Eastern Conference", data: eastStandings }, 
              { title: "Western Conference", data: westStandings }
            ].map((conf, index) => (
              <div key={index} style={s.confCard}>
                <h3 style={s.confTitle}>{conf.title}</h3>
                <table style={s.table}>
                  <thead>
                    <tr>
                      <th style={s.th}>#</th>
                      <th style={s.th}>Team</th>
                      <th style={{...s.th, textAlign: 'right'}}>Trend</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(conf.data || {})
                      // Convert object to array: [teamId, [delta, rank]]
                      // Then sort by Rank (the second item in the array)
                      .sort(([, a], [, b]) => a[1] - b[1])
                      .map(([teamId, [delta, rank]]) => {
                        const team = TEAMS[teamId] || { name: 'Unknown', abbr: 'UNK' };
                        
                        return (
                          <tr key={teamId} style={s.tr}>
                            <td style={{...s.td, ...s.rankCell}}>{rank}</td>
                            <td style={{...s.td, ...s.teamCell, display: 'flex', alignItems: 'center', gap: '8px'}}>
                              {/* NEW: Dynamic Logo Image */}
                              <img 
                                src={`https://cdn.nba.com/logos/nba/${teamId}/global/L/logo.svg`} 
                                alt={team.name}
                                style={{ width: '24px', height: '24px', objectFit: 'contain' }}
                              />
                              <div>
                                {team.name} 
                                <span style={{fontSize: '0.8em', opacity: 0.6, fontWeight: 'normal', marginLeft: '4px'}}>
                                  {team.abbr}
                                </span>
                              </div>
                            </td>
                            <td style={s.td}>
                              <div style={s.deltaCell}>
                                {delta > 0 && (
                                  <span style={s.deltaPos}>
                                    <TrendingUp size={14} /> +{delta}
                                  </span>
                                )}
                                {delta < 0 && (
                                  <span style={s.deltaNeg}>
                                    {/* Rotated arrow for down trend */}
                                    <TrendingUp size={14} style={{transform: 'scaleY(-1)'}} /> {delta}
                                  </span>
                                )}
                                {delta === 0 && (
                                  <span style={s.deltaNeu}>-</span>
                                )}
                              </div>
                            </td>
                          </tr>
                        );
                      })}
                  </tbody>
                </table>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer style={s.footer}>
        <div style={{...s.logoIcon, margin: '0 auto 0.5rem'}}>
          {darkMode ? (<img src={MetrixLogoBlack} widht={40} height={40}></img>) : (<img src={MetrixLogoWhite} widht={40} height={40}></img>)}
        </div>
        <p style={{marginBottom: '0.5rem', fontWeight: 'bold'}}>
          METRIX: Around the Arc
        </p>
        <p style={{marginTop: '1rem', fontSize: '0.9rem'}}>
          © 2025 Metrix. Elevating basketball through data.
        </p>
      </footer>
    </div>
  );
}