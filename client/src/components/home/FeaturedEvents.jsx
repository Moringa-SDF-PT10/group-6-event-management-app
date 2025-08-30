import { useState, useEffect } from 'react';
import EventCard from '../shared/EventCard';

const FeaturedEvents = () => {
  const [featuredEvents, setFeaturedEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFeaturedEvents = async () => {
      try {
        // UPDATED: Changed to a relative path
        const response = await fetch('/api/events/featured');
        const data = await response.json();
        if (response.ok) {
          setFeaturedEvents(data);
        } else {
          throw new Error(data.error || 'Failed to fetch featured events');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchFeaturedEvents();
  }, []);

  return (
    <section className="py-20 px-6 container mx-auto">
      <h2 className="text-4xl font-bold text-center mb-12 text-charcoal">Featured Events</h2>
      
      {loading && <p className="text-center">Loading events...</p>}
      {error && <p className="text-center text-red-500">Error: {error}</p>}

      {!loading && !error && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {featuredEvents.map(event => (
            <EventCard key={event.id} event={event} />
          ))}
        </div>
      )}
    </section>
  );
};

export default FeaturedEvents;
