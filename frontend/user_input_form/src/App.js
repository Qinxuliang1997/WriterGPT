import Preliminary from "./components/Preliminary";
import Article from "./components/Article";
import Navigation from "./components/Navigations";
import Login from "./components/Login";
import Logout from "./components/Logout";
import Register from "./components/Register";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Navigation></Navigation>
      <Routes>
        <Route path="/" >
          <Route path="/login" element={<Login/>}/>
          <Route path="/logout" element={<Logout/>}/>
          <Route path="/register" element={<Register/>}/>
          <Route index element={<Preliminary />} />
          <Route path="article" element={<Article />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
