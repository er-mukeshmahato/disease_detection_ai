import React from "react";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter as Router, Routes, Route, Link, useLocation  } from "react-router-dom";
import Login from "./components/login.component";
import SignUp from "./components/signup.component";
import Home from "./components/home.commonent";
import Dashboard from "./Dashboard";
import User from "./User";
import Report from "./Report";
import Account from "./Account";
import Predict from "./Predict";


Predict
function App() {
  const location = useLocation(); // Get current location

  // Check if the URL contains '/admin' and decide whether to render the navbar
  const isAdminPage = location.pathname.startsWith("/admin");

  return (
    <div className="App">
      {/* Render Navbar only if the path does not start with '/admin' */}
      {!isAdminPage && (
        <nav className="navbar navbar-expand-lg navbar-light fixed-top">
          <div className="container">
            <Link className="navbar-brand" to={"/home"}>
              Techno
            </Link>
            <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
              <ul className="navbar-nav ml-auto">
                <li className="nav-item">
                  <Link className="nav-link" to={"/login"}>
                    Login
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to={"/home"}>
                    Home
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to={"/sign-up"}>
                    Sign up
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>
      )}

      <div className="page">
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/sign-up" element={<SignUp />} />
          
          {/* Admin routes */}
          <Route path="/admin/dashboard" element={<Dashboard />} />
          <Route path="/admin/user-page" element={<User />} />
          <Route path="/admin/predict" element={<Predict />} />
          <Route path="/admin/report" element={<Report />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
