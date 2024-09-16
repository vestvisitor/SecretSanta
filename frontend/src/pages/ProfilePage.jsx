import axios from 'axios';
import { useNavigate } from "react-router-dom";
import React, { useState, useEffect } from 'react';
import {
  LogoutOutlined,
  UserOutlined,
  HomeOutlined,
} from '@ant-design/icons';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
const { Content, Footer, Sider } = Layout;
function getItem(label, key, icon, children) {
  return {
    key,
    icon,
    children,
    label,
  };
}

const ProfilePage = () => {

  const navigate = useNavigate();

  const [userData, setuserData] = useState([])

  const [items, setItems] = useState([])

  const AuthenticateUser = (token) => {
    axios.get('http://127.0.0.1:8000/users/me',
      {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
          
        }
    }).then(r => {
      const Response = r.data
      console.log(Response);
      setuserData(Response)

      const items = [
        getItem(<a href='/'>Home page</a>, '1', <HomeOutlined />),
        getItem('User', 'sub1', <UserOutlined />, [
          getItem(<a href='/#profile'>My profile</a>, '3'),
          getItem(<a href='/#my-wishlist'>My wishlist</a>, '4'),
          getItem(<a href='/#make-wish'>Make wish</a>, '5'),
        ]),
        getItem('Logout', '6', <LogoutOutlined />),
      ];

      setItems(items);

    })
    .catch(function (error) {
      console.log(error);
      navigate('/login');
    });
  }

  useEffect(() => {
    const access_token = localStorage.getItem('access_token');
    AuthenticateUser(access_token);
  }, []);

  const [collapsed, setCollapsed] = useState(true);
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  return (
    <Layout
      style={{
        minHeight: '100vh',
      }}
    >
      <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
        <div className="demo-logo-vertical" />
        <Menu theme="dark" defaultSelectedKeys={['3']} mode="inline" items={items} />
      </Sider>
      <Layout>
        <Content
          style={{
            margin: '0 16px',
          }}
        >
        <Breadcrumb
            style={{
              margin: '16px 0',
            }}
          >
            <Breadcrumb.Item>User</Breadcrumb.Item>
            <Breadcrumb.Item>Profile</Breadcrumb.Item>
          </Breadcrumb>
          <div
            style={{
              margin: '16px 0',  
              padding: 24,
              minHeight: 360,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <h2>Username:</h2><p>{userData.username}</p>
            <h2>Email:</h2><p>{userData.email}</p>
          </div>
        </Content>
        <Footer
          style={{
            textAlign: 'center',
          }}
        >
          ©{new Date().getFullYear()} Created by vestvisitor
        </Footer>
      </Layout>
    </Layout>
  );
};
export default ProfilePage;