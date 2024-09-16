import WishCardPublic from '../components/WishCardPublic.jsx';

import { useNavigate } from "react-router-dom";

import axios from 'axios';
import React, { useEffect, useState } from 'react';
import {
  LogoutOutlined,
  UserOutlined,
  HomeOutlined,
} from '@ant-design/icons';
import { Breadcrumb, Layout, Menu, theme, Pagination } from 'antd';
const { Content, Footer, Sider } = Layout;
function getItem(label, key, icon, children) {
  return {
    key,
    icon,
    children,
    label,
  };
}

const WishlistPage = () => {

  const navigate = useNavigate();

  const [wishes, setWishes] = useState([])

  const fetchWishes = (number, userId) => {
    axios.get(`http://127.0.0.1:8000/wishes/${userId}`,
      {
        params: {
          offset: number
        }
      }
    ).then(r => {
      const wishResponse = r.data
    setWishes(wishResponse)
    })
  }

  const [pages, setPages] = useState(0)

  const fetchPages = (userId) => {
    axios.get(`http://127.0.0.1:8000/wishes/private-pagination/${userId}`,
    ).then(p => {
      const pageResponse = p.data
      setPages(pageResponse)
    })
  }

  const [userData, setuserData] = useState([])

  const fetchUserData = (userId, token) => {
    axios.get(`http://127.0.0.1:8000/users/${userId}`,
      {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
          
        }
      }
    ).then(p => {
      const userResponse = p.data
      setuserData(userResponse)
    })
  }

  const [items, setItems] = useState([])

  const AuthenticateUser = (token) => {
    axios.get('http://127.0.0.1:8000/users/me',
      {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
          
        }
    }).then(r => {

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

      const userId = window.location.href.split('/')[4]

      fetchUserData(userId, token)

      fetchWishes(0, userId)

      fetchPages(userId);
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

  function OnChange (page) {
    // fetchWishes((page-1)*5, userData.id)
    console.log(window.location.href.split('/')[4])
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
        <Menu theme="dark" defaultSelectedKeys={['4']} mode="inline" items={items} />
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
            <Breadcrumb.Item>{userData.username}</Breadcrumb.Item>
            <Breadcrumb.Item>Wishlist</Breadcrumb.Item>
          </Breadcrumb>
          
          {wishes.map((item) => (
            <div
            style={{
              margin: '16px 0',  
              padding: 24,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
            >
            <WishCardPublic 
              id={item.id}
              name={item.name}
              link={item.link}
              image_src={item.picture_src}
            />
            </div>
          ))}
        </Content>

        <Pagination
          style={{
            justifyContent: 'center'
          }}
          defaultCurrent={1}
          total={pages} 
          onChange={OnChange}
        />

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
export default WishlistPage;