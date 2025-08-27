import { useState } from 'react';
import Header from '../components/layout/Header';
import TopPicksSlider from '../components/home/TopPicksSlider'; // We'll use this directly
import FeaturedEvents from '../components/home/FeaturedEvents';
import Footer from '../components/layout/Footer';
import AuthModal from '../components/auth/AuthModal';

const LandingPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLogin, setIsLogin] = useState(true);

  const openModal = (loginState) => {
    setIsLogin(loginState);
    setIsModalOpen(true);
  };

  return (
    <div className="bg-cream text-charcoal font-sans">
      <AuthModal isOpen={isModalOpen} setIsOpen={setIsModalOpen} isLogin={isLogin} setIsLogin={setIsLogin} />
      
      {/* The Header is now a permanent fixture at the top */}
      <Header onLoginClick={() => openModal(true)} onSignupClick={() => openModal(false)} />
      
      <main>
        {/* The TopPicksSlider is now the first thing the user sees below the header */}
        <TopPicksSlider />
        <FeaturedEvents />
      </main>

      <Footer />
    </div>
  );
};

export default LandingPage;