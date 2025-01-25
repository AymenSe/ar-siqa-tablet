import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import SubjectRegistration from './pages/SubjectRegistration';
import TrainingSession from './pages/TrainingSession';
import Break from './pages/Break';
import RealSession from './pages/RealSession';
import Completion from './pages/Completion';

function App() {
  return (
    <div className="w-screen min-h-screen bg-gray-100 text-black flex flex-col">
      {/* 
        A full-screen flex container with a gray background 
        and black text, ensuring everything spans the entire page. 
      */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<SubjectRegistration />} />
          <Route path="/training" element={<TrainingSession />} />
          <Route path="/break" element={<Break />} />
          <Route path="/real" element={<RealSession />} />
          <Route path="/completion" element={<Completion />} />
        </Routes>
      </div>
    
  );
}

export default App;
