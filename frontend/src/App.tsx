import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Videos from "./pages/Videos";
import Layout from "./components/Layout";
import VideoDetailPage from "./pages/VideoDetailPage";
import { AuthProvider } from "./context/AuthContext";
import PrivateRoute from "./components/PrivateRoute";
import UserPageLayout from "./components/UserPageLayout";


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
            <Route element={<UserPageLayout />}>
              <Route 
                path="/videos"
                element={
                  <PrivateRoute>
                    <Videos />
                  </PrivateRoute>
                } 
              />
            </Route>
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
