import axios from 'axios';
import React, { useEffect, useState } from 'react';
import {
  HomeOutlined,
  UserOutlined,
  LogoutOutlined
} from '@ant-design/icons';
import { Layout, Menu, theme } from 'antd';
const { Header, Content, Footer, Sider } = Layout;
const siderStyle = {
  overflow: 'auto',
  height: '100vh',
  position: 'fixed',
  insetInlineStart: 0,
  top: 0,
  bottom: 0,
  scrollbarWidth: 'thin',
  scrollbarColor: 'unset',
};
function getItem(label, key, icon, children) {
  return {
    key,
    icon,
    children,
    label,
  };
}
const items = [
  getItem('Home', '1', <HomeOutlined />),
  getItem('Profile', '2', <UserOutlined />),
  getItem('Logout', '3', <LogoutOutlined />),
];
const MainMenu = () => {

  const [wishes, setWishes] = useState([])

  const fetchWishes = () => {
    axios.get('http://127.0.0.1:8000/wishes').then(r => {
      const wishResponse = r.data
      const menuWishes = [
        getItem("Wishes", "1", null, 
          wishResponse.map(w => {
            return {label: w.name, link: w.link}
          }))
      ]
      setWishes(menu)
    })
  }

  useEffect(() => {
    fetchWishes()
  }, []);

  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  return (
    <Layout hasSider>
      <Sider style={siderStyle} collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}> 
        <div className="demo-logo-vertical" />
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['4']} items={items} />
      </Sider>
      <Layout
        style={{
          marginInlineStart: 200,
        }}
      >
        <Content
          style={{
            margin: '24px 16px 0',
            overflow: 'initial',
          }}
        >
          <div
            style={{
              padding: 24,
              textAlign: 'center',
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <p>long content</p>

          </div>
        </Content>
        <Footer
          style={{
            textAlign: 'center',
          }}
        >
          Ant Design ©{new Date().getFullYear()} Created by Ant UED
        </Footer>
      </Layout>
    </Layout>
  );
};
export default MainMenu;
