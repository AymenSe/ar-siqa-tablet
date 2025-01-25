import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import axios from "axios";

function SubjectRegistration() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    age: "",
    gender: ""
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  // Submits data to FastAPI endpoint, then navigates to training
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // POST to your FastAPI endpoint for creating a subject
      const res = await axios.post("http://127.0.0.1:8000/subjects", {
        name: formData.name,
        age: parseInt(formData.age, 10),
        gender: formData.gender
      });
      // We get the created subject data (with subject_id)
      const subject = res.data;
      // Save subject_id in local storage
      localStorage.setItem("subject_id", subject.subject_id);

      // Next step: navigate to training
      navigate("/training");
    } catch (error) {
      console.error(error);
      alert("Failed to register subject. Check console for details.");
    }
  };

  return (
    <motion.div
      className="p-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h2 className="text-2xl font-bold mb-4">Subject Registration</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1 font-medium">Name:</label>
          <input
            className="border border-gray-300 rounded-lg p-2 w-full"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">Age:</label>
          <input
            className="border border-gray-300 rounded-lg p-2 w-full"
            name="age"
            type="number"
            value={formData.age}
            onChange={handleChange}
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">Gender:</label>
          <input
            className="border border-gray-300 rounded-lg p-2 w-full"
            name="gender"
            value={formData.gender}
            onChange={handleChange}
          />
        </div>
        <button
          type="submit"
          className="px-6 py-2 bg-green-500 text-white font-semibold rounded-2xl shadow-md hover:bg-green-600 transition-all"
        >
          Start Training
        </button>
      </form>
    </motion.div>
  );
}

export default SubjectRegistration;
