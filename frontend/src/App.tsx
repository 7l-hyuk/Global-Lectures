import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Userpage from "./pages/Userpage";
import Layout from "./components/Layout";
import VideoDetailPage from "./pages/VideoDetailPage";
import { AuthProvider } from "./context/AuthContext";
import PrivateRoute from "./components/PrivateRoute";


function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/videos/:id" element={<VideoDetailPage />} />
            <Route 
              path="/mypage"
              element={
                <PrivateRoute>
                <Userpage />
                </PrivateRoute>
              } 
            />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
