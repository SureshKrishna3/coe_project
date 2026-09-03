import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import DashboardPage from './pages/DashboardPage';
import StudentProfilePage from './pages/StudentProfilePage';
import ElectiveExplorerPage from './pages/ElectiveExplorerPage';
import CareerPathwayPage from './pages/CareerPathwayPage';
import EvaluationDashboardPage from './pages/EvaluationDashboardPage';
import InstructorPage from './pages/InstructorPage';
import StakeholderValidationPage from './pages/StakeholderValidationPage';
import { api } from './services/api';
import { offlineCache } from './services/offlineCache';

export default function App() {
  const [activeStudent, setActiveStudent] = useState(null);
  const [isOffline, setIsOffline] = useState(!navigator.onLine);

  useEffect(() => {
    // Check network connectivity status
    const handleOnline = () => setIsOffline(false);
    const handleOffline = () => setIsOffline(true);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Initial student load
    loadInitialStudent();

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const loadInitialStudent = async () => {
    const cached = offlineCache.getActiveStudent();
    if (cached) {
      setActiveStudent(cached);
    } else {
      const res = await api.getStudents();
      if (res.data && res.data.length > 0) {
        setActiveStudent(res.data[0]);
        offlineCache.saveActiveStudent(res.data[0]);
      }
    }
  };

  const handleSetActiveStudent = (student) => {
    setActiveStudent(student);
    if (student) {
      offlineCache.saveActiveStudent(student);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
        
        {/* Navigation Header */}
        <Navbar activeStudent={activeStudent} isOffline={isOffline} />

        {/* Offline Alert Banner */}
        {isOffline && (
          <div className="bg-amber-500/10 border-b border-amber-500/30 px-4 py-2 text-center text-xs text-amber-300 font-medium">
            Offline Mode — Using locally cached course catalog and recommendations.
          </div>
        )}

        {/* Main Content View */}
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 pt-6">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<DashboardPage activeStudent={activeStudent} setActiveStudent={handleSetActiveStudent} />} />
            <Route path="/profile" element={<StudentProfilePage activeStudent={activeStudent} setActiveStudent={handleSetActiveStudent} />} />
            <Route path="/explorer" element={<ElectiveExplorerPage activeStudent={activeStudent} />} />
            <Route path="/career-pathway" element={<CareerPathwayPage activeStudent={activeStudent} />} />
            <Route path="/evaluation" element={<EvaluationDashboardPage />} />
            <Route path="/instructor" element={<InstructorPage />} />
            <Route path="/validation" element={<StakeholderValidationPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-900 bg-slate-950/80 py-6 text-center text-xs text-slate-500">
          <p>© 2026 Vocational Elective Explorer — Explainable Prerequisite & Career-Consequence Navigator.</p>
        </footer>

      </div>
    </Router>
  );
}
