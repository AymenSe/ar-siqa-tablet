import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

function Completion() {
  const navigate = useNavigate();

  const handleGoHome = () => {
    navigate('/');
  };

  return (
    <motion.div
      className="flex flex-col items-center justify-center flex-1 p-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="bg-white p-8 rounded-xl shadow-md w-3/4 text-center">
        <h2 className="text-2xl font-bold mb-4">Thank You!</h2>
        <p className="mb-4 text-gray-600">
          You have completed the experiment. We appreciate your participation.
        </p>
        <button
          onClick={handleGoHome}
          className="px-6 py-2 bg-black text-white font-semibold rounded-2xl shadow hover:bg-gray-800 transition-all"
        >
          Back to Beginning
        </button>
      </div>
    </motion.div>
  );
}

export default Completion;
