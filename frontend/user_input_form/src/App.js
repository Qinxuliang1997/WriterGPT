import Preliminary from "./components/Preliminary";
import Article from "./components/Article";
import Navigation from "./components/Navigations";
import Login from "./components/Login";
import Logout from "./components/Logout";
import Register from "./components/Register";
import Portfolio from "./components/Home"
import Start from "./components/Start"
import OneClickRequirement from "./components/OneClickRequirement"
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Navigation></Navigation>
      <Routes>
        <Route path="/" >
          <Route index element={<Portfolio />} />
          <Route path="/login" element={<Login/>}/>
          <Route path="/logout" element={<Logout/>}/>
          <Route path="/register" element={<Register/>}/>
          <Route path="/start" element={<Start/>}/>
          <Route path="/preliminary" element={<Preliminary />} />
          <Route path="article" element={<Article />} />
          <Route path="/oneclickrequirement" element={<OneClickRequirement/>} />
          {/* <Route path="*" element={<NoPage />} /> */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
