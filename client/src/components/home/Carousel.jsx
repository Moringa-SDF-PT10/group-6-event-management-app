import { motion } from 'framer-motion';

const carouselEvents = [
  { id: 1, title: 'Nairobi Tech Summit 2025', image: 'https://placehold.co/1200x600/8B5CF6/FFFFFF?text=Tech+Summit' },
  { id: 2, title: 'AfroBeats Music Festival', image: 'https://placehold.co/1200x600/EC4899/FFFFFF?text=Music+Fest' },
  { id: 3, title: 'Savannah Art Exhibition', image: 'https://placehold.co/1200x600/F59E0B/FFFFFF?text=Art+Exhibit' },
  //Using Mock data just to show the carousel and test responsiveness
];

const Carousel = () => {
  const duplicatedEvents = [...carouselEvents, ...carouselEvents];
  
  return (
    <section className="py-20 bg-gray-900">
      <div className="w-full overflow-hidden">
        <motion.div
          className="flex gap-8"
          animate={{ x: ['0%', `-${100 * (carouselEvents.length / duplicatedEvents.length)}%`] }}
          transition={{ ease: 'linear', duration: 20, repeat: Infinity }}
        >
          {duplicatedEvents.map((event, index) => (
            <div key={index} className="relative flex-shrink-0 w-[60vw] md:w-[40vw] h-[40vh] rounded-lg overflow-hidden">
              <img src={event.image} alt={event.title} className="w-full h-full object-cover" />
              <div className="absolute inset-0 bg-black bg-opacity-40 flex items-end p-6">
                <h3 className="text-2xl font-bold text-white">{event.title}</h3>
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default Carousel;