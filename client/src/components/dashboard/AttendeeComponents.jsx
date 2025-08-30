import { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import { Calendar, Clock, MapPin, Search, ArrowRight } from 'lucide-react';
import AuthContext from '../../context/AuthContext';

export const AttendeeDashboardLayout = () => {
    const { token } = useContext(AuthContext);
    const [myTickets, setMyTickets] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMyTickets = async () => {
            if (!token) return;
            try {
                const response = await fetch('http://127.0.0.1:5000/api/users/attendee/tickets', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const data = await response.json();
                if (response.ok) {
                    setMyTickets(data || []);
                } else {
                    throw new Error(data.error || "Failed to fetch tickets.");
                }
            } catch (error) {
                console.error(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchMyTickets();
    }, [token]);

    return (
        <div className="space-y-12">
            <div>
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-3xl font-bold text-charcoal">My Tickets</h2>
                    <Link to="/events" className="flex items-center gap-2 bg-coral text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-opacity-90 transition-transform hover:scale-105">
                        Browse More Events <ArrowRight size={18} />
                    </Link>
                </div>
                {loading ? (
                    <p>Loading your tickets...</p>
                ) : myTickets.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {myTickets.map(ticket => (
                            <TicketCard key={ticket.id} ticket={ticket} />
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-12 bg-white rounded-lg border border-dashed">
                        <p className="text-slate-light">You don't have any tickets yet.</p>
                        <Link to="/events" className="text-coral font-semibold hover:underline mt-2 inline-block">Find your next event!</Link>
                    </div>
                )}
            </div>
        </div>
    );
};


export const TicketCard = ({ ticket }) => {
    const { event } = ticket;
    const eventDate = new Date(event.date);
    const time = eventDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
    const date = eventDate.toLocaleDateString('en-US', { weekday: 'short', day: '2-digit', month: 'short' });

    return (
        <Link to={`/tickets/${ticket.id}`} className="block group">
            <div className="bg-white rounded-xl overflow-hidden shadow-lg border border-black/10 transform group-hover:-translate-y-2 transition-transform duration-300">
                <img src={event.image_url || 'https://placehold.co/600x400/FF6F61/FFFFFF?text=Event'} alt={event.title} className="w-full h-48 object-cover" />
                <div className="p-5">
                    <h3 className="text-xl font-bold text-charcoal mb-3 truncate">{event.title}</h3>
                    <div className="space-y-2 text-sm text-slate-light">
                        <p className="flex items-center"><Calendar size={14} className="mr-2.5" /> {date}</p>
                        <p className="flex items-center"><Clock size={14} className="mr-2.5" /> {time}</p>
                        <p className="flex items-center"><MapPin size={14} className="mr-2.5" /> {event.location}</p>
                    </div>
                </div>
            </div>
        </Link>
    );
};

export const FilterBar = () => (
    <div className="p-4 bg-white rounded-lg border border-black/10 grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="relative md:col-span-2">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input placeholder="Search by event name or location..." className="w-full pl-10 p-2 border rounded-md" />
        </div>
        <select className="p-2 border rounded-md"><option>Event Type</option></select>
        <select className="p-2 border rounded-md"><option>Date Range</option></select>
        <button className="bg-coral text-white font-semibold py-2 px-4 rounded-md">Filter</button>
    </div>
);

