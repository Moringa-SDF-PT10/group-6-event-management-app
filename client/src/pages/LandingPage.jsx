import { useState } from 'react';
import Header from '../components/layout/Header';
import TopPicksSlider from '../components/home/TopPicksSlider';
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
      <Header onLoginClick={() => openModal(true)} onSignupClick={() => openModal(false)} />
      
      <main>
        <TopPicksSlider />
        <FeaturedEvents />
      </main>

      <Footer />
    </div>
  );
};

export default LandingPage;