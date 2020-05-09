import React, { Component } from "react";
import { Layout, Typography } from "antd";

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
        </Header>
      </div>
    );
  }
}
