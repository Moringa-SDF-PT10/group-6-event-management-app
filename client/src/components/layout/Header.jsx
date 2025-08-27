import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="absolute top-0 left-0 right-0 z-40 p-6 flex justify-between items-center">
      <Link to="/" className="text-2xl font-bold tracking-wider text-charcoal">EH.</Link>
      <div className="flex items-center gap-4">
        <Link to="/auth?mode=login" className="px-4 py-2 text-sm font-semibold rounded-md text-charcoal hover:bg-black/5 transition-colors">Log In</Link>
        <Link to="/auth?mode=signup" className="px-4 py-2 text-sm font-semibold bg-coral text-white rounded-md hover:bg-opacity-90 transition-colors">Sign Up</Link>
      </div>
    </header>
  );
};

export default Header;