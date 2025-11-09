import React from "react";
import { Table } from "react-bootstrap";
import Nav from "./Nav";

function Home({ Toggle, Title, data }) {
  // Directly set data without fetching or loading state
  console.log(data);
  console.log(Title);

  const renderTable = () => {
    if (!data) {
      return (
        <div className="text-center">
          <p>Loading...</p>
        </div>
      ); // Show loading message while data is being fetched
    }

    const tableConfigs = {
      "Users Information": {
        caption: "List of Users",
        headers: ["#", "Name", "Email", "Password"],
        keys: ["id", "name", "email", "password"]
      },
      "Accounts Information": {
        caption: "List of Accounts",
        headers: ["#", "Account Number", "Balance", "Account Type"],
        keys: ["id", "accountNumber", "balance", "accountType"]
      },
      "Transactions Information": {
        caption: "List of Transactions",
        headers: ["#", "Transaction ID", "Amount", "Transaction Type"],
        keys: ["id", "transactionId", "amount", "transactionType"]
      }
    };

    const config = tableConfigs[Title];

    if (!config) {
      return null; // Return null if no matching title configuration is found
    }

    return (
      <Table className="table caption-top rounded mt-2" striped>
        <caption className="text-white fs-4">{config.caption}</caption>
        <thead>
          <tr>
            {config.headers.map((header, index) => (
              <th key={index}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr>
              <td colSpan={config.headers.length}>No data available</td>
            </tr>
          ) : (
            data.map((item) => (
              <tr key={item.id}>
                {config.keys.map((key, index) => (
                  <td key={index}>{item[key]}</td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </Table>
    );
  };

  return (
    <div className="px-3">
      <Nav Toggle={Toggle} />
      <div className="container-fluid">
        <div className="row g-3 my-2">
          {/* Example of other UI elements */}
          {[...Array(4)].map((_, index) => (
            <div className="col-md-3 p-1" key={index}>
              <div className="p-3 bg-white shadow-sm d-flex justify-content-around align-items-center rounded">
                <div>
                  <h3 className="fs-2">230</h3>
                  <p className="fs-5">Total</p>
                </div>
                <i className="bi bi-activity p-3 fs-1"></i>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Render the appropriate table based on Title */}
      {renderTable()}
    </div>
  );
}

export default Home;
