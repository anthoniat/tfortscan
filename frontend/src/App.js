import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import ScanPage from './pages/ScanPage';
import InfoSqlPage from './pages/InfoSqlPage';
import InfoXssPage from './pages/InfoXssPage';
import InfoHeadersPage from './pages/InfoHeadersPage';
// Import other info pages if needed

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="container mt-3"> {/* Add container for padding */}
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/scan" element={<ScanPage />} />
            {/* Info Pages Routes based on Figure 4 */}
            <Route path="/info/sql" element={<InfoSqlPage />} />
            <Route path="/info/xss" element={<InfoXssPage />} />
            <Route path="/info/headers" element={<InfoHeadersPage />} />
             {/* Add routes for Open Ports Scan page if separate */}
             {/* <Route path="/open-ports" element={<OpenPortsPage />} /> */}
            {/* Add a fallback route for unknown paths */}
            <Route path="*" element={<HomePage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;