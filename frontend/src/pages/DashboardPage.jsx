import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { User, Target, BookOpen, AlertTriangle, CheckCircle2, ArrowRight, Sparkles, Filter } from 'lucide-react';
import { api } from '../services/api';
import CourseCard from '../components/CourseCard';
import CourseModal from '../components/CourseModal';
import ExplanationModal from '../components/ExplanationModal';

export default function DashboardPage({ activeStudent, setActiveStudent }) {
  const [students, setStudents] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCourseDetails, setSelectedCourseDetails] = useState(null);
  const [selectedCourseExplanation, setSelectedCourseExplanation] = useState(null);

  useEffect(() => {
    fetchStudents();
  }, []);

  useEffect(() => {
    if (activeStudent) {
      fetchRecommendations(activeStudent.student_id);
    }
  }, [activeStudent]);

  const fetchStudents = async () => {
    const res = await api.getStudents();
    const list = res.data || [];
    setStudents(list);
    if (!activeStudent && list.length > 0) {
      setActiveStudent(list[0]);
    }
  };

  const fetchRecommendations = async (studentId) => {
    setLoading(true);
    const res = await api.getRecommendations(studentId);
    setRecommendations(res.data || []);
    setLoading(false);
  };

  const handleSelectStudent = (e) => {
    const sId = e.target.value;
    const match = students.find(s => s.student_id === sId);
    if (match) {
      setActiveStudent(match);
    }
  };

  const eligibleCount = recommendations.filter(r => r.eligibility_status === 'ELIGIBLE').length;
  const missingPrereqCount = recommendations.filter(r => r.eligibility_status === 'MISSING_PREREQUISITES').length;
  const conflictCount = recommendations.filter(r => r.eligibility_status === 'SCHEDULE_CONFLICT').length;

  return (
    <div className="space-y-8 pb-12">
      
      {/* Header Panel */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-panel p-6 rounded-2xl border border-slate-800">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white">Student Dashboard</h1>
          <p className="text-xs text-slate-400 mt-1">Real-time prerequisite & elective recommendation summary</p>
        </div>

        {/* Student Selector */}
        <div className="flex items-center gap-3 bg-slate-900/80 p-2.5 rounded-xl border border-slate-800">
          <User className="w-4 h-4 text-sky-400" />
          <div className="flex flex-col">
            <span className="text-[10px] text-slate-400 font-mono">Select Student Profile</span>
            <select
              value={activeStudent?.student_id || ''}
              onChange={handleSelectStudent}
              className="bg-transparent text-xs font-bold text-white outline-none cursor-pointer"
            >
              {students.map(s => (
                <option key={s.student_id} value={s.student_id} className="bg-slate-900 text-slate-100">
                  {s.name} ({s.student_id}) — {s.career_goal || 'No Goal'}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Card 1: Active Student Goal */}
        <div className="glass-card p-5 rounded-xl border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-400 font-medium">Career Goal</p>
            <h3 className="text-lg font-bold text-white truncate max-w-[150px]">
              {activeStudent?.career_goal || 'Not Selected'}
            </h3>
            <span className="text-[10px] text-sky-400">Semester {activeStudent?.semester || 1}</span>
          </div>
          <div className="w-10 h-10 rounded-xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400">
            <Target className="w-5 h-5" />
          </div>
        </div>

        {/* Card 2: Eligible Electives */}
        <div className="glass-card p-5 rounded-xl border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-400 font-medium">Eligible Electives</p>
            <h3 className="text-2xl font-extrabold text-emerald-400">{eligibleCount}</h3>
            <span className="text-[10px] text-slate-400">Prerequisites Satisfied</span>
          </div>
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <CheckCircle2 className="w-5 h-5" />
          </div>
        </div>

        {/* Card 3: Missing Prerequisites */}
        <div className="glass-card p-5 rounded-xl border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-400 font-medium">Missing Prerequisites</p>
            <h3 className="text-2xl font-extrabold text-rose-400">{missingPrereqCount}</h3>
            <span className="text-[10px] text-slate-400 font-mono">Requires Foundational Units</span>
          </div>
          <div className="w-10 h-10 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400">
            <AlertTriangle className="w-5 h-5" />
          </div>
        </div>

        {/* Card 4: Schedule Conflicts */}
        <div className="glass-card p-5 rounded-xl border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-400 font-medium">Timetable Conflicts</p>
            <h3 className="text-2xl font-extrabold text-amber-400">{conflictCount}</h3>
            <span className="text-[10px] text-slate-400">Overlapping Timeslots</span>
          </div>
          <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
            <Filter className="w-5 h-5" />
          </div>
        </div>

      </div>

      {/* Top Recommended Electives Section */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-sky-400" />
            <h2 className="text-xl font-bold text-white">Top Recommended Electives for {activeStudent?.name}</h2>
          </div>
          
          <Link
            to="/explorer"
            className="text-xs font-semibold text-sky-400 hover:text-sky-300 flex items-center gap-1 group"
          >
            <span>View All {recommendations.length} Courses</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        {loading ? (
          <div className="glass-panel p-12 rounded-2xl text-center text-slate-400 animate-pulse">
            Analyzing student prerequisites, schedules, and career pathways...
          </div>
        ) : recommendations.length === 0 ? (
          <div className="glass-panel p-8 rounded-2xl text-center text-slate-400">
            No course recommendations generated. Ensure completed courses are saved.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {recommendations.slice(0, 4).map((c) => (
              <CourseCard
                key={c.course_id}
                course={c}
                onOpenDetails={setSelectedCourseDetails}
                onOpenExplanation={setSelectedCourseExplanation}
              />
            ))}
          </div>
        )}
      </div>

      {/* Course Detail Modal */}
      {selectedCourseDetails && (
        <CourseModal
          course={selectedCourseDetails}
          onClose={() => setSelectedCourseDetails(null)}
          onOpenExplanation={(c) => {
            setSelectedCourseDetails(null);
            setSelectedCourseExplanation(c);
          }}
        />
      )}

      {/* Explanation Modal */}
      {selectedCourseExplanation && (
        <ExplanationModal
          course={selectedCourseExplanation}
          onClose={() => setSelectedCourseExplanation(null)}
        />
      )}

    </div>
  );
}
