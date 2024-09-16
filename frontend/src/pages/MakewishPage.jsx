import MakeWishCard from "../components/MakeWishCard.jsx"

import axios from 'axios';
import { useNavigate } from "react-router-dom";
import React, { useState, useEffect } from 'react';
import {
  LogoutOutlined,
  UserOutlined,
  HomeOutlined,
} from '@ant-design/icons';
import { Breadcrumb, Layout, Menu, theme, Input, Rate } from 'antd';

const { Search } = Input;

const { Content, Footer, Sider } = Layout;
function getItem(label, key, icon, children) {
  return {
    key,
    icon,
    children,
    label,
  };
}

const AddwishPage = () => {

  const navigate = useNavigate();

  const [userData, setUserdata] = useState([]);

  const [items, setItems] = useState([])

  const AuthenticateUser = (token) => {
    axios.get('http://127.0.0.1:8000/users/me',
      {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
          
        }
    }).then(r => {
      setUserdata(r.data)
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

  const [wishdata, setWishData] = useState()

  const postWish = (token, obj) => {
    axios.post('http://127.0.0.1:8000/wishes/make',
      obj,
      {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
          
        }
      }
    ).then(w => {
      const linkResponse = w.data
      setWishData(linkResponse)
      navigate('/wishlist');
    })
    .catch(function (error) {
      console.log(error);
      navigate('/');
    });
  }
  
  function onSearch (value) {
    const obj = {link: value, priority: stars}
    const access_token = localStorage.getItem('access_token');
    postWish(access_token, obj)
  }
  
  const [stars, setStars] = useState()

  function onChange (star) {
    setStars(star);
  }

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
        <Menu theme="dark" defaultSelectedKeys={['5']} mode="inline" items={items} />
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
            <Breadcrumb.Item>Make wish</Breadcrumb.Item>
          </Breadcrumb>
          <div
            style={{
              alignContent: 'center',
              margin: '16px 0',  
              padding: 24,
              minHeight: 260,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <h1
              style={{
                textAlign: 'center'
              }}
            >Write down your wish!</h1>
            
            <p>Choose priority:</p>
            <Rate
            style={{
              padding: 1
            }}
              allowClear={false}
              defaultValue={1}
              onChange={onChange}
            />  

            <Search
            style={{
              padding: 10
            }}
              placeholder="input the wish link"
              enterButton="Make"
              size="large"
              onSearch={onSearch}
            />
                           
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
export default AddwishPage;