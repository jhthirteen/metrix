import React, { useState } from 'react';
import { BarChart3, TrendingUp, Mail, ArrowRight, Menu, X, Sun, Moon } from 'lucide-react';

export default function LandingPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  const handleSubmit = () => {
    if (email) {
      setSubmitted(true);
      setTimeout(() => {
        setSubmitted(false);
        setEmail('');
      }, 3000);
    }
  };

  const styles = {
    container: {
      minHeight: '100vh',
      width: '100%',
      backgroundColor: darkMode ? '#000' : '#fff',
      color: darkMode ? '#fff' : '#000',
      transition: 'all 0.3s ease',
      overflowX: 'hidden',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    },
    nav: {
      position: 'fixed',
      top: 0,
      width: '100%',
      backgroundColor: darkMode ? 'rgba(0, 0, 0, 0.95)' : 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(8px)',
      borderBottom: `1px solid ${darkMode ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.2)'}`,
      zIndex: 50
    },
    navContent: {
      maxWidth: '1280px',
      margin: '0 auto',
      padding: '1rem 1.5rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    },
    logo: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem'
    },
    logoIcon: {
      width: '40px',
      height: '40px',
      backgroundColor: 'transparent',
      border: `2px solid ${darkMode ? '#fff' : '#000'}`,
      borderRadius: '8px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    },
    logoText: {
      fontSize: '1.5rem',
      fontWeight: 'bold'
    },
    navMenu: {
      display: 'flex',
      alignItems: 'center',
      gap: '2rem'
    },
    navLinks: {
      display: 'flex',
      gap: '2rem'
    },
    navLink: {
      color: darkMode ? '#fff' : '#000',
      textDecoration: 'none',
      transition: 'color 0.3s',
      cursor: 'pointer'
    },
    themeToggle: {
      background: 'none',
      border: 'none',
      color: darkMode ? '#fff' : '#000',
      cursor: 'pointer',
      padding: '0.5rem',
      borderRadius: '8px',
      display: 'flex',
      alignItems: 'center',
      transition: 'background-color 0.3s'
    },
    btnPrimary: {
      backgroundColor: 'transparent',
      color: darkMode ? '#fff' : '#000',
      border: `2px solid ${darkMode ? '#fff' : '#000'}`,
      padding: '0.5rem 1.5rem',
      borderRadius: '8px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'all 0.3s'
    },
    hero: {
      paddingTop: '8rem',
      paddingBottom: '5rem',
      padding: '8rem 1.5rem 5rem'
    },
    heroContent: {
      maxWidth: '1280px',
      margin: '0 auto',
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
      gap: '3rem',
      alignItems: 'center',
      width: '100%'
    },
    heroTitle: {
      fontSize: 'clamp(2.5rem, 8vw, 4rem)',
      fontWeight: 'bold',
      marginBottom: '1.5rem',
      lineHeight: '1.1'
    },
    gradient: {
      backgroundImage: darkMode ? 'linear-gradient(to right, #fff, #888)' : 'linear-gradient(to right, #000, #888)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      MozBackgroundClip: 'text',
      MozTextFillColor: 'transparent',
      backgroundClip: 'text',
      color: 'transparent',
      display: 'inline-block'
    },
    heroText: {
      fontSize: '1.25rem',
      color: darkMode ? '#9ca3af' : '#666',
      marginBottom: '2rem',
      lineHeight: '1.8'
    },
    heroCTA: {
      display: 'flex',
      gap: '1rem',
      flexWrap: 'wrap'
    },
    btnSecondary: {
      border: `2px solid ${darkMode ? '#fff' : '#000'}`,
      backgroundColor: 'transparent',
      color: darkMode ? '#fff' : '#000',
      padding: '1rem 2rem',
      borderRadius: '8px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'all 0.3s'
    },
    btnLarge: {
      backgroundColor: 'transparent',
      color: darkMode ? '#fff' : '#000',
      border: `2px solid ${darkMode ? '#fff' : '#000'}`,
      padding: '1rem 2rem',
      borderRadius: '8px',
      fontWeight: '600',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '0.5rem',
      transition: 'all 0.3s'
    },
    heroImage: {
      aspectRatio: '1',
      background: darkMode ? 'linear-gradient(to bottom right, rgba(255, 255, 255, 0.1), transparent)' : 'linear-gradient(to bottom right, rgba(0, 0, 0, 0.1), transparent)',
      borderRadius: '1.5rem',
      border: `1px solid ${darkMode ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.2)'}`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    },
    section: {
      padding: '5rem 1.5rem'
    },
    sectionTitle: {
      fontSize: 'clamp(2rem, 6vw, 3rem)',
      fontWeight: 'bold',
      textAlign: 'center',
      marginBottom: '4rem'
    },
    featuresGrid: {
      maxWidth: '1280px',
      margin: '0 auto',
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
      gap: '2rem'
    },
    featureCard: {
      padding: '2rem',
      border: `2px solid ${darkMode ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.2)'}`,
      borderRadius: '1rem',
      transition: 'all 0.3s',
      cursor: 'pointer',
      transform: 'translateY(0)',
      boxShadow: 'none'
    },
    featureIcon: {
      width: '56px',
      height: '56px',
      backgroundColor: darkMode ? '#fff' : '#000',
      borderRadius: '12px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      marginBottom: '1.5rem',
      transition: 'all 0.3s'
    },
    featureTitle: {
      fontSize: '1.5rem',
      fontWeight: 'bold',
      marginBottom: '1rem'
    },
    featureText: {
      color: darkMode ? '#9ca3af' : '#666',
      transition: 'color 0.3s'
    },
    newsletterSection: {
      padding: '5rem 1.5rem',
      textAlign: 'center'
    },
    newsletterContent: {
      maxWidth: '56rem',
      margin: '0 auto'
    },
    newsletterForm: {
      maxWidth: '42rem',
      margin: '0 auto',
      display: 'flex',
      gap: '1rem',
      flexWrap: 'wrap'
    },
    input: {
      flex: 1,
      minWidth: '250px',
      padding: '1rem 1.5rem',
      borderRadius: '8px',
      backgroundColor: darkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)',
      border: `1px solid ${darkMode ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.2)'}`,
      color: darkMode ? '#fff' : '#000',
      fontSize: '1rem',
      outline: 'none',
      transition: 'border-color 0.3s'
    },
    successMessage: {
      marginTop: '1rem',
      color: '#4ade80',
      fontWeight: '600'
    },
    statsGrid: {
      maxWidth: '1280px',
      margin: '0 auto',
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '3rem',
      textAlign: 'center'
    },
    statNumber: {
      fontSize: '3rem',
      fontWeight: 'bold',
      marginBottom: '0.5rem'
    },
    statText: {
      color: darkMode ? '#9ca3af' : '#666'
    },
    aboutContent: {
      maxWidth: '56rem',
      margin: '0 auto',
      textAlign: 'center'
    },
    aboutText: {
      fontSize: '1.25rem',
      color: darkMode ? '#9ca3af' : '#666',
      lineHeight: '1.8'
    },
    footer: {
      borderTop: `1px solid ${darkMode ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.2)'}`,
      padding: '3rem 1.5rem'
    },
    footerContent: {
      maxWidth: '1280px',
      margin: '0 auto',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      flexWrap: 'wrap',
      gap: '1rem'
    },
    footerText: {
      color: darkMode ? '#9ca3af' : '#666'
    },
    mobileMenuBtn: {
      display: 'none',
      background: 'none',
      border: 'none',
      color: darkMode ? '#fff' : '#000',
      cursor: 'pointer',
      padding: '0.5rem'
    },
    mobileMenu: {
      display: 'none',
      paddingTop: '1rem',
      paddingBottom: '0.5rem'
    },
    mobileMenuActive: {
      display: 'block'
    },
    mobileMenuLink: {
      display: 'block',
      color: darkMode ? '#fff' : '#000',
      textDecoration: 'none',
      padding: '0.5rem 0',
      cursor: 'pointer'
    }
  };

  return (
    <div style={styles.container}>
      {/* Navigation */}
      <nav style={styles.nav}>
        <div style={styles.navContent}>
          <div style={styles.logo}>
            <div style={styles.logoIcon}>
              <BarChart3 size={24} color={darkMode ? '#fff' : '#000'} />
            </div>
            <span style={styles.logoText}>METRIX</span>
          </div>
          
          <div style={{...styles.navMenu, display: window.innerWidth < 768 ? 'none' : 'flex'}}>
            <div style={styles.navLinks}>
              <a href="#features" style={styles.navLink}>Features</a>
              <a href="#newsletter" style={styles.navLink}>Newsletter</a>
              <a href="#about" style={styles.navLink}>About</a>
            </div>
            <button 
              onClick={() => setDarkMode(!darkMode)}
              style={styles.themeToggle}
            >
              {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>
            <button style={styles.btnPrimary}>
              Get Started
            </button>
          </div>

          <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <button 
              onClick={() => setDarkMode(!darkMode)}
              style={{...styles.themeToggle, display: window.innerWidth >= 768 ? 'none' : 'flex'}}
            >
              {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>
            <button 
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              style={{...styles.mobileMenuBtn, display: window.innerWidth >= 768 ? 'none' : 'block'}}
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div style={{...styles.mobileMenu, ...styles.mobileMenuActive, padding: '1rem 1.5rem'}}>
            <a href="#features" style={styles.mobileMenuLink}>Features</a>
            <a href="#newsletter" style={styles.mobileMenuLink}>Newsletter</a>
            <a href="#about" style={styles.mobileMenuLink}>About</a>
            <button style={{...styles.btnPrimary, width: '100%', marginTop: '1rem'}}>
              Get Started
            </button>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section style={styles.hero}>
        <div style={styles.heroContent}>
          <div>
            <h1 style={styles.heroTitle}>
              Where Basketball
              <br />
              <span style={styles.gradient}>
                Meets Data
              </span>
            </h1>
            <p style={styles.heroText}>
              Unlock the power of machine learning and advanced analytics to transform how you understand basketball.
            </p>
            <div style={styles.heroCTA}>
              <button style={styles.btnLarge}>
                Start Free Trial
                <ArrowRight size={20} />
              </button>
              <button style={styles.btnSecondary}>
                Watch Demo
              </button>
            </div>
          </div>
          <div style={styles.heroImage}>
            <img 
              src={`data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='100' cy='100' r='90' fill='none' stroke='${darkMode ? 'white' : 'black'}' stroke-width='2'/%3E%3Cpath d='M100 10 Q150 100 100 190' fill='none' stroke='${darkMode ? 'white' : 'black'}' stroke-width='2'/%3E%3Cpath d='M100 10 Q50 100 100 190' fill='none' stroke='${darkMode ? 'white' : 'black'}' stroke-width='2'/%3E%3Cline x1='30' y1='100' x2='170' y2='100' stroke='${darkMode ? 'white' : 'black'}' stroke-width='2'/%3E%3Crect x='140' y='60' width='10' height='30' fill='${darkMode ? 'white' : 'black'}'/%3E%3Crect x='140' y='110' width='10' height='50' fill='${darkMode ? 'white' : 'black'}'/%3E%3Crect x='155' y='80' width='10' height='40' fill='${darkMode ? 'white' : 'black'}'/%3E%3C/svg%3E`}
              alt="Basketball Analytics"
              style={{width: '256px', height: '256px', opacity: 0.8}}
            />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" style={styles.section}>
        <h2 style={styles.sectionTitle}>Powerful Features</h2>
        <div style={styles.featuresGrid}>
          <div 
            style={styles.featureCard}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-8px)';
              e.currentTarget.style.boxShadow = darkMode ? '0 10px 40px rgba(255, 255, 255, 0.1)' : '0 10px 40px rgba(0, 0, 0, 0.1)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div className="feature-icon" style={styles.featureIcon}>
              <BarChart3 size={32} color={darkMode ? '#000' : '#fff'} />
            </div>
            <h3 style={styles.featureTitle}>Analytics Engine</h3>
            <p className="feature-text" style={styles.featureText}>
              Deep dive into player performance, team dynamics, and game-changing insights powered by advanced ML models.
            </p>
          </div>

          <div 
            style={styles.featureCard}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-8px)';
              e.currentTarget.style.boxShadow = darkMode ? '0 10px 40px rgba(255, 255, 255, 0.1)' : '0 10px 40px rgba(0, 0, 0, 0.1)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div className="feature-icon" style={styles.featureIcon}>
              <TrendingUp size={32} color={darkMode ? '#000' : '#fff'} />
            </div>
            <h3 style={styles.featureTitle}>Predictive Models</h3>
            <p className="feature-text" style={styles.featureText}>
              Leverage cutting-edge machine learning to forecast outcomes, identify trends, and gain competitive advantage.
            </p>
          </div>

          <div 
            style={styles.featureCard}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-8px)';
              e.currentTarget.style.boxShadow = darkMode ? '0 10px 40px rgba(255, 255, 255, 0.1)' : '0 10px 40px rgba(0, 0, 0, 0.1)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div className="feature-icon" style={styles.featureIcon}>
              <Mail size={32} color={darkMode ? '#000' : '#fff'} />
            </div>
            <h3 style={styles.featureTitle}>Daily Newsletter</h3>
            <p className="feature-text" style={styles.featureText}>
              Get curated insights, analysis, and predictions delivered to your inbox every morning.
            </p>
          </div>
        </div>
      </section>

      {/* Newsletter Signup Section */}
      <section id="newsletter" style={styles.newsletterSection}>
        <div style={styles.newsletterContent}>
          <h2 style={styles.sectionTitle}>Join the Metrix Community</h2>
          <p style={{...styles.heroText, textAlign: 'center'}}>
            Get daily insights, analysis, and predictions straight to your inbox.
          </p>
          
          <div style={styles.newsletterForm}>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              style={styles.input}
            />
            <button
              onClick={handleSubmit}
              style={{...styles.btnLarge, whiteSpace: 'nowrap'}}
            >
              Subscribe Free
            </button>
          </div>
          {submitted && (
            <p style={styles.successMessage}>
              ✓ Thanks for subscribing! Check your inbox.
            </p>
          )}
        </div>
      </section>

      {/* Stats Section */}
      <section style={styles.section}>
        <div style={styles.statsGrid}>
          <div>
            <div style={styles.statNumber}>10K+</div>
            <div style={styles.statText}>Data Points Analyzed Daily</div>
          </div>
          <div>
            <div style={styles.statNumber}>98%</div>
            <div style={styles.statText}>Prediction Accuracy</div>
          </div>
          <div>
            <div style={styles.statNumber}>5K+</div>
            <div style={styles.statText}>Active Users</div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" style={styles.section}>
        <div style={styles.aboutContent}>
          <h2 style={styles.sectionTitle}>
            The Future of Basketball Analytics
          </h2>
          <p style={styles.aboutText}>
            Metrix combines the passion of basketball with the precision of data science. 
            Our platform empowers teams, analysts, and fans to make smarter decisions through 
            advanced machine learning models and intuitive analytics tools.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer style={styles.footer}>
        <div style={styles.footerContent}>
          <div style={styles.logo}>
            <div style={{...styles.logoIcon, width: '32px', height: '32px'}}>
              <BarChart3 size={20} color={darkMode ? '#fff' : '#000'} />
            </div>
            <span style={{fontSize: '1.25rem', fontWeight: 'bold'}}>METRIX</span>
          </div>
          <div style={styles.footerText}>
            © 2025 Metrix. Elevating basketball through data.
          </div>
        </div>
      </footer>
    </div>
  );
}