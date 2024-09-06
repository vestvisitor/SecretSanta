import { HashRouter as Router, Routes, Route } from "react-router-dom";
import MainPage from "./pages/MainPage.jsx"
import LoginForm from "./components/LoginForm.jsx"
import WishCard from "./components/WishCard.jsx"


const App = () => {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage/>}/>
        <Route path="/login" element={<LoginForm/>}/>
        <Route path="/register" element={<WishCard/>}/>
      </Routes>
    </Router>
  )
}

export default App;
