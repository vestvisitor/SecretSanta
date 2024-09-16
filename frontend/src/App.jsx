import { HashRouter as Router, Routes, Route } from "react-router-dom";
import MainPage from "./pages/MainPage.jsx"
import LoginPage from "./pages/LoginPage.jsx"
import SignupPage from "./pages/SignupPage.jsx"
import ProfilePage from "./pages/ProfilePage.jsx"
import MyWishlistPage from "./pages/MyWishlistPage.jsx"
import WishlistPage from "./pages/WishlistPage.jsx"
import MakewishPage from "./pages/MakewishPage.jsx"

const App = () => {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage/>}/>
        <Route path="/login" element={<LoginPage/>}/>
        <Route path="/signup" element={<SignupPage/>}/>
        <Route path="/profile" element={<ProfilePage/>}/>
        <Route path="/my-wishlist" element={<MyWishlistPage/>}/>
        <Route path="/wishlist/:userId"
        loader={({ params }) => {
          return fetchTeam(params.userId);
        }}
         element={<WishlistPage/>}/>
        <Route path="/make-wish" element={<MakewishPage/>}/>
      </Routes>
    </Router>
  )
}

export default App;
