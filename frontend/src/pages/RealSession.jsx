import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import axios from "axios";

function RealSession() {
  const navigate = useNavigate();
  const [sessionId, setSessionId] = useState(null);
  const [images, setImages] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [ratingValue, setRatingValue] = useState("");

  useEffect(() => {
    const subject_id = localStorage.getItem("subject_id");
    if (!subject_id) {
      navigate("/register");
      return;
    }
    createRealSession(subject_id);
  }, [navigate]);

  const createRealSession = async (subject_id) => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/sessions", {
        subject_id: parseInt(subject_id, 10),
        session_type: "real"
      });
      setSessionId(res.data.session_id);

      // 2. Assign images to the session (hard-coded example)
      const imagesToAssign = [1, 2, 3, 4, 5];
      await axios.post(
        `http://127.0.0.1:8000/session-images/${res.data.session_id}/assign_images`,
        imagesToAssign
      );

      // Load images for the session
      loadRealImages(res.data.session_id);
    } catch (error) {
      console.error(error);
      alert("Could not create real session");
    }
  };

  const loadRealImages = async (sId) => {
    try {
      // fetch images assigned for the real session
      const res = await axios.get("http://127.0.0.1:8000/session-images", {
        params: { session_id: sId }
      });
      setImages(res.data);
      setCurrentIndex(0);
    } catch (error) {
      console.error(error);
      alert("Could not load real images");
    }
  };

  const handleRatingSubmit = async () => {
    if (currentIndex >= images.length) return;

    const sessionImage = images[currentIndex];
    try {
      await axios.post("http://127.0.0.1:8000/ratings", {
        session_image_id: sessionImage.session_image_id,
        question_id: 1,
        rating_value: parseFloat(ratingValue),
        text_answer: null,
        response_time: 3.0
      });
      // Move to the next
      setRatingValue("");
      setCurrentIndex((prev) => prev + 1);
    } catch (error) {
      console.error(error);
      alert("Failed to submit rating");
    }
  };

  if (!sessionId) {
    return <div className="p-8">Loading Real Session...</div>;
  }

  if (!images.length) {
    return <div className="p-8">No real images assigned</div>;
  }

  if (currentIndex >= images.length) {
    // done with real session
    return (
      <motion.div
        className="p-8 text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-2xl font-bold mb-4">Real Session Completed!</h2>
        <button
          onClick={() => navigate("/completion")}
          className="px-6 py-2 bg-purple-500 text-white font-semibold rounded-2xl shadow-md hover:bg-purple-600 transition-all"
        >
          Finish Experiment
        </button>
      </motion.div>
    );
  }

  const currentImage = images[currentIndex];
  const imageUrl = `http://127.0.0.1:8000/${currentImage.image?.file_path || ""}`;

  return (
    <motion.div
      className="p-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h2 className="text-2xl font-bold mb-2">Real Session</h2>
      <p className="mb-4">
        Image {currentIndex + 1} of {images.length}
      </p>
      <img
        src={imageUrl}
        alt={currentImage.image?.file_name || "real_image"}
        className="max-w-md mx-auto mb-4 rounded-2xl shadow-lg"
      />
      <div className="flex items-center justify-center mb-4">
        <label className="mr-2">Rating (1-5): </label>
        <input
          type="number"
          min="1"
          max="5"
          value={ratingValue}
          onChange={(e) => setRatingValue(e.target.value)}
          className="border border-gray-300 rounded-lg p-2 w-20 mr-2 text-center"
        />
        <button
          onClick={handleRatingSubmit}
          className="px-4 py-2 bg-green-500 text-white font-semibold rounded-2xl shadow-md hover:bg-green-600 transition-all"
        >
          Submit Rating
        </button>
      </div>
    </motion.div>
  );
}

export default RealSession;
