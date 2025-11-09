import React, { Component } from "react";
export default class SignUp extends Component {
  render() {
    return (
      <div className="form-wrapper">
        <div className="auth-wrapper">
          <div className="auth-inner">
            <form id="signup">
              <h3>Sign Up</h3>
              <div className="mb-3">
                <label>First name</label>
                <input
                  id="Fname"
                  type="text"
                  className="form-control"
                  placeholder="First name"
                />
              </div>
              <div className="mb-3">
                <label>Last name</label>
                <input
                  id="Lname"
                  type="text"
                  className="form-control"
                  placeholder="Last name"
                />
              </div>
              <div className="mb-3">
                <label>Email address</label>
                <input
                  id="email"
                  type="email"
                  className="form-control"
                  placeholder="Enter email"
                />
              </div>
              <div className="mb-3">
                <label>Password</label>
                <input
                  id="password"
                  type="password"
                  className="form-control"
                  placeholder="Enter password"
                />
              </div>
              <div className="d-grid">
                <button type="submit" className="btn btn-primary">
                  Sign Up
                </button>
              </div>
              <p className="forgot-password text-right">
                Already registered <a href="/sign-in">sign in?</a>
              </p>
            </form>
          </div>
        </div>
      </div>
    );
  }
}
