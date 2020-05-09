import "antd/dist/antd.css";
import React from "react";
import "./App.css";
import ResultTable from "./Components/ResultTable/ResultTable";
import SearchBar from "./Components/SearchBar/SearchBar";
import NavBar from "./Components/NavBar/NavBar";

function App() {
  return (
    <div className="App">
      <NavBar />
      <SearchBar />
      <ResultTable />
    </div>
  );
}

export default App;
