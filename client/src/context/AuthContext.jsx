import { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(() => localStorage.getItem('token') || null);
    const navigate = useNavigate();
    const API_URL = 'http://127.0.0.1:5000';

    useEffect(() => {
        if (token) {
            localStorage.setItem('token', token);
        } else {
            localStorage.removeItem('token');
        }
    }, [token]);

    const signup = async (values) => {
        try {
            const response = await fetch(`${API_URL}/signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    firstName: values.firstName,
                    lastName: values.lastName,
                    phoneNumber: values.phoneNumber,
                    username: values.username,
                    email: values.email,
                    password: values.password,
                    role: values.role,
                }),
            });
            const data = await response.json();
            if (response.ok) {
                setToken(data.access_token);
                setUser(data.user);
                navigate('/dashboard'); 
            } else {
                console.error(data.error);
            }
        } catch (error) {
            console.error('Signup failed:', error);
        }
    };

    const login = async (values) => {
        try {
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: values.username,
                    password: values.password,
                }),
            });
            const data = await response.json();
            if (response.ok) {
                setToken(data.access_token);
                setUser(data.user);
                navigate('/dashboard');
            } else {
                console.error(data.error);
            }
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    const logout = () => {
        fetch(`${API_URL}/logout`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        setUser(null);
        setToken(null);
        navigate('/');
    };

    return (
        <AuthContext.Provider value={{ user, token, login, signup, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthContext;