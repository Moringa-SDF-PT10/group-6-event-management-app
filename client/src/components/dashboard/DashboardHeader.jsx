import { useContext } from 'react';
import { Link } from 'react-router-dom';
import { LogOut, PlusCircle } from 'lucide-react';
import AuthContext from '../../context/AuthContext';

const DashboardHeader = ({ user, onCreateEvent }) => {
    const { logout } = useContext(AuthContext);
    const isOrganizer = user.role === 'organizer';

    return (
        <header className="bg-white/80 backdrop-blur-sm border-b border-black/10 sticky top-0 z-40">
            <div className="container mx-auto p-4 flex justify-between items-center">
                <div>
                    <Link to="/dashboard" className="text-2xl font-bold text-charcoal hover:text-coral transition-colors">
                        Dashboard
                    </Link>
                    <p className="text-slate-light">Welcome back, {user.username}!</p>
                </div>

                {/* Logout button component */}
                <div className="flex items-center gap-4">
                    <button 
                        onClick={logout} 
                        className="flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-md text-coral hover:bg-coral/10 transition-colors"
                    >
                        <LogOut size={16} />
                        Logout
                    </button>
                </div>
            </div>
        </header>
    );
};

export default DashboardHeader;