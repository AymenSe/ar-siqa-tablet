import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';

interface ImageData {
  file_path?: string;
  file_name?: string;
}

interface SessionImage {
  session_image_id: number;
  image?: ImageData;
}

function TrainingSession() {
  const navigate = useNavigate();
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [images, setImages] = useState<SessionImage[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [ratingValue, setRatingValue] = useState<number>(3);
  const [showSlider, setShowSlider] = useState(false);

  const createTrainingSession = useCallback(async (subject_id: string) => {
    try {
      // 1. Create a training session
      const sessionRes = await axios.post('http://127.0.0.1:8000/sessions', {
        subject_id: parseInt(subject_id, 10),
        session_type: 'training'
      });
      setSessionId(sessionRes.data.session_id);

      // 2. Assign images to the session (hard-coded example)
      const imagesToAssign = [1, 2, 3, 4, 5];
      await axios.post(
        `http://127.0.0.1:8000/session-images/${sessionRes.data.session_id}/assign_images`,
        imagesToAssign
      );

      // 3. Load images
      loadTrainingImages(sessionRes.data.session_id);
    } catch (error) {
      console.error('Error in creating/assigning training session:', error);
      alert('Could not create or assign images for training session');
    }
  }, []);

  const loadTrainingImages = async (sId: number) => {
    try {
      const res = await axios.get<SessionImage[]>('http://127.0.0.1:8000/session-images', {
        params: { session_id: sId }
      });
      setImages(res.data);
      setCurrentIndex(0);
    } catch (error) {
      console.error(error);
      alert('Could not load training images');
    }
  };

  useEffect(() => {
    const subject_id = localStorage.getItem('subject_id');
    if (!subject_id) {
      navigate('/register');
      return;
    }
    createTrainingSession(subject_id);
  }, [navigate, createTrainingSession]);

  // Hide slider for 5s each time a new image is loaded
  useEffect(() => {
    setShowSlider(false);
    const timer = setTimeout(() => setShowSlider(true), 5000);
    return () => clearTimeout(timer);
  }, [currentIndex]);

  const handleRatingSubmit = async () => {
    if (currentIndex >= images.length) return;
    const sessionImage = images[currentIndex];
    try {
      await axios.post('http://127.0.0.1:8000/ratings', {
        session_image_id: sessionImage.session_image_id,
        question_id: 1,
        rating_value: ratingValue,
        text_answer: null,
        response_time: 2.5
      });
      // Next
      setCurrentIndex((prev) => prev + 1);
    } catch (error) {
      console.error(error);
      alert('Failed to submit rating');
    }
  };

  if (sessionId === null) {
    return <div className="p-8">Loading Training Session...</div>;
  }

  if (!images.length) {
    return <div className="p-8">No training images assigned</div>;
  }

  if (currentIndex >= images.length) {
    // Done
    return (
      <motion.div
        className="flex flex-col items-center justify-center flex-1 p-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="bg-white p-8 rounded-xl shadow-md text-center">
          <h2 className="text-2xl font-bold mb-4">Training Completed!</h2>
          <button
            onClick={() => navigate('/break')}
            className="px-6 py-2 bg-black text-white font-semibold rounded-2xl shadow hover:bg-gray-800 transition-all"
          >
            Proceed to Break
          </button>
        </div>
      </motion.div>
    );
  }

  const currentImage = images[currentIndex];
  const imageUrl = `http://127.0.0.1:8000/${currentImage.image?.file_path || ''}`;

  return (
    <motion.div
      className="flex flex-col items-center justify-center flex-1 p-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="bg-white p-8 rounded-xl shadow-md flex flex-col items-center">
        <h2 className="text-2xl font-bold mb-2">Training Session</h2>
        <p className="text-gray-600 mb-4">Image {currentIndex + 1} of {images.length}</p>
        <img
          src={imageUrl}
          alt={currentImage.image?.file_name || 'training_image'}
          className="w-full rounded-xl mb-4"
          style={{ maxHeight: '512px', objectFit: 'contain' }}
        />
        {!showSlider && (
          <p className="mb-4 text-gray-500">Please wait 5 seconds before rating...</p>
        )}
        {showSlider && (
          <div className="flex flex-col items-center w-full">
            <input
              type="range"
              min={1}
              max={5}
              step={1}
              value={ratingValue}
              onChange={(e) => setRatingValue(Number(e.target.value))}
              className="w-1/2 mb-2"
            />
            <p className="font-medium mb-4">Current Rating: {ratingValue}</p>
            <button
              onClick={handleRatingSubmit}
              className="px-6 py-2 bg-black text-white font-semibold rounded-2xl shadow hover:bg-gray-800 transition-all"
            >
              Submit Rating
            </button>
          </div>
        )}
      </div>
    </motion.div>
  );
}

export default TrainingSession;
