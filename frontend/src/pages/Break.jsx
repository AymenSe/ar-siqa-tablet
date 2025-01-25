import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

function Break() {
  const navigate = useNavigate();

  const handleContinue = () => {
    // proceed to real session
    navigate("/real");
  };

  return (
    <motion.div
      className="p-8 text-center"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h2 className="text-2xl font-bold mb-4">Break Time</h2>
      <p className="mb-4">
        You can relax for a moment. Click the button below when you're ready to continue.
      </p>
      <button
        onClick={handleContinue}
        className="px-6 py-2 bg-blue-500 text-white font-semibold rounded-2xl shadow-md hover:bg-blue-600 transition-all"
      >
        Continue to Real Session
      </button>
    </motion.div>
  );
}

export default Break;
