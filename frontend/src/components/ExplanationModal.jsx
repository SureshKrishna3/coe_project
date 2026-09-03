import React from 'react';
import { X, CheckCircle2, AlertTriangle, XCircle, Lightbulb, Compass, Sparkles } from 'lucide-react';

export default function ExplanationModal({ course, onClose }) {
  if (!course) return null;

  const {
    course_name,
    score = 0,
    category_rating = '',
    explanation = {},
    alternative_pathway = []
  } = course;

  const {
    overall_summary = '',
    reasons_pro = [],
    reasons_con = [],
    suggested_action = ''
  } = explanation;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md animate-fadeIn">
      <div className="glass-panel w-full max-w-xl rounded-2xl border border-sky-500/30 shadow-2xl shadow-sky-500/10 p-6 relative text-slate-100">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-2 rounded-full bg-slate-800/60 hover:bg-slate-700 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-sky-500/20 border border-sky-500/40 flex items-center justify-center text-sky-400">
            <Compass className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h3 className="text-xs font-mono text-sky-400 uppercase tracking-widest">Explainable Recommendation</h3>
            <h2 className="text-xl font-bold text-white">{course_name}</h2>
          </div>
        </div>

        {/* Match Summary Box */}
        <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl mb-5 flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-400">Overall Rating</p>
            <p className="text-base font-extrabold text-sky-300">{category_rating || 'Evaluated'}</p>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-sky-500/20 border border-sky-500/40 text-sky-300 font-extrabold text-lg">
            <Sparkles className="w-4 h-4 text-amber-300" />
            <span>{score} / 100</span>
          </div>
        </div>

        {/* Why this course is recommended / positive reasons */}
        {reasons_pro.length > 0 && (
          <div className="mb-4">
            <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Positive Factors</span>
            </h4>
            <div className="space-y-2">
              {reasons_pro.map((r, idx) => (
                <div key={idx} className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-xs text-emerald-300 flex items-start gap-2">
                  <span className="font-bold text-emerald-400">✓</span>
                  <span>{r}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Concerns / Red flags */}
        {reasons_con.length > 0 && (
          <div className="mb-4">
            <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <XCircle className="w-4 h-4 text-rose-400" />
              <span>Prerequisite & Schedule Warnings</span>
            </h4>
            <div className="space-y-2">
              {reasons_con.map((r, idx) => (
                <div key={idx} className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-lg text-xs text-rose-300 flex items-start gap-2">
                  <span className="font-bold text-rose-400">✗</span>
                  <span>{r}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Suggested Next Action */}
        {suggested_action && (
          <div className="mb-5 p-3.5 bg-indigo-500/10 border border-indigo-500/30 rounded-xl text-xs text-indigo-200">
            <div className="flex items-center gap-1.5 font-bold text-indigo-300 mb-1">
              <Lightbulb className="w-4 h-4 text-amber-300" />
              <span>Suggested Next Step:</span>
            </div>
            <p className="leading-relaxed">{suggested_action}</p>
          </div>
        )}

        {/* Footer */}
        <div className="pt-3 border-t border-slate-800 flex justify-end">
          <button
            onClick={onClose}
            className="py-2 px-5 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-white transition-colors"
          >
            Got it, thanks!
          </button>
        </div>

      </div>
    </div>
  );
}
