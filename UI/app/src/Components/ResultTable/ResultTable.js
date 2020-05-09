import { Table, Tag } from "antd";
import React, { Component } from "react";
import "./ResultTable.css";

export default class ResultTable extends Component {
  constructor(props) {
    super(props);
    this.state = { data: [] };
  }

  async loadRows() {
    fetch("http://localhost:5000/results").then((res) =>
      res.json().then((resp) => {
        this.setState({ data: resp.results });
      })
    );
  }

  componentDidMount() {
    this.loadRows();
  }

  render() {
    const columns = [
      {
        title: "url",
        dataIndex: "url",
        key: "url",
        render: (text) => <a href={text}>{text}</a>,
      },
      {
        title: "Tags",
        key: "tags",
        dataIndex: "tags",
        render: (tags) => (
          <>
            {tags.map((tag) => {
              let color = "geekblue";
              return (
                <Tag color={color} key={tag}>
                  {tag.toUpperCase()}
                </Tag>
              );
            })}
          </>
        ),
      },
    ];
    return (
      <div>
        <Table
          className="result-table"
          columns={columns}
          dataSource={this.state.data}
        />
      </div>
    );
  }
}
