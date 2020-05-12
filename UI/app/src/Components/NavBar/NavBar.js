import React, { Component } from "react";
import { Layout, Typography, Menu } from "antd";
import "./NavBar.css";

const { Header } = Layout;
const { Title } = Typography;
export default class NavBar extends Component {
  render() {
    return (
      <div>
        <Header
          style={{
            zIndex: 1,
            width: "100%",
          }}
        >
          <div className="logo">
            <Title style={{ color: "#fff", cursor: "pointer" }}>
              AutoTagger
            </Title>
          </div>
          <Menu
            theme="dark"
            mode="horizontal"
            style={{ float: "right", marginRight: 24 }}
            defaultSelectedKeys={["1"]}
          >
            <Menu.Item key="1" onClick={this.props.onClickExtract}>
              {this.props.itemName}
            </Menu.Item>
          </Menu>
        </Header>
      </div>
    );
  }
}
