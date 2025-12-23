

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  return (
    <Router>
      <header className="App-header">
        <img src="/logo192.png" alt="OctofitApp Logo" className="App-logo" />
        <span style={{ fontWeight: 700, fontSize: '2rem', letterSpacing: '1px', marginRight: '32px' }}>Octofit Tracker</span>
        <nav className="nav-menu">
          <Link className="App-link" to="/activities">Activities</Link>
          <Link className="App-link" to="/leaderboard">Leaderboard</Link>
          <Link className="App-link" to="/teams">Teams</Link>
          <Link className="App-link" to="/users">Users</Link>
          <Link className="App-link" to="/workouts">Workouts</Link>
        </nav>
      </header>
      <div className="container">
        <Routes>
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/users" element={<Users />} />
          <Route path="/workouts" element={<Workouts />} />
          <Route path="/" element={
            <div style={{ marginTop: '48px' }}>
              <h1>Welcome to Octofit Tracker!</h1>
              <p>Track your fitness, join teams, and compete on the leaderboard.</p>
              <Link className="btn" to="/activities">Get Started</Link>
            </div>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
