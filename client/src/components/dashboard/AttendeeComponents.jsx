import { Link } from 'react-router-dom';
import { Calendar, Clock, MapPin, Search, ArrowRight } from 'lucide-react';

// --- Mock Data fir testing ---
const myTickets = [
    { id: 1, title: 'Komplex - The Hangar', date: 'Sat, 30 Aug', time: '8:00 PM', location: 'Wilson Airport', image: 'https://placehold.co/600x400/FF6F61/FFFFFF?text=Ticket' },
    { id: 2, title: 'Sultana\'s Dream Festival', date: 'Thu, 03 Jul', time: '6:00 PM', location: 'Coastal Grounds, Mombasa', image: 'https://placehold.co/600x400/6BFFB8/2D2D2D?text=Ticket' },
];

// --- Main Layout for the Attendee Dashboard ---
export const AttendeeDashboardLayout = () => (
    <div className="space-y-12">
        <div>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-charcoal">My Upcoming Events</h2>
                <Link 
                    to="/events" 
                    className="flex items-center gap-2 bg-coral text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-opacity-90 transition-transform hover:scale-105"
                >
                    Browse More Events <ArrowRight size={18} />
                </Link>
            </div>
            {myTickets.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {myTickets.map(ticket => <TicketCard key={ticket.id} ticket={ticket} />)}
                </div>
            ) : (
                <div className="text-center py-12 bg-white rounded-lg border border-dashed">
                    <p className="text-slate-light">You don't have any tickets yet.</p>
                </div>
            )}
        </div>
    </div>
);

// --- Reusable Components for Attendee Views ---

export const TicketCard = ({ ticket }) => (
    <div className="bg-white rounded-xl overflow-hidden shadow-lg border border-black/10 transform hover:-translate-y-2 transition-transform duration-300">
        <img src={ticket.image} alt={ticket.title} className="w-full h-48 object-cover" />
        <div className="p-5">
            <h3 className="text-xl font-bold text-charcoal mb-3">{ticket.title}</h3>
            <div className="space-y-2 text-sm text-slate-light">
                <p className="flex items-center"><Calendar size={14} className="mr-2.5" /> {ticket.date}</p>
                <p className="flex items-center"><Clock size={14} className="mr-2.5" /> {ticket.time}</p>
                <p className="flex items-center"><MapPin size={14} className="mr-2.5" /> {ticket.location}</p>
            </div>
        </div>
    </div>
);

// This is the advanced filter bar thats on the events page
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

// This is a generic event card for the events page
export const EventCard = ({ event }) => (
    <div className="bg-white rounded-xl overflow-hidden shadow-lg border border-black/10 transform hover:-translate-y-2 transition-transform duration-300">
        <img src={event.image} alt={event.title} className="w-full h-48 object-cover" />
        <div className="p-5">
            <h3 className="text-xl font-bold text-charcoal mb-3">{event.title}</h3>
            <div className="space-y-2 text-sm text-slate-light">
                <p className="flex items-center"><Calendar size={14} className="mr-2.5" /> {event.date.day} {event.date.month}</p>
                <p className="flex items-center"><Clock size={14} className="mr-2.5" /> {event.time}</p>
                <p className="flex items-center"><MapPin size={14} className="mr-2.5" /> {event.location}</p>
            </div>
        </div>
    </div>
);