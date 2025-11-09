import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  // You can use state here if needed, for example for form inputs
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(""); // Track error message
  const navigate = useNavigate(); // Hook for navigation

  // Simulated login function (replace with real authentication logic)
  const handleLogin = (e) => {
    e.preventDefault();

    // Dummy credentials check
    if (email === "admin@techno.com" && password === "admin123") {
      // Redirect to admin panel on successful login
      navigate("/admin/dashboard");
    } else {
      setError("Invalid credentials, please try again.");
    }
  };

  return (
    <div className="form-wrapper">
      <div className="auth-wrapper">
        <div className="auth-inner">
          <form id="login" onSubmit={handleLogin}>
            <h3>Sign In</h3>
            {error && <div className="alert alert-danger">{error}</div>}{" "}
            {/* Display error message */}
            <div className="mb-3">
              <label>Email address</label>
              <input
                id="email"
                type="email"
                className="form-control"
                placeholder="Enter email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="mb-3">
              <label>Password</label>
              <input
                id="password"
                type="password"
                className="form-control"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="mb-3">
              <div className="custom-control custom-checkbox">
                <input
                  type="checkbox"
                  className="custom-control-input"
                  id="customCheck1"
                />
                <label className="custom-control-label" htmlFor="customCheck1">
                  Remember me
                </label>
              </div>
            </div>
            <div className="d-grid">
              <button type="submit" className="btn btn-primary">
                Submit
              </button>
            </div>
            <p className="forgot-password text-right">
              Forgot <a href="#">password?</a>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
