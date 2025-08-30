import { useState, useEffect, useContext } from 'react';
import DashboardHeader from '../components/dashboard/DashboardHeader';
import { FilterBar } from '../components/dashboard/AttendeeComponents';
import EventCard from '../components/shared/EventCard';
import AuthContext from '../context/AuthContext';

const EventsPage = () => {
    const { user } = useContext(AuthContext);
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                // UPDATED: Changed to a relative path
                const response = await fetch('/api/events');
                if (!response.ok) {
                    throw new Error('Failed to fetch events');
                }
                const data = await response.json();
                setEvents(data.events);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchEvents();
    }, []);

    return (
        <div className="min-h-screen bg-cream font-sans">
            <DashboardHeader user={user} />
            <main className="p-6 container mx-auto">
                <h1 className="text-3xl font-bold text-charcoal mb-6">Discover Events</h1>
                <FilterBar />
                
                {loading && <p className="text-center mt-8">Loading events...</p>}
                {error && <p className="text-center mt-8 text-red-500">Error: {error}</p>}
                
                {!loading && !error && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mt-8">
                        {events.map(event => (
                            <EventCard key={event.id} event={event} />
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
};

export default EventsPage;
