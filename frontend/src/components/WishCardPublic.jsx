import axios from 'axios';
import { Card, Button } from 'antd';
import { useNavigate } from "react-router-dom";

const WishCardPublic = ({id, name, link, image_src}) => {

  const navigate = useNavigate();

  const addWish = (token, data) => {
    axios.post('http://127.0.0.1:8000/wishes/add',
      data,
      {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
        }
    }
    )
    .catch(function (error) {
      console.log(error);
      // navigate('/login');
    });
  }

  const AuthenticateUser = (token) => {
    axios.get('http://127.0.0.1:8000/users/me',
      {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
          
        }
    }).then(r => {
      const obj = {wish_id: id}
      addWish(token, obj)
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

  return (
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
      onClick={onClick}
      type="primary">
    Add wish to my wishlist
      </Button>
    </div>
    
  </Card>
);
};
export default WishCardPublic;