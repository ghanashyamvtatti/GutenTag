import { Table, Tag } from "antd";
import React, { Component } from "react";
import "./ResultTable.css";

export default class ResultTable extends Component {
  constructor(props) {
    super(props);
    this.state = { data: props.data };
  }

  updateData = (data) => {
    this.setState({ data: data });
  };

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
        key: "vocab",
        dataIndex: "vocab",
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
      {
        title: "sentiment",
        dataIndex: "sentiment",
        key: "sentiment",
        render: (sentiment) => (
          <>
            <Tag
              color={sentiment === "positive" ? "green" : "red"}
              key={sentiment}
            >
              {sentiment.toUpperCase()}
            </Tag>
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
          scroll={{ y: 400 }}
        />
      </div>
    );
  }
}
