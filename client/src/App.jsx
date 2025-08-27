import { Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import AuthPage from './pages/AuthPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/auth" element={<AuthPage />} /> {/* Add the auth route */}
      {/* TODO: Add a protected route for the dashboard, e.g., /dashboard */}
    </Routes>
  );
}

export default App;