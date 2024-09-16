import React from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import { Card, Button } from 'antd';

const WishCardPrivate = ({id, name, link, image_src}) => {

  const navigate = useNavigate();

  const deleteWish = (data, token) => {
    axios.delete('http://127.0.0.1:8000/wishes/delete',
      {
        params: {
          wish_id: data
        },
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      }
    )
    .then(r => {
      window.location.reload();
    })
    .catch(function (error) {
      console.log(error);
      // navigate('/login');
    });
  }

  const AuthenticateUser = (token, wish) => {
    axios.get('http://127.0.0.1:8000/users/me',
      {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
          
        }
    }).then(r => {
      deleteWish(id, token)
    })
    .catch(function (error) {
      console.log(error);
      navigate('/login');
    });
  }

  function onClick () {
    const access_token = localStorage.getItem('access_token');
    AuthenticateUser(access_token)
  }

  return(
    <Card
    id={id}
    hoverable
    title={
      <a href={link}>{name}</a>      
    }
    style={{
      width: '100%',
      height: '100%'
    }}
  >
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 50
      }}
    >
      <img 
      src={image_src}
      style={{
        height: '150px',
        width: '150px'
      }}
    >      
    </img>
    <Button 
        type="primary" 
        danger
        onClick={onClick}
    >
      Delete wish
    </Button>
    </div>
    
  </Card>
  );
}; 
export default WishCardPrivate;