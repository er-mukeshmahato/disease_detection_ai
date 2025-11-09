import React, { useState, useEffect } from "react";
import Sidebar from "./components/sidebar.component";
import UploadImage from "./components/uploadimage.component";

function Predict() {
  const [toggle, setToggle] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("data.json")
      .then((res) => res.json())
      .then((json) => setData(json.users))
      .catch((err) => console.error(err));
  }, []);

  const Toggle = () => setToggle(!toggle);

  return (
    <div className="container-fluid bg-secondary min-vh-100">
      <div className="row">
        {toggle && (
          <div className="col-4 col-md-2 bg-white vh-100 position-fixed">
            <Sidebar />
          </div>
        )}
        {toggle && <div className="col-4 col-md-2"></div>}

        <div className="col p-4 predict-main-div">
          <h2 className="text-white mb-3">Image Upload For Prediction</h2>
          <UploadImage />
        </div>
      </div>
    </div>
  );
}

export default Predict;
