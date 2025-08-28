import { motion, AnimatePresence } from 'framer-motion';
import AuthForm from './AuthForm';

const AuthModal = ({ isOpen, setIsOpen, isLogin, setIsLogin }) => {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-70 backdrop-blur-sm"
        onClick={() => setIsOpen(false)}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
          className="bg-gray-800 rounded-xl shadow-lg border border-gray-700"
          onClick={(e) => e.stopPropagation()}
        >
          <AuthForm isLogin={isLogin} setIsLogin={setIsLogin} />
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default AuthModal;