import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import TopPicksSlider from './TopPicksSlider';

const HeroSection = () => {
  const [introAnimationComplete, setIntroAnimationComplete] = useState(false);

  const title = "Event Horizon";
  const titleVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.2 } },
  };
  const charVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <section className="h-screen w-full flex flex-col items-center justify-center relative overflow-hidden">
      <AnimatePresence>
        {!introAnimationComplete ? (
          <motion.div
            key="intro-title"
            exit={{ opacity: 0, y: -50 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="text-center"
          >
            <motion.h1
              variants={titleVariants}
              initial="hidden"
              animate="visible"
              onAnimationComplete={() => setTimeout(() => setIntroAnimationComplete(true), 1500)}
              className="text-6xl md:text-8xl font-extrabold tracking-tight mb-4 z-10"
            >
              {title.split("").map((char, index) => (
                <motion.span key={index} variants={charVariants} className="inline-block">
                  {char === " " ? "\u00A0" : char}
                </motion.span>
              ))}
            </motion.h1>
          </motion.div>
        ) : (
          <TopPicksSlider key="top-picks" />
        )}
      </AnimatePresence>
    </section>
  );
};

export default HeroSection;