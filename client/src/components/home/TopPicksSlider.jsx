import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Calendar, MapPin, ArrowRight } from 'lucide-react';

const TopPicksSlider = () => {
  const [topPicks, setTopPicks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const fetchTopPicks = async () => {
      try {
        // UPDATED: Changed to a relative path
        const response = await fetch('/api/events/top-picks');
        const data = await response.json();
        if (response.ok) {
          setTopPicks(data);
        } else {
          throw new Error(data.error || 'Failed to fetch top picks');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchTopPicks();
  }, []);

  useEffect(() => {
    if (topPicks.length === 0) return;
    const timer = setTimeout(() => {
      setIndex((prevIndex) => (prevIndex + 1) % topPicks.length);
    }, 15000); // Change slide every 15 seconds
    return () => clearTimeout(timer);
  }, [index, topPicks]);

  if (loading) {
    return <section className="w-full pt-24 md:pt-32 container mx-auto px-6 h-[65vh] flex items-center justify-center"><p>Loading top events...</p></section>;
  }
  
  if (error) {
     return <section className="w-full pt-24 md:pt-32 container mx-auto px-6 h-[65vh] flex items-center justify-center"><p className="text-red-500">Error: {error}</p></section>;
  }

  if (topPicks.length === 0) {
      return <section className="w-full pt-24 md:pt-32 container mx-auto px-6 h-[65vh] flex items-center justify-center"><p>No top picks available right now. Check back soon!</p></section>;
  }
  
  const currentEvent = topPicks[index];

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
                <div className="w-full md:w-1/2 text-left p-8 md:p-12 flex flex-col justify-center">
                  <div>
                    <p className="font-semibold text-coral mb-4">Top picks from our staff</p>
                    <h2 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{currentEvent.title}</h2>
                    <div className="flex flex-col md:flex-row items-start md:items-center gap-6 text-slate-light mb-6">
                      <p className="flex items-center"><Calendar size={18} className="mr-3 text-coral" /> {new Date(currentEvent.date).toLocaleDateString('en-US', { month: 'short', day: '2-digit' })}</p>
                      <p className="flex items-center"><MapPin size={18} className="mr-3 text-coral" /> {currentEvent.location}</p>
                    </div>
                    <p className="text-slate-light mb-8 max-w-lg">
                        {currentEvent.short_description}
                    </p>
                    <Link to="/login?mode=login">
                        <motion.div 
                          className="relative w-fit"
                          whileHover="hover"
                        >
                          <motion.div 
                            className="absolute inset-0 bg-charcoal rounded-lg transform"
                            variants={{ hover: { x: 4, y: 4 } }}
                            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                          />
                          <button
                            className="relative bg-coral text-white font-semibold py-3 px-6 rounded-lg flex items-center gap-2 border-2 border-charcoal"
                          >
                            Get Tickets <ArrowRight size={20} />
                          </button>
                        </motion.div>
                    </Link>
                  </div>
                </div>
                <div className="w-full md:w-1/2 h-full rounded-2xl overflow-hidden">
                  <img src={currentEvent.image_url || 'https://placehold.co/1200x900/A491D3/FFFFFF?text=Event'} alt={currentEvent.title} className="w-full h-full object-cover" />
                </div>
              </div>
            </motion.div>
        </AnimatePresence>
    </section>
  );
};

export default TopPicksSlider;
