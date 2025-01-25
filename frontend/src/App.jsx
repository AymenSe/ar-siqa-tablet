import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";

// Import your page components
import Home from "./pages/Home";
import SubjectRegistration from "./pages/SubjectRegistration";
import TrainingSession from "./pages/TrainingSession";
import Break from "./pages/Break";
import RealSession from "./pages/RealSession";
import Completion from "./pages/Completion";

function App() {
  return (
      <div className="min-h-screen bg-gray-50 text-gray-800">
        {/* Simple top nav bar (Optional) */}
        <nav className="p-4 bg-white shadow flex items-center justify-between">
          <Link to="/" className="text-xl font-bold hover:text-blue-600">
            SQ Experiment
          </Link>
          <div className="space-x-4">
            <Link to="/register" className="hover:text-blue-600">
              Register
            </Link>
            <Link to="/training" className="hover:text-blue-600">
              Training
            </Link>
            <Link to="/break" className="hover:text-blue-600">
              Break
            </Link>
            <Link to="/real" className="hover:text-blue-600">
              Real
            </Link>
          </div>
        </nav>

        {/* Main content area (Routes) */}
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
