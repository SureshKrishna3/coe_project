import React, { useState, useEffect } from 'react';
import { Search, Filter, Sparkles, CheckCircle2, AlertTriangle, XCircle, Info } from 'lucide-react';
import { api } from '../services/api';
import CourseCard from '../components/CourseCard';
import CourseModal from '../components/CourseModal';
import ExplanationModal from '../components/ExplanationModal';

export default function ElectiveExplorerPage({ activeStudent }) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');

  const [selectedCourseDetails, setSelectedCourseDetails] = useState(null);
  const [selectedCourseExplanation, setSelectedCourseExplanation] = useState(null);

  useEffect(() => {
    if (activeStudent) {
      loadRecommendations(activeStudent.student_id);
    }
  }, [activeStudent]);

  const loadRecommendations = async (sId) => {
    setLoading(true);
    const res = await api.getRecommendations(sId);
    setRecommendations(res.data || []);
    setLoading(false);
  };

  // Filter evaluation results
  const filtered = recommendations.filter((c) => {
    const matchesSearch = c.course_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          c.course_id.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesCategory = categoryFilter === 'ALL' || c.category.toLowerCase() === categoryFilter.toLowerCase();
    
    let matchesStatus = true;
    if (statusFilter === 'ELIGIBLE') matchesStatus = c.eligibility_status === 'ELIGIBLE';
    if (statusFilter === 'MISSING_PREREQ') matchesStatus = c.eligibility_status === 'MISSING_PREREQUISITES';
    if (statusFilter === 'CONFLICT') matchesStatus = c.eligibility_status === 'SCHEDULE_CONFLICT';

    return matchesSearch && matchesCategory && matchesStatus;
  });

  const categories = Array.from(new Set(recommendations.map(r => r.category)));

  return (
    <div className="space-y-8 pb-12">
      
      {/* Header Panel */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-sky-400" />
            <span>Elective Explorer</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Analyzing courses for <strong className="text-sky-300">{activeStudent?.name || 'Guest'}</strong> (Target Goal: <strong className="text-white">{activeStudent?.career_goal || 'Software Engineer'}</strong>)
          </p>
        </div>

        {/* Color Legend */}
        <div className="flex flex-wrap items-center gap-2 text-[11px] bg-slate-900/80 p-2.5 rounded-xl border border-slate-800">
          <span className="font-semibold text-slate-400 mr-1">Status Legend:</span>
          <span className="px-2 py-0.5 rounded-md bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> Eligible / Recommended
          </span>
          <span className="px-2 py-0.5 rounded-md bg-amber-500/15 text-amber-400 border border-amber-500/30 flex items-center gap-1">
            <AlertTriangle className="w-3 h-3" /> Schedule Conflict
          </span>
          <span className="px-2 py-0.5 rounded-md bg-rose-500/15 text-rose-400 border border-rose-500/30 flex items-center gap-1">
            <XCircle className="w-3 h-3" /> Missing Prereqs
          </span>
        </div>
      </div>

      {/* Filter Control Bar */}
      <div className="glass-card p-4 rounded-xl border border-slate-800 grid grid-cols-1 sm:grid-cols-3 gap-3">
        {/* Search */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search courses by name or ID..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-xl pl-9 pr-3 py-2 text-xs text-white outline-none focus:border-sky-500"
          />
        </div>

        {/* Category Filter */}
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-400 flex-shrink-0" />
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-sky-500"
          >
            <option value="ALL">All Categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        {/* Status Filter */}
        <div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-sky-500"
          >
            <option value="ALL">All Statuses</option>
            <option value="ELIGIBLE">Recommended / Fully Eligible</option>
            <option value="MISSING_PREREQ">Missing Prerequisites</option>
            <option value="CONFLICT">Schedule Conflict</option>
          </select>
        </div>
      </div>

      {/* Results Count Summary */}
      <div className="flex items-center justify-between text-xs text-slate-400">
        <span>Showing {filtered.length} of {recommendations.length} total electives</span>
      </div>

      {/* Course Cards Grid */}
      {loading ? (
        <div className="glass-panel p-16 rounded-2xl text-center text-slate-400 animate-pulse">
          Evaluating prerequisite chains, timetable conflicts, and career alignments...
        </div>
      ) : filtered.length === 0 ? (
        <div className="glass-panel p-12 rounded-2xl text-center text-slate-400 space-y-3">
          <Info className="w-8 h-8 text-sky-400 mx-auto" />
          <p className="font-semibold text-white">No matching electives found for selected filter.</p>
          <button
            onClick={() => { setSearchTerm(''); setCategoryFilter('ALL'); setStatusFilter('ALL'); }}
            className="text-xs text-sky-400 underline"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map((course) => (
            <CourseCard
              key={course.course_id}
              course={course}
              onOpenDetails={setSelectedCourseDetails}
              onOpenExplanation={setSelectedCourseExplanation}
            />
          ))}
        </div>
      )}

      {/* Details Modal */}
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
