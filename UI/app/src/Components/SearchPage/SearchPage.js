import axios from "axios";
import React, { Component } from "react";
import { Input } from "antd";
import ResultTable from "../ResultTable/ResultTable";
import "./SearchPage.css";

const { Search } = Input;

export default class SearchPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
    };
    this.tableElement = React.createRef();
  }

  loadRows = (query) => {
    axios.get("http://localhost:5000/results?q=" + query).then((res) => {
      this.setState({ data: res.data.results });
      this.tableElement.current.updateData(res.data.results);
    });
  };
  render() {
    return (
      <div>
        <div className="search-bar">
          <Search
            placeholder="input search text"
            onSearch={(value) => this.loadRows(value)}
            enterButton
          />
        </div>
        <ResultTable ref={this.tableElement} data={this.state.data} />
      </div>
    );
  }
}
