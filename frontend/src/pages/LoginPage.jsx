import axios from 'axios';
import { Layout, theme, Flex } from 'antd';
import LoginForm from '../components/LoginForm.jsx'
import { useNavigate } from "react-router-dom";
import React, { useEffect } from 'react';

const { Content, Footer } = Layout;

const LoginPage = () => {

  const navigate = useNavigate();

  const AuthenticateUser = (token) => {
    axios.get('http://127.0.0.1:8000/users/me',
      {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
          
        }
    }).then(r => {
      navigate('/');

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

  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  
  return (
    <Layout
      style={{
        minHeight: '100vh',
      }}
    >
      <Layout>
        <Content
          style={{
            margin: '0 16px',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <div
            style={{
              margin: '16px 0',  
              padding: 24,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <h1 
             style={{
                textAlign: 'center',
             }}
            >
                Log in
            </h1>
            <LoginForm />
            <p
              style={{
                textAlign: 'center',
             }}
            >
              Don't have an account? <a href='/#signup'>Signup</a>
            </p>
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
export default LoginPage;