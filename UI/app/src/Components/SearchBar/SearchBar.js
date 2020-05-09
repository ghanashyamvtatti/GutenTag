import React, { Component } from "react";
import { Input } from "antd";
import "./SearchBar.css";

const { Search } = Input;

export default class SearchBar extends Component {
  render() {
    return (
      <div className="search-bar">
        <Search
          placeholder="input search text"
          onSearch={(value) => console.log(value)}
          enterButton
        />
      </div>
    );
  }
}
