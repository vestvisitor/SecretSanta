import React from 'react';
import { Button, Form, Input } from 'antd';
import { useNavigate } from "react-router-dom";

import axios from 'axios';

const SignupForm = () => {

    const navigate = useNavigate();
    
    const SignUp = (data) => {
        axios.post('http://127.0.0.1:8000/users/signup', 
          data,
          {
            headers: {
              'Content-Type': 'application/json'
            }
        }).then(r => {
          const wishResponse = r.data
          console.log(wishResponse);
          console.log(r);
          setUserdata(wishResponse)
        })
        .catch(function (error) {
          console.log(error);
        });
      }

    const onFinish = (values) => {
        console.log('Success:', values);
        SignUp(values);
        navigate('/login');
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
        initialValues={{
        remember: true,
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
            label="Email"
            name="email"
            rules={[
            {
                required: true,
                message: 'Please input your email!',
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
export default SignupForm;
