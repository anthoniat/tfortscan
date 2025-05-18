import React from 'react';
import { Link, NavLink } from 'react-router-dom';

function Navbar() {
  // Simple bootstrap navbar
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">Tonia Vuln Scanner</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <NavLink className={({ isActive }) => isActive ? "nav-link active" : "nav-link"} aria-current="page" to="/">Home</NavLink>
            </li>
            <li className="nav-item">
              <NavLink className={({ isActive }) => isActive ? "nav-link active" : "nav-link"} to="/scan">Scan Website</NavLink>
            </li>
             {/* Link for Open Ports (can be combined with ScanPage results) */}
            {/* <li className="nav-item">
              <NavLink className={({ isActive }) => isActive ? "nav-link active" : "nav-link"} to="/scan">Open Ports</NavLink>
            </li> */}
          </ul>
          {/* Optional: Links to info pages in dropdown or separate menu */}
           <ul className="navbar-nav">
             <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" href="#" id="navbarDropdownInfoLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Vulnerability Info
                </a>
                <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdownInfoLink">
                    <li><Link className="dropdown-item" to="/info/sql">SQL Injection</Link></li>
                    <li><Link className="dropdown-item" to="/info/xss">XSS</Link></li>
                    <li><Link className="dropdown-item" to="/info/headers">Security Headers</Link></li>
                </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;