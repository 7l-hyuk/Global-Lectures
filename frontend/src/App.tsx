import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import IndexPage from './pages/IndexPage';
import SignupPage from './pages/SignupPage';
import SigninPage from './pages/SigninPage';
import SerivcePage from './pages/ServicePage';
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
            <Route path="/service" element={<SerivcePage />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}


export default App;
