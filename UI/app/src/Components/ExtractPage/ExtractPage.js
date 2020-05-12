import axios from "axios";
import React, { Component } from "react";
import SearchBar from "../SearchBar/SearchBar";
import "./ExtractPage.css";

export default class ExtractPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      status: "READY",
      query: "",
      count: 0,
    };
    this.pollForStatus = this.pollForStatus.bind(this);
  }

  async pollForStatus() {
    console.log(this);
    const res = await axios.get("http://localhost:5000/status");
    console.log(res);
    if (res.data.status !== "READY") {
      // Update status
      this.setState({ status: res.data.status });
      if ("count" in res.data) {
        this.setState({ count: res.data.count });
      }
      setTimeout(this.pollForStatus, 5000);
    } else {
      this.setState({
        status: "READY",
        query: "",
        count: 0,
      });
    }
  }

  beginExtraction = (query) => {
    axios.get("http://localhost:5000/extract?q=" + query).then((res) => {
      // Start polling
      this.pollForStatus();
    });
  };

  onSearch = (query) => {
    this.setState({ query: query });
    this.beginExtraction(query);
  };

  render() {
    return (
      <div>
        <SearchBar onSearch={this.onSearch} />
        <div className="status">
          <h3>Current Status: {this.state.status}</h3>
          <h3>Remaining Count: {this.state.count}</h3>
        </div>
      </div>
    );
  }
}
