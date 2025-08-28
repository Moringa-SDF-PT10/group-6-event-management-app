import DashboardHeader from '../components/dashboard/DashboardHeader';
import { FilterBar, EventCard } from '../components/dashboard/AttendeeComponents';
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';

// Mock data for all discoverable events
const allEvents = Array.from({ length: 12 }, (_, i) => ({
  id: i + 1,
  title: `Community Art Workshop ${i + 1}`,
  date: { day: `${10 + i}`, month: 'NOV' },
  time: '10:00 AM',
  location: 'Nairobi, Kenya',
  image: `https://placehold.co/600x400/${['FFD166', '91C9FF', 'FF6F61', '6BFFB8'][i%4]}/2D2D2D?text=Event+${i+1}`
}));

const EventsPage = () => {
    const { user } = useContext(AuthContext);

    return (
        <div className="min-h-screen bg-cream font-sans">
            <DashboardHeader user={user} />
            <main className="p-6 container mx-auto">
                <h1 className="text-3xl font-bold text-charcoal mb-6">Discover Events</h1>
                <FilterBar />
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mt-8">
                    {allEvents.map(event => (
                        <EventCard key={event.id} event={event} />
                    ))}
                </div>
            </main>
        </div>
    );
};

export default EventsPage;