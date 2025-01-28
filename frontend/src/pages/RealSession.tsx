import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';

interface ImageData {
  file_path?: string;
  file_name?: string;
}

interface SessionImage {
  session_image_id: number;
  image?: ImageData;
}

function RealSession() {
  const navigate = useNavigate();
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [images, setImages] = useState<SessionImage[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [ratingValue, setRatingValue] = useState<number>(3);
  const [showSlider, setShowSlider] = useState(false);

  useEffect(() => {
    const subject_id = localStorage.getItem('subject_id');
    if (!subject_id) {
      navigate('/register');
      return;
    }
    createRealSession(subject_id);
  }, [navigate]);

  useEffect(() => {
    setShowSlider(false);
    const timer = setTimeout(() => setShowSlider(true), 5000);
    return () => clearTimeout(timer);
  }, [currentIndex]);

  const createRealSession = async (subject_id: string) => {
    try {
      const res = await axios.post('http://127.0.0.1:8000/sessions', {
        subject_id: parseInt(subject_id, 10),
        session_type: 'real'
      });
      setSessionId(res.data.session_id);

      // Assign images
      const imagesToAssign = [1, 2, 3, 4, 5];
      await axios.post(
        `http://127.0.0.1:8000/session-images/${res.data.session_id}/assign_images`,
        imagesToAssign
      );

      // Load images
      loadRealImages(res.data.session_id);
    } catch (error) {
      console.error(error);
      alert('Could not create real session');
    }
  };

  const loadRealImages = async (sId: number) => {
    try {
      const res = await axios.get<SessionImage[]>('http://127.0.0.1:8000/session-images', {
        params: { session_id: sId }
      });
      setImages(res.data);
      setCurrentIndex(0);
    } catch (error) {
      console.error(error);
      alert('Could not load real images');
    }
  };

  const handleRatingSubmit = async () => {
    if (currentIndex >= images.length) return;
    const sessionImage = images[currentIndex];
    try {
      await axios.post('http://127.0.0.1:8000/ratings', {
        session_image_id: sessionImage.session_image_id,
        question_id: 1,
        rating_value: ratingValue,
        text_answer: null,
        response_time: 3.0
      });
      // Next
      setCurrentIndex((prev) => prev + 1);
    } catch (error) {
      console.error(error);
      alert('Failed to submit rating');
    }
  };

  if (sessionId === null) {
    return <div className="p-8">Loading Real Session...</div>;
  }

  if (!images.length) {
    return <div className="p-8">No real images assigned</div>;
  }

  if (currentIndex >= images.length) {
    return (
      <motion.div
        className="flex flex-col items-center justify-center flex-1 p-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="bg-white p-8 rounded-xl shadow-md w-3/4 text-center">
          <h2 className="text-2xl font-bold mb-4">Real Session Completed!</h2>
          <button
            onClick={() => navigate('/completion')}
            className="px-6 py-2 bg-black text-white font-semibold rounded-2xl shadow hover:bg-gray-800 transition-all"
          >
            Finish Experiment
          </button>
        </div>
      </motion.div>
    );
  }

  const currentImage = images[currentIndex];
  const imageUrl = `http://127.0.0.1:8000/${currentImage.image?.file_path || ''}`;

  const ratingLabels = ["Bad", "Poor", "Fair", "Good", "Perfect"];

  return (
    <motion.div
      className="flex flex-col flex-1 p-0"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Main Content */}
      <div className="relative flex justify-center items-center h-screen w-screen">
        {/* Image (Fullscreen) */}
        {!showSlider ? (
          <img
            src={imageUrl}
            alt={currentImage.image?.file_name || "training_image"}
            className="absolute inset-0 h-full w-full object-cover"
          />
        ) : (
          /* Slider Content */
          <div
            className="absolute inset-0 flex flex-col justify-center items-center"
          >
          <p className="text-gray-600 font-bold text-center ">Real Session | Image {currentIndex + 1} of {images.length}</p>
          <hr className="mb-6" />

            <p className="text-2xl font-bold text-black mb-6">
              How do you rate the quality?
            </p>

            <div className="w-2/4 relative mb-6">
              <input
                id="large-range"
                type="range"
                min={1}
                max={5}
                step={1}
                value={ratingValue}
                onChange={(e) => setRatingValue(Number(e.target.value))}
                className="w-full h-3 bg-gray rounded-lg appearance-none cursor-pointer range-lg dark:bg-gray-700"
                style={{
                  accentColor: "blue",
                }}
              />
              <span className="text-sm text-gray-600 dark:text-gray-500 font-bold absolute start-0 -bottom-6">Bad</span>
              <span className="text-sm text-gray-600 dark:text-gray-500 font-bold absolute start-1/4 -translate-x-1/2 rtl:translate-x-1/2 -bottom-6">Poor</span>
              <span className="text-sm text-gray-600 dark:text-gray-500 font-bold absolute start-2/4 -translate-x-1/2 rtl:translate-x-1/2 -bottom-6">Fair</span>
              <span className="text-sm text-gray-600 dark:text-gray-500 font-bold absolute start-3/4 -translate-x-1/2 rtl:translate-x-1/2 -bottom-6">Good</span>
              <span className="text-sm text-gray-600 dark:text-gray-500 font-bold absolute end-0 -bottom-6">Perfect</span>
            </div>

            <p className="text-sm text-black font-bold mt-4">
              The precieved qaulity is {ratingLabels[ratingValue - 1]}
            </p>

            {/* Submit Button */}
            <button
              onClick={handleRatingSubmit}
              className="px-6 py-2 mt-6 bg-black text-white font-semibold rounded-2xl shadow hover:bg-gray-800 transition-all"
            >
              Submit & Next
            </button>
          </div>
        )}
      </div>
    </motion.div>

  );
}

export default RealSession;
