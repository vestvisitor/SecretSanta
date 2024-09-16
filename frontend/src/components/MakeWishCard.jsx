import React from 'react';
import { Card, Rate } from 'antd';
const { Meta } = Card;
const MakeWishCard = (title, image_src) => (
  <Card
    style={{
      width: 240,
    }}
    cover={<img alt="example" src={image_src} />}
  >
    <Meta title={title} />
  </Card>  
);
export default MakeWishCard;