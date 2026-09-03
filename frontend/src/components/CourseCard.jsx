import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, Info, Sparkles, Clock, Award, BookOpen } from 'lucide-react';

export default function CourseCard({ course, onOpenDetails, onOpenExplanation }) {
  const {
    course_id,
    course_name,
    category,
    difficulty,
    credits,
    duration,
    score = 0,
    category_rating = 'Available',
    eligibility_status = 'ELIGIBLE',
    prerequisite_status = {},
    schedule_status = {},
    career_alignment = {}
  } = course;

  // Status visual badge styling
  const getStatusBadge = () => {
    if (eligibility_status === 'ELIGIBLE') {
      return (
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>Recommended / Eligible</span>
        </div>
      );
    } else if (eligibility_status === 'SCHEDULE_CONFLICT') {
      return (
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/15 text-amber-400 border border-amber-500/30">
          <AlertTriangle className="w-3.5 h-3.5" />
          <span>Schedule Conflict</span>
        </div>
      );
    } else if (eligibility_status === 'MISSING_PREREQUISITES') {
      return (
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-500/15 text-rose-400 border border-rose-500/30">
          <XCircle className="w-3.5 h-3.5" />
          <span>Missing Prerequisites</span>
        </div>
      );
    } else if (eligibility_status === 'ALREADY_COMPLETED') {
      return (
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-sky-500/15 text-sky-400 border border-sky-500/30">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>Completed</span>
        </div>
      );
    }
    return null;
  };

  const isHighMatch = score >= 75;

  return (
    <div className="glass-card rounded-xl p-5 flex flex-col justify-between hover:shadow-xl hover:shadow-sky-500/5 transition-all group relative border border-slate-800">
      
      {/* Top Header */}
      <div>
        <div className="flex items-start justify-between gap-2 mb-3">
          <div>
            <span className="text-xs font-mono text-slate-400 tracking-wider uppercase block mb-1">
              {course_id} • {category}
            </span>
            <h3 className="text-lg font-bold text-white group-hover:text-sky-300 transition-colors">
              {course_name}
            </h3>
          </div>

          {/* Score Badge */}
          <div className="flex flex-col items-end">
            <div className={`px-2.5 py-1 rounded-lg text-sm font-extrabold flex items-center gap-1 ${
              score >= 80 ? 'bg-sky-500 text-white' : (score >= 60 ? 'bg-slate-700 text-sky-300' : 'bg-slate-800 text-slate-400')
            }`}>
              <Sparkles className="w-3.5 h-3.5 text-amber-300" />
              <span>{score}</span>
            </div>
            <span className="text-[10px] text-slate-400 mt-0.5">Match Score</span>
          </div>
        </div>

        {/* Status Indicator */}
        <div className="mb-4">
          {getStatusBadge()}
        </div>

        {/* Course Metadata */}
        <div className="grid grid-cols-3 gap-2 text-xs text-slate-300 mb-4 bg-slate-900/60 rounded-lg p-2.5 border border-slate-800/80">
          <div className="flex items-center gap-1.5">
            <Award className="w-3.5 h-3.5 text-sky-400" />
            <span>{difficulty}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-indigo-400" />
            <span>{duration}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <BookOpen className="w-3.5 h-3.5 text-amber-400" />
            <span>{credits} Credits</span>
          </div>
        </div>

        {/* Career Alignment Summary */}
        {career_alignment?.summary && (
          <p className="text-xs text-slate-300 line-clamp-2 mb-4 bg-sky-950/20 p-2 rounded border border-sky-900/30">
            <strong className="text-sky-400">Career Impact:</strong> {career_alignment.summary}
          </p>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex items-center gap-2 pt-3 border-t border-slate-800/80">
        <button
          onClick={() => onOpenExplanation(course)}
          className="flex-1 py-2 px-3 rounded-lg text-xs font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/30 hover:bg-sky-500/20 hover:text-white transition-colors flex items-center justify-center gap-1.5"
        >
          <Info className="w-3.5 h-3.5" />
          <span>Why this course?</span>
        </button>

        <button
          onClick={() => onOpenDetails(course)}
          className="py-2 px-3 rounded-lg text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white transition-colors"
        >
          Details
        </button>
      </div>

    </div>
  );
}
