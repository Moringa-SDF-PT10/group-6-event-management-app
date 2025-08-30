import { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { Calendar, MapPin, Ticket, Clock } from 'lucide-react';
import AuthContext from '../context/AuthContext';
import DashboardHeader from '../components/dashboard/DashboardHeader';
import PurchaseTicketModal from '../components/dashboard/PurchaseTicketModal';

const EventDetailPage = () => {
    const { slug } = useParams();
    const { user } = useContext(AuthContext);
    const [event, setEvent] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isPurchaseModalOpen, setPurchaseModalOpen] = useState(false);

    useEffect(() => {
        const fetchEvent = async () => {
            try {
                // UPDATED: Changed to a relative path
                const response = await fetch(`/api/events/slug/${slug}`);
                if (!response.ok) {
                    throw new Error('Event not found');
                }
                const data = await response.json();
                setEvent(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchEvent();
    }, [slug]);

    if (loading) {
        return <div className="min-h-screen bg-cream flex items-center justify-center">Loading event details...</div>;
    }

    if (error) {
        return <div className="min-h-screen bg-cream flex items-center justify-center text-red-500">Error: {error}</div>;
    }
    
    if (!event) {
         return <div className="min-h-screen bg-cream flex items-center justify-center">Could not find the event.</div>;
    }

    const formatDateTime = (isoString) => {
        const date = new Date(isoString);
        return {
            date: date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }),
            time: date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
        };
    };
    
    const { date, time } = formatDateTime(event.date);

    return (
        <div className="min-h-screen bg-gray-50 font-sans">
            {event && (
                <PurchaseTicketModal
                    isOpen={isPurchaseModalOpen}
                    onClose={() => setPurchaseModalOpen(false)}
                    event={event}
                />
            )}
            
            <DashboardHeader user={user} />
            <main className="container mx-auto p-6">
                <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
                    <img 
                        src={event.image_url || 'https://placehold.co/1200x400/FF6F61/FFFFFF?text=Event+Banner'} 
                        alt={event.title}
                        className="w-full h-64 md:h-80 object-cover"
                    />
                    <div className="p-8 md:p-12">
                        <div className="flex flex-wrap justify-between items-start gap-4 mb-6">
                            <div>
                                <h1 className="text-4xl md:text-5xl font-extrabold text-charcoal">{event.title}</h1>
                                <div className="flex items-center gap-2 mt-2">
                                    {event.categories.map(cat => (
                                        <span key={cat.id} className="text-xs font-semibold bg-coral/10 text-coral px-3 py-1 rounded-full">{cat.name}</span>
                                    ))}
                                </div>
                            </div>
                            <div className="bg-coral text-white font-bold py-3 px-6 rounded-lg text-center shadow-md">
                                <span className="text-2xl">{event.price > 0 ? `KES ${event.price.toLocaleString()}` : 'Free'}</span>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 border-y py-6 mb-8">
                            <div className="flex items-center gap-4">
                                <Calendar className="w-8 h-8 text-coral"/>
                                <div>
                                    <p className="font-bold text-charcoal">Date</p>
                                    <p className="text-slate-light">{date}</p>
                                </div>
                            </div>
                             <div className="flex items-center gap-4">
                                <Clock className="w-8 h-8 text-coral"/>
                                <div>
                                    <p className="font-bold text-charcoal">Time</p>
                                    <p className="text-slate-light">{time}</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-4">
                                <MapPin className="w-8 h-8 text-coral"/>
                                <div>
                                    <p className="font-bold text-charcoal">Location</p>
                                    <p className="text-slate-light">{event.location} - {event.venue}</p>
                                </div>
                            </div>
                        </div>

                        <div>
                            <h2 className="text-2xl font-bold text-charcoal mb-4">About This Event</h2>
                            <p className="text-slate-light leading-relaxed whitespace-pre-wrap">{event.description}</p>
                        </div>
                         <div className="mt-10 text-center">
                            <button 
                                onClick={() => setPurchaseModalOpen(true)}
                                className="bg-coral text-white font-semibold py-4 px-10 rounded-lg shadow-lg hover:bg-opacity-90 transition-transform hover:scale-105 flex items-center gap-3 mx-auto"
                            >
                                <Ticket size={20} />
                                Get Your Ticket
                            </button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default EventDetailPage;
