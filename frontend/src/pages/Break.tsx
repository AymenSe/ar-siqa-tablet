import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

function Break() {
  const navigate = useNavigate();

  const handleContinue = () => {
    navigate('/real');
  };

  return (
    <motion.div
      className="flex flex-col items-center justify-center flex-1 p-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="bg-white p-8 rounded-xl shadow-md w-3/4 text-center">
        <h2 className="text-2xl font-bold mb-4">Break Time</h2>
        <p className="mb-4 text-gray-600">
          You can relax for a moment. Click the button below when you're ready to continue.
        </p>
        <button
          onClick={handleContinue}
          className="px-6 py-2 bg-black text-white font-semibold rounded-2xl shadow hover:bg-gray-800 transition-all"
        >
          Continue to Real Session
        </button>
      </div>
    </motion.div>
  );
}

export default Break;
