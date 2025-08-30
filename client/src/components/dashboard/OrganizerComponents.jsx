import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Edit, Trash2, PlusCircle, ArrowUp, DollarSign, Ticket, Users } from 'lucide-react';
import EditEventModal from './EditEventModal';
import DeleteConfirmationModal from './DeleteConfirmationModal';

// --- Mock Data ---
const myEvents = [
    { id: 1, title: 'My Awesome Tech Conference', date: '2025-10-15', time: '09:00', description: 'A conference about the future of tech.', status: 'Live', ticketsSold: 150, capacity: 200, price: 2500 },
    { id: 2, title: 'Annual Charity Gala', date: '2025-11-22', time: '18:00', description: 'A gala to support local charities.', status: 'Upcoming', ticketsSold: 88, capacity: 100, price: 5000 },
    { id: 3, title: 'Summer Music Fest', date: '2025-07-10', time: '12:00', description: 'Featuring the best local and international artists.', status: 'Completed', ticketsSold: 500, capacity: 500, price: 1500 },
];

const analyticsData = [ { name: 'Tech Conf', sold: 150 }, { name: 'Charity Gala', sold: 88 }, { name: 'Music Fest', sold: 500 }];

// --- Main Layout Component ---
export const OrganizerDashboardLayout = ({ onCreateEvent }) => {
    // --- State Management for Modals ---
    const [isEditModalOpen, setEditModalOpen] = useState(false);
    const [isDeleteModalOpen, setDeleteModalOpen] = useState(false);
    const [selectedEvent, setSelectedEvent] = useState(null);

    // --- Handler Functions ---
    const handleEditClick = (event) => {
        setSelectedEvent(event);
        setEditModalOpen(true);
    };

    const handleDeleteClick = (event) => {
        setSelectedEvent(event);
        setDeleteModalOpen(true);
    };

    const handleConfirmDelete = () => {
        alert(`Deleting event: ${selectedEvent.title}`); // Replace with API call
        console.log('Deleting event ID:', selectedEvent.id);
        closeModals();
    };
    
    const closeModals = () => {
        setEditModalOpen(false);
        setDeleteModalOpen(false);
        setSelectedEvent(null);
    };

    return (
        <>
            {/* --- Modals --- */}
            <EditEventModal 
                isOpen={isEditModalOpen} 
                onClose={closeModals} 
                event={selectedEvent} 
            />
            <DeleteConfirmationModal 
                isOpen={isDeleteModalOpen} 
                onClose={closeModals} 
                onConfirm={handleConfirmDelete}
                eventName={selectedEvent?.title}
            />

            {/* --- Dashboard Layout --- */}
            <div className="space-y-8">
                <div className="flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-bold text-charcoal">Organizer Dashboard</h1>
                        <p className="text-slate-light">Here's your event overview.</p>
                    </div>
                    <button onClick={onCreateEvent} className="flex items-center gap-2 bg-coral text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:bg-opacity-90 transition-transform hover:scale-105">
                        <PlusCircle size={20} />
                        Create New Event
                    </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <StatCard icon={DollarSign} title="Total Revenue" value="KES 251,000" change="+12.5%" />
                    <StatCard icon={Ticket} title="Tickets Sold (Month)" value="238" change="-2.1%" />
                    <StatCard icon={Users} title="New Attendees" value="42" change="+5.5%" />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2 bg-white p-6 rounded-xl border border-black/10 shadow-sm">
                        <h3 className="font-bold text-lg mb-4">My Events</h3>
                        <div className="space-y-4">
                            {myEvents.map(event => (
                                <EventListItem 
                                    key={event.id} 
                                    event={event} 
                                    onEdit={() => handleEditClick(event)}
                                    onDelete={() => handleDeleteClick(event)}
                                />
                            ))}
                        </div>
                    </div>
                    <div className="bg-white p-6 rounded-xl border border-black/10 shadow-sm">
                        <h3 className="font-bold text-lg mb-4">Ticket Sales per Event</h3>
                        <div className="h-80">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={analyticsData} layout="vertical">
                                    <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                                    <XAxis type="number" hide />
                                    <YAxis type="category" dataKey="name" width={80} tickLine={false} axisLine={false} />
                                    <Tooltip cursor={{ fill: 'rgba(255, 111, 97, 0.1)' }} />
                                    <Bar dataKey="sold" fill="#FF6F61" radius={[0, 4, 4, 0]} barSize={20} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

// --- Child Components ---
const StatCard = ({ icon: Icon, title, value, change }) => (
    <div className="bg-white p-6 rounded-xl border border-black/10 shadow-sm">
        <div className="flex items-center justify-center w-12 h-12 rounded-full bg-coral/10 mb-4">
            <Icon className="text-coral" size={24} />
        </div>
        <p className="text-sm text-slate-light">{title}</p>
        <div className="flex items-end justify-between mt-1">
            <p className="text-3xl font-bold text-charcoal">{value}</p>
            <div className={`flex items-center text-sm ${change.startsWith('+') ? 'text-green-500' : 'text-red-500'}`}>
                <ArrowUp size={14} className="mr-1" /> {change.substring(1)}
            </div>
        </div>
    </div>
);

const EventListItem = ({ event, onEdit, onDelete }) => (
    <div className="bg-gray-50 p-4 rounded-lg border flex flex-col md:flex-row justify-between items-center hover:bg-gray-100 transition-colors">
        <div>
            <h4 className="font-bold text-charcoal">{event.title}</h4>
            <p className="text-sm text-slate-light">
                {event.date} • {event.ticketsSold} / {event.capacity} tickets
            </p>
        </div>
        <div className="flex items-center gap-2 mt-4 md:mt-0">
            <span className={`text-xs font-semibold px-2 py-1 rounded-full ${event.status === 'Live' ? 'bg-green-100 text-green-700' : 'bg-gray-200 text-gray-600'}`}>
                {event.status}
            </span>
            <button onClick={onEdit} className="p-2 rounded-md hover:bg-blue-100 text-blue-500"><Edit size={18} /></button>
            <button onClick={onDelete} className="p-2 rounded-md hover:bg-red-100 text-red-500"><Trash2 size={18} /></button>
        </div>
    </div>
);