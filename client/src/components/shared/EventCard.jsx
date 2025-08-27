import { motion } from 'framer-motion';
import { Clock, MapPin } from 'lucide-react';

const EventCard = ({ event }) => {
  return (
    <motion.div
      className="bg-white rounded-xl overflow-hidden border border-black/10 relative group"
      whileHover={{ 
        y: -8, 
        boxShadow: "0 15px 30px -5px rgba(45, 45, 45, 0.15), 0 8px 10px -6px rgba(45, 45, 45, 0.1)" 
      }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
    >
      <div className="h-72 w-full overflow-hidden">
        <img 
          src={event.image} 
          alt={event.title} 
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300 ease-in-out" 
        />
      </div>
      
      <div className="absolute top-3 right-3 bg-coral text-white p-2 rounded-lg text-center leading-none shadow-md">
        <span className="font-bold text-lg">{event.date.day}</span>
        <span className="text-xs block">{event.date.month}</span>
      </div>
      
      <div className="p-5">
        <h3 className="text-xl font-bold text-charcoal mb-3 truncate">{event.title}</h3>
        <div className="space-y-2 text-sm text-slate-light">
          <p className="flex items-center"><Clock size={14} className="mr-2.5" /> {event.time}</p>
          <p className="flex items-center"><MapPin size={14} className="mr-2.5" /> {event.location}</p>
        </div>
      </div>
    </motion.div>
  );
};

export default EventCard;