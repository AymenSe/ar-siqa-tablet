import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

function Home() {
  return (
    <motion.div
      className="p-8 flex flex-col items-center justify-center"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="text-3xl font-bold mb-4">
        Welcome to the Subjective Quality Experiment
      </h1>
      <p className="text-center mb-6">
        In this experiment, you'll be asked to rate several images. Please follow the instructions carefully.
      </p>
      <Link to="/register">
        <button className="px-6 py-2 bg-blue-500 text-white font-semibold rounded-2xl shadow-md hover:bg-blue-600 transition-all">
          Start Experiment
        </button>
      </Link>
    </motion.div>
  );
}

export default Home;
