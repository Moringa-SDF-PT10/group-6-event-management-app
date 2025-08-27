import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, MapPin, ArrowRight } from 'lucide-react';

const topPicksEvents = [
    { 
        id: 1, 
        title: 'Komplex - The Hangar', 
        date: 'Sat, 30 Aug', 
        location: 'Wilson Airport', 
        image: 'https://placehold.co/1200x900/FF6F61/FFFFFF?text=The+Hangar',
        description: 'Komplex KE touches down at Hangar #2! For a raw, industrial gathering at Wilson Airport. Strictly 21+ and zero-tolerance policy.'
    },
    { 
        id: 2, 
        title: 'Sultana\'s Dream Festival', 
        date: 'Thu, 03 Jul', 
        location: 'Coastal Grounds, Mombasa', 
        image: 'https://placehold.co/1200x900/6BFFB8/2D2D2D?text=Sultana\'s+Dream',
        description: 'An immersive experience celebrating coastal art, music, and culture under the stars. Featuring live bands and culinary delights.'
    },
    { 
        id: 3, 
        title: 'Nafasi Circuit Grand Finale', 
        date: 'Thu, 31 Jul', 
        location: 'The GoDown Arts Centre', 
        image: 'https://placehold.co/1200x900/A491D3/FFFFFF?text=Nafasi+Circuit',
        description: 'The final stop of the Nafasi Circuit tour, showcasing the best in East African electronic music and visual arts.'
    },
];

const TopPicksSlider = () => {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIndex((prevIndex) => (prevIndex + 1) % topPicksEvents.length);
    }, 15000);
    return () => clearTimeout(timer);
  }, [index]);

  return (
    <section className="w-full pt-24 md:pt-32 container mx-auto px-6">
        <AnimatePresence mode="wait">
            <motion.div
              key={index}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 1.2, ease: "easeInOut" }}
              className="w-full"
            >
              <div className="flex flex-col md:flex-row items-stretch h-[65vh] max-h-[550px]">
                {/* Details Section */}
                <div className="w-full md:w-1/2 text-left p-8 md:p-12 flex flex-col justify-center">
                  <div>
                    <p className="font-semibold text-coral mb-4">Top picks</p>
                    <h2 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{topPicksEvents[index].title}</h2>
                    <div className="flex flex-col md:flex-row items-start md:items-center gap-6 text-slate-light mb-6">
                      <p className="flex items-center"><Calendar size={18} className="mr-3 text-coral" /> {topPicksEvents[index].date}</p>
                      <p className="flex items-center"><MapPin size={18} className="mr-3 text-coral" /> {topPicksEvents[index].location}</p>
                    </div>
                    <p className="text-slate-light mb-8 max-w-lg">
                        {topPicksEvents[index].description}
                    </p>
                    <motion.div 
                      className="relative w-fit"
                      whileHover="hover"
                    >
                      <motion.div 
                        className="absolute inset-0 bg-charcoal rounded-lg transform"
                        variants={{ hover: { x: 4, y: 4 } }}
                        transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                      />
                      <button className="relative bg-coral text-white font-semibold py-3 px-6 rounded-lg flex items-center gap-2 border-2 border-charcoal">
                        Get Tickets <ArrowRight size={20} />
                      </button>
                    </motion.div>
                  </div>
                </div>

                {/* Image Section */}
                <div className="w-full md:w-1/2 h-full rounded-2xl overflow-hidden">
                  <img src={topPicksEvents[index].image} alt={topPicksEvents[index].title} className="w-full h-full object-cover" />
                </div>
              </div>
            </motion.div>
        </AnimatePresence>
    </section>
  );
};

export default TopPicksSlider;