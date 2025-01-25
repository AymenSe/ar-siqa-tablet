import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

function Home() {
  const handleGoFullscreen = () => {
    const docEl = document.documentElement; // Target the full webpage
    if (docEl.requestFullscreen) {
      docEl.requestFullscreen();
    } else if ((docEl as any).mozRequestFullScreen) { /* Firefox */
      (docEl as any).mozRequestFullScreen();
    } else if ((docEl as any).webkitRequestFullscreen) { /* Chrome, Safari, Opera */
      (docEl as any).webkitRequestFullscreen();
    } else if ((docEl as any).msRequestFullscreen) { /* IE/Edge */
      (docEl as any).msRequestFullscreen();
    }
  };

  return (
    <motion.div
      className="flex flex-col items-center justify-center min-h-screen bg-gray-100 text-black"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="bg-white p-8 rounded-xl shadow-md max-w-md w-full">
        <h1 className="text-3xl font-bold mb-4 text-center">
          Welcome to the Subjective Quality Experiment
        </h1>
        <p className="text-center mb-6">
          In this experiment, you'll be asked to rate several images.
          Please follow the instructions carefully.
        </p>
        <div className="flex flex-col gap-4">
          {/* Link to start experiment */}
          <Link to="/register">
            <button 
              onClick={handleGoFullscreen}
              className="px-6 py-2 bg-black text-white font-semibold rounded-xl shadow hover:bg-gray-800 transition-all">
              Start Experiment
            </button>
          </Link>
        </div>
      </div>
    </motion.div>
  );
}

export default Home;
