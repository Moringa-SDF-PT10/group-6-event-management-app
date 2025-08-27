import EventCard from '../shared/EventCard';

const featuredEvents = Array.from({ length: 8 }, (_, i) => ({
  id: i + 1,
  title: `Pastel Night Groove ${i + 1}`,
  date: { day: `${10 + i}`, month: 'OCT' },
  time: '8:00 PM',
  location: 'Nairobi, Kenya',
  image: `https://placehold.co/600x400/${['FF6F61', '6BFFB8', 'A491D3', 'FFD166'][i%4]}/2D2D2D?text=Event+${i+1}`
}));

const FeaturedEvents = () => {
  return (
    <section className="py-20 px-6 container mx-auto">
      <h2 className="text-4xl font-bold text-center mb-12 text-charcoal">Featured Events</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
        {featuredEvents.map(event => (
          <EventCard key={event.id} event={event} />
        ))}
      </div>
    </section>
  );
};

export default FeaturedEvents;