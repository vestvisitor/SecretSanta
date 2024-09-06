import { Card } from "antd";

function WishCard() {

    return (
      <div>
        <Card
            title={
                <div className="flex items-center gap-3">
                    <img src="https://gw.alipayobjects.com/zos/rmsportal/KDpgvguMpGfqaHPjicRK.svg"/>
                    <span>Wish</span>
                </div>
            }
            extra={<a href="#">More</a>}
            style={{
                width: 300,
            }}
            >
            <p>Card content</p>
            <p>Card content</p>
            <p>Card content</p>
        </Card>
      </div>
    )
  }
  
  export default WishCard
