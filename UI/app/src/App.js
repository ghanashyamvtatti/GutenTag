import "antd/dist/antd.css";
import React, { Component } from "react";
import "./App.css";
import ExtractPage from "./Components/ExtractPage/ExtractPage";
import NavBar from "./Components/NavBar/NavBar";
import SearchPage from "./Components/SearchPage/SearchPage";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      showExtract: false,
      menuItem: "Extract",
    };
  }

  toggleExtract = () => {
    let currentState = this.state.showExtract;
    this.setState({
      showExtract: !currentState,
      menuItem: currentState ? "Extract" : "Search",
    });
  };

  render() {
    return (
      <div className="App">
        <NavBar
          itemName={this.state.menuItem}
          onClickExtract={this.toggleExtract}
        />
        <div className={this.state.showExtract ? "" : "hide"}>
          <ExtractPage />
        </div>
        <div className={this.state.showExtract ? "hide" : ""}>
          <SearchPage />
        </div>
      </div>
    );
  }
}
