import { Link } from "react-router-dom";
import { motion } from "framer-motion";

function Home() {
  const handleGoFullscreen = () => {
    const docEl = document.documentElement; // Target the full webpage
    if (docEl.requestFullscreen) {
      docEl.requestFullscreen();
    } else if ((docEl as any).mozRequestFullScreen) {
      // Firefox
      (docEl as any).mozRequestFullScreen();
    } else if ((docEl as any).webkitRequestFullscreen) {
      // Chrome, Safari, Opera
      (docEl as any).webkitRequestFullscreen();
    } else if ((docEl as any).msRequestFullscreen) {
      // IE/Edge
      (docEl as any).msRequestFullscreen();
    }
  };

  return (
    <motion.div
      className="w-full flex flex-col items-center justify-center min-h-screen bg-gray-50 text-black"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="bg-white p-10 rounded-2xl shadow-lg w-3/4">
        <h1 className="font-extrabold mb-6 text-center text-gray-900">
          Welcome to the Subjective Quality Experiment
        </h1>
        <p className="text-lg text-center text-gray-600 mb-8">
          In this experiment, you'll be asked to rate several images. Please
          follow the instructions carefully.
        </p>
        <div className="flex justify-center">
          <Link to="/register">
            <button
              onClick={handleGoFullscreen}
              className="px-8 py-3 bg-black text-white text-lg font-semibold rounded-lg shadow-lg hover:bg-gray-800 transition-transform transform hover:scale-105"
            >
              Start Experiment
            </button>
          </Link>
        </div>
      </div>
    </motion.div>
  );
}

export default Home;
