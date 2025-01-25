import { useState, ChangeEvent, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';

interface FormData {
  name: string;
  age: string;
  gender: string;
}

function SubjectRegistration() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    name: '',
    age: '',
    gender: ''
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://127.0.0.1:8000/subjects', {
        name: formData.name,
        age: parseInt(formData.age, 10),
        gender: formData.gender
      });
      const subject = res.data;
      localStorage.setItem('subject_id', subject.subject_id);

      navigate('/training');
    } catch (error) {
      console.error(error);
      alert('Failed to register subject. Check console for details.');
    }
  };

  return (
    <motion.div
      className="flex flex-col items-center justify-center flex-1 p-4"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="bg-white p-8 rounded-xl shadow-md w-3/4">
        <h2 className="text-2xl font-bold mb-4">Subject Registration</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 font-medium">Name:</label>
            <input
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="border border-gray-300 rounded-lg p-2 w-full"
            />
          </div>
          <div>
            <label className="block mb-1 font-medium">Age:</label>
            <input
              name="age"
              type="number"
              value={formData.age}
              onChange={handleChange}
              className="border border-gray-300 rounded-lg p-2 w-full"
            />
          </div>
          <div>
            <label className="block mb-1 font-medium">Gender:</label>
            <input
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              className="border border-gray-300 rounded-lg p-2 w-full"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-2 bg-black text-white font-semibold rounded-2xl shadow hover:bg-gray-800 transition-all"
          >
            Start Training
          </button>
        </form>
      </div>
    </motion.div>
  );
}

export default SubjectRegistration;
