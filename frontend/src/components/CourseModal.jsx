import React from 'react';
import { X, CheckCircle2, XCircle, Clock, Calendar, MapPin, Award, BookOpen, Target, ArrowRight } from 'lucide-react';

export default function CourseModal({ course, onClose, onOpenExplanation }) {
  if (!course) return null;

  const {
    course_id,
    course_name,
    category,
    difficulty,
    credits,
    duration,
    description,
    prerequisites = [],
    outcomes = [],
    schedules = [],
    prerequisite_status = {},
    schedule_status = {},
    career_alignment = {},
    alternative_pathway = []
  } = course;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
      <div className="glass-panel w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl border border-slate-700 shadow-2xl p-6 relative text-slate-100">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-2 rounded-full bg-slate-800/60 hover:bg-slate-700 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-sky-500/20 text-sky-400 border border-sky-500/30">
              {course_id}
            </span>
            <span className="text-xs text-slate-400">• {category}</span>
          </div>
          <h2 className="text-2xl font-extrabold text-white">{course_name}</h2>
        </div>

        {/* Quick Attributes */}
        <div className="grid grid-cols-3 gap-3 mb-6 bg-slate-900/80 p-3 rounded-xl border border-slate-800 text-xs">
          <div className="flex items-center gap-2">
            <Award className="w-4 h-4 text-sky-400" />
            <div>
              <p className="text-slate-400">Difficulty</p>
              <p className="font-semibold text-white">{difficulty}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-indigo-400" />
            <div>
              <p className="text-slate-400">Duration</p>
              <p className="font-semibold text-white">{duration}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-amber-400" />
            <div>
              <p className="text-slate-400">Credits</p>
              <p className="font-semibold text-white">{credits} Credits</p>
            </div>
          </div>
        </div>

        {/* Course Description */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-2">Description</h3>
          <p className="text-sm text-slate-300 leading-relaxed bg-slate-900/40 p-3 rounded-lg border border-slate-800">
            {description || 'No detailed description available.'}
          </p>
        </div>

        {/* Prerequisites Checklist */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-2">
            <Target className="w-4 h-4 text-sky-400" />
            <span>Prerequisite Requirements</span>
          </h3>

          {prerequisite_status.is_satisfied ? (
            <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400 text-xs flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              <span>All prerequisites satisfied! You are eligible to enroll in this course.</span>
            </div>
          ) : (
            <div className="space-y-2">
              <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-lg text-rose-400 text-xs flex items-center gap-2">
                <XCircle className="w-4 h-4 flex-shrink-0" />
                <span>Missing prerequisite(s): {prerequisite_status.missing_direct?.join(', ') || 'Required background courses missing'}</span>
              </div>
              
              {alternative_pathway && alternative_pathway.length > 0 && (
                <div className="p-3 bg-amber-500/10 border border-amber-500/30 rounded-lg text-amber-300 text-xs">
                  <p className="font-semibold mb-1">Recommended Pathway Forward:</p>
                  <div className="flex items-center gap-2 flex-wrap">
                    {alternative_pathway.map((step, idx) => (
                      <React.Fragment key={step}>
                        <span className="px-2 py-0.5 rounded bg-slate-800 text-amber-200 border border-slate-700 font-mono">
                          {step}
                        </span>
                        {idx < alternative_pathway.length - 1 && <ArrowRight className="w-3 h-3 text-amber-400" />}
                      </React.Fragment>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Learning Outcomes */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-2">Learning Outcomes</h3>
          {outcomes.length > 0 ? (
            <ul className="space-y-2 text-xs text-slate-300">
              {outcomes.map((o, idx) => (
                <li key={idx} className="flex items-start gap-2 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                  <span>{o.outcome_description}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-slate-400 italic">Course outcomes pending documentation.</p>
          )}
        </div>

        {/* Schedule Slots */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-2">Timetable Schedule</h3>
          {schedules.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {schedules.map((s, idx) => (
                <div key={idx} className="flex items-center gap-2 text-xs bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                  <Calendar className="w-4 h-4 text-indigo-400 flex-shrink-0" />
                  <div>
                    <p className="font-semibold text-white">{s.day} ({s.start_time} - {s.end_time})</p>
                    <p className="text-slate-400 flex items-center gap-1 mt-0.5">
                      <MapPin className="w-3 h-3 text-slate-500" />
                      <span>{s.location}</span>
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-slate-400 italic">Schedule TBD for upcoming semester.</p>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-800">
          <button
            onClick={() => {
              onClose();
              if (onOpenExplanation) onOpenExplanation(course);
            }}
            className="py-2.5 px-4 rounded-xl text-xs font-semibold bg-sky-500/20 text-sky-300 border border-sky-500/40 hover:bg-sky-500/30 transition-colors"
          >
            Why this course recommendation?
          </button>

          <button
            onClick={onClose}
            className="py-2.5 px-5 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-white transition-colors"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
}
