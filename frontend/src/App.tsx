import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import IndexPage from './pages/IndexPage';
import SignupPage from './pages/SignupPage';
import SigninPage from './pages/SigninPage';
import SerivcePage from './pages/ServicePage';
import VideoListPage from './pages/VideoListPage';
import VideoPlayPage from './pages/VideoPlayPage';
import PrivateRoute from './viewmodels/PrivateRoute';

import { AuthProvider } from './viewmodels/AuthContext';
import Layout from './components/Layouts/Layout';
import './styles/App.css';


function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<IndexPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/signin" element={<SigninPage />} />
            <Route path="/service" element={
                <PrivateRoute>
                  <SerivcePage />
                </PrivateRoute>
              }
            />
            <Route path="/videos/:id" element={
              <PrivateRoute>
                <VideoPlayPage />
              </PrivateRoute>
            } />
            <Route path="/videos" element={
              <PrivateRoute>
                <VideoListPage />
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
