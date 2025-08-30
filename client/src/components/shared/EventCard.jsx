import { motion } from 'framer-motion';
import { Clock, MapPin } from 'lucide-react';
import { Link } from 'react-router-dom';

const EventCard = ({ event }) => {
  // Format the date from the ISO string
  const eventDate = new Date(event.date);
  const day = eventDate.getDate();
  const month = eventDate.toLocaleString('default', { month: 'short' }).toUpperCase();
  const time = eventDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });

  return (
    <Link to={`/events/${event.slug}`}>
      <motion.div
        className="bg-white rounded-xl overflow-hidden border border-black/10 relative group h-full flex flex-col"
        whileHover={{ 
          y: -8, 
          boxShadow: "0 15px 30px -5px rgba(45, 45, 45, 0.15), 0 8px 10px -6px rgba(45, 45, 45, 0.1)" 
        }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
      >
        <div className="h-48 w-full overflow-hidden">
          <img 
            src={event.image_url || `https://placehold.co/600x400/FF6F61/FFFFFF?text=${event.title.replace(' ', '+')}`} 
            alt={event.title} 
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300 ease-in-out" 
          />
        </div>
        
        <div className="absolute top-3 right-3 bg-coral text-white p-2 rounded-lg text-center leading-none shadow-md">
          <span className="font-bold text-lg">{day}</span>
          <span className="text-xs block">{month}</span>
        </div>
        
        <div className="p-5 flex-grow flex flex-col">
          <h3 className="text-xl font-bold text-charcoal mb-3 truncate flex-grow">{event.title}</h3>
          <div className="space-y-2 text-sm text-slate-light mt-auto">
            <p className="flex items-center"><Clock size={14} className="mr-2.5" /> {time}</p>
            <p className="flex items-center"><MapPin size={14} className="mr-2.5" /> {event.location}</p>
          </div>
        </div>
      </motion.div>
    </Link>
  );
};

export default EventCard;
