import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

interface Question {
  question_id: number;
  text: string;
  category: string;
}

interface ImageData {
  file_path?: string;
  file_name?: string;
}

interface SessionImage {
  session_image_id: number;
  image?: ImageData;
}

interface Answer {
  question_id: number;
  answer: string;
}

function QuestionCard({
  question,
  onAnswerChange,
}: {
  question: Question;
  onAnswerChange: (answer: Answer) => void;
}) {
  const options = ["Very Bad", "Bad", "Neutral", "Good", "Very Good"]; // Example categorical options

  const handleSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onAnswerChange({ question_id: question.question_id, answer: e.target.value });
  };

  return (
    <div className="p-4 border rounded-lg shadow bg-gray-50">
      <h3 className="font-bold mb-2">{question.text}</h3>
      <select
        onChange={handleSelect}
        className="w-full border rounded p-2"
        defaultValue=""
      >
        <option value="" disabled>
          Select an answer
        </option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
}

function RealSession() {
  const navigate = useNavigate();
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [images, setImages] = useState<SessionImage[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [showQuestions, setShowQuestions] = useState(false);

  useEffect(() => {
    const subject_id = localStorage.getItem("subject_id");
    if (!subject_id) {
      navigate("/register");
      return;
    }
    createRealSession(subject_id);
    fetchQuestions();
  }, [navigate]);

  useEffect(() => {
    setShowQuestions(false); // Hide questions initially
    const timer = setTimeout(() => setShowQuestions(true), 5000); // Show after 5 seconds
    return () => clearTimeout(timer);
  }, [currentIndex]);

  const createRealSession = async (subject_id: string) => {
    try {
      const sessionRes = await axios.post("http://127.0.0.1:8000/sessions", {
        subject_id: parseInt(subject_id, 10),
        session_type: "real",
      });
      setSessionId(sessionRes.data.session_id);

      // Assign images (hard-coded example)
      const imagesToAssign = [1, 2, 3, 4, 5];
      await axios.post(
        `http://127.0.0.1:8000/session-images/${sessionRes.data.session_id}/assign_images`,
        imagesToAssign
      );

      loadRealImages(sessionRes.data.session_id);
    } catch (error) {
      console.error("Error creating real session:", error);
      alert("Could not create real session");
    }
  };

  const loadRealImages = async (sId: number) => {
    try {
      const res = await axios.get<SessionImage[]>(
        "http://127.0.0.1:8000/session-images",
        {
          params: { session_id: sId },
        }
      );
      setImages(res.data);
      setCurrentIndex(0);
    } catch (error) {
      console.error("Error loading images:", error);
      alert("Could not load real session images");
    }
  };

  const fetchQuestions = async () => {
    try {
      const res = await axios.get<Question[]>("http://127.0.0.1:8000/questions");
      setQuestions(res.data);
    } catch (error) {
      console.error("Error fetching questions:", error);
      alert("Could not load questions");
    }
  };

  const handleAnswerChange = (newAnswer: Answer) => {
    setAnswers((prev) => {
      const updated = prev.filter((a) => a.question_id !== newAnswer.question_id);
      updated.push(newAnswer);
      return updated;
    });
  };

  const handleSubmit = async () => {
    if (currentIndex >= images.length) return;

    try {
      await axios.post("http://127.0.0.1:8000/ratings", {
        session_image_id: images[currentIndex].session_image_id,
        ratings: answers,
      });
      setAnswers([]);
      setCurrentIndex((prev) => prev + 1);
    } catch (error) {
      console.error("Error submitting ratings:", error);
      alert("Failed to submit ratings");
    }
  };

  if (currentIndex >= images.length) {
    return (
      <div className="p-8 text-center">
        <h2 className="text-2xl font-bold">Real Session Completed!</h2>
        <button
          onClick={() => navigate("/completion")}
          className="mt-4 px-6 py-2 bg-black text-white rounded shadow"
        >
          Finish Experiment
        </button>
      </div>
    );
  }

  const currentImage = images[currentIndex];
  const imageUrl = `http://127.0.0.1:8000/${currentImage?.image?.file_path}`;

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-lg w-full max-w-3xl text-center">
        <h2 className="text-2xl font-bold mb-4">Real Session</h2>
        <p className="text-gray-600 mb-4">
          Image {currentIndex + 1} of {images.length}
        </p>
        <img
          src={imageUrl}
          alt={currentImage?.image?.file_name}
          className="w-full max-h-96 rounded-lg mb-4 object-contain"
        />
        {!showQuestions && (
          <p className="text-gray-500">Please wait 5 seconds for the questions to appear...</p>
        )}
        {showQuestions && (
          <div className="grid grid-cols-2 gap-4">
            {questions.map((question) => (
              <QuestionCard
                key={question.question_id}
                question={question}
                onAnswerChange={handleAnswerChange}
              />
            ))}
          </div>
        )}
        {showQuestions && (
          <button
            onClick={handleSubmit}
            className="mt-6 px-6 py-2 bg-black text-white rounded shadow"
          >
            Submit
          </button>
        )}
      </div>
    </div>
  );
}

export default RealSession;
