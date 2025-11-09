import React, { useState ,useEffect} from 'react';
import Sidebar from './components/sidebar.component';
import Home from './Home';

function Account() {
  const [toggle, setToggle] = useState(true);
  const [data, setData] = useState(null);
  const [section, setSection] = useState("accounts");
  useEffect(() => {
    fetch("data.json") // Load data from the JSON file
      .then(response => response.json())
      .then(json => setData(json.accounts))  // Assuming data.json has a 'users' key
      .catch(error => console.error("Error loading data:", error));
  }, []);

  const Toggle = () => {
    setToggle(!toggle);
  };

  return (
    <div className="container-fluid bg-secondary min-vh-100">
      <div className="row">
        {/* Conditionally render Sidebar based on toggle state */}
        {toggle && (
          <div className="col-4 col-md-2 bg-white vh-100 position-fixed">
            <Sidebar />
          </div>
        )}
        {toggle && (
          <div className="col-4 col-md-2">  
          </div>
        )}


        {/* Main content area */}
        <div className="col">
          <Home Toggle={Toggle}  Title="Accounts Information" 
            data={data}/>
        </div>
      </div>
    </div>
  );
}

export default Account;
