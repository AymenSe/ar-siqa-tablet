import React from "react";
import { motion } from "framer-motion";

function Completion() {
  return (
    <motion.div
      className="p-8 text-center"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h2 className="text-2xl font-bold mb-4">Thank You!</h2>
      <p className="mb-4">
        You have completed the experiment. We appreciate your participation.
      </p>
    </motion.div>
  );
}

export default Completion;
