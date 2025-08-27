import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import AuthForm from '../components/auth/AuthForm';

const AuthPage = () => {
    const [searchParams] = useSearchParams();
    const mode = searchParams.get('mode') || 'login';

    // Set the initial state based on the URL
    const [isLogin, setIsLogin] = useState(mode === 'login');
    const [role, setRole] = useState('attendee');

    // This effect ensures the form syncs if the user presses back or forward
    useEffect(() => {
        setIsLogin(mode === 'login');
    }, [mode]);

    return (
        <div className="min-h-screen bg-cream flex flex-col items-center justify-center p-4 font-sans">
            <div className="text-center mb-8">
                <Link to="/" className="text-3xl font-bold tracking-wider text-charcoal">EH.</Link>
                <p className="text-slate-light mt-2">Your ultimate platform for event management.</p>
            </div>

            <div className="w-full max-w-lg bg-white p-8 rounded-2xl shadow-lg border border-black/10">
                <div className="flex justify-center mb-6 bg-gray-100 p-1 rounded-lg">
                    <button 
                        onClick={() => setRole('attendee')}
                        className={`w-1/2 py-2 rounded-md transition-colors text-sm font-semibold ${role === 'attendee' ? 'bg-coral text-white shadow' : 'text-slate-light'}`}
                    >
                        I'm an Attendee
                    </button>
                    <button 
                        onClick={() => setRole('organizer')}
                        className={`w-1/2 py-2 rounded-md transition-colors text-sm font-semibold ${role === 'organizer' ? 'bg-coral text-white shadow' : 'text-slate-light'}`}
                    >
                        I'm an Organizer
                    </button>
                </div>
                
                <AuthForm isLogin={isLogin} setIsLogin={setIsLogin} role={role} />
            </div>
        </div>
    );
};

export default AuthPage;