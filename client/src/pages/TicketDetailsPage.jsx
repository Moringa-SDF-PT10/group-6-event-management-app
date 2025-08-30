import { useState, useEffect, useContext } from 'react';
import { useParams, Link } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import DashboardHeader from '../components/dashboard/DashboardHeader';
import { ArrowLeft, Calendar, Clock, MapPin, Users } from 'lucide-react';

const TicketDetailsPage = () => {
    const { ticketId } = useParams();
    const { user, token } = useContext(AuthContext);
    const [ticket, setTicket] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTicketDetails = async () => {
            if (!token || !ticketId) return;
            try {
                // UPDATED: Changed to a relative path
                const response = await fetch(`/api/users/attendee/tickets/${ticketId}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || 'Could not fetch ticket details.');
                }
                setTicket(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchTicketDetails();
    }, [token, ticketId]);

    if (loading) return <div className="min-h-screen bg-gray-100 flex items-center justify-center">Loading your ticket...</div>;
    if (error) return <div className="min-h-screen bg-gray-100 flex items-center justify-center text-red-500">Error: {error}</div>;
    if (!ticket) return <div className="min-h-screen bg-gray-100 flex items-center justify-center">Ticket not found.</div>;
    
    const { event } = ticket;

    return (
        <div className="min-h-screen bg-gray-100 font-sans">
            <DashboardHeader user={user} />
            <main className="container mx-auto p-6">
                <Link to="/dashboard" className="flex items-center gap-2 text-coral font-semibold mb-6 hover:underline">
                    <ArrowLeft size={18} />
                    Back to My Tickets
                </Link>

                <div className="bg-white rounded-2xl shadow-lg max-w-2xl mx-auto flex flex-col md:flex-row overflow-hidden">
                    {/* Left Side - Event Details */}
                    <div className="p-8 flex-grow">
                        <span className="text-xs font-semibold bg-coral/10 text-coral px-3 py-1 rounded-full">{event.categories[0]?.name || 'General'}</span>
                        <h1 className="text-3xl font-bold text-charcoal mt-4">{event.title}</h1>
                        <p className="text-slate-light mt-2">{event.short_description}</p>
                        
                        <div className="border-t my-6"></div>

                        <div className="space-y-4 text-sm">
                            <div className="flex items-center gap-3"><Calendar size={18} className="text-coral" /><span>{new Date(event.date).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</span></div>
                            <div className="flex items-center gap-3"><Clock size={18} className="text-coral" /><span>{new Date(event.date).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })}</span></div>
                            <div className="flex items-center gap-3"><MapPin size={18} className="text-coral" /><span>{event.location} - {event.venue}</span></div>
                            <div className="flex items-center gap-3"><Users size={18} className="text-coral" /><span>{ticket.quantity} Ticket(s)</span></div>
                        </div>
                    </div>
                    {/* Right Side - QR Code */}
                    <div className="bg-gray-50 p-8 flex-shrink-0 flex flex-col items-center justify-center border-l">
                         <img 
                            src={`https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=ticket-${ticket.id}-event-${event.id}`}
                            alt="QR Code for ticket"
                            className="w-40 h-40 rounded-lg"
                        />
                        <p className="text-xs text-slate-light mt-4 text-center">Scan at the gate</p>
                        <p className="font-mono text-xs text-charcoal">Ticket ID: {ticket.id}</p>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default TicketDetailsPage;
