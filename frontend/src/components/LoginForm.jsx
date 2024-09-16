import React, { useEffect, useState } from 'react';
import { Button, Form, Input } from 'antd';
import axios from 'axios';
import { useNavigate } from "react-router-dom";

const LoginForm = () => {

  const navigate = useNavigate();

  useEffect(() => {
    console.log(localStorage.getItem('access_token'))
  });

  const Login = (data) => {
    axios.post('http://127.0.0.1:8000/users/token', 
      data,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(r => {
      const wishResponse = r.data
      console.log(wishResponse);
      localStorage.setItem("access_token", wishResponse.access_token)
      localStorage.setItem("token_type", wishResponse.token_type)
      navigate('/');
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  const onFinish = (values) => {
    console.log('Success:', values);
    Login(values)    
  };

  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };
  
  return(

  <Form
    name="basic"
    labelCol={{
      span: 8,
    }}
    wrapperCol={{
      span: 16,
    }}
    style={{
      maxWidth: 600,
    }}
    onFinish={onFinish}
    onFinishFailed={onFinishFailed}
    autoComplete="off"
  >
    <Form.Item
      label="Username"
      name="username"
      rules={[
        {
          required: true,
          message: 'Please input your username!',
        },
      ]}
    >
      <Input />
    </Form.Item>

    <Form.Item
      label="Password"
      name="password"
      rules={[
        {
          required: true,
          message: 'Please input your password!',
        },
      ]}
    >
      <Input.Password />
    </Form.Item>
  
    <Form.Item
      wrapperCol={{
        offset: 9,
        span: 16,
      }}
    >
      <Button type="primary" htmlType="submit">
        Submit
      </Button>
    </Form.Item>
  </Form>
  );
};
export default LoginForm;