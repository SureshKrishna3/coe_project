import React, { useState, useEffect } from 'react';
import { ShieldCheck, MessageSquare, CheckCircle2, Send, Info } from 'lucide-react';
import { api } from '../services/api';

export default function StakeholderValidationPage() {
  const [stats, setStats] = useState(null);
  const [isOffline, setIsOffline] = useState(false);
  const [form, setForm] = useState({
    role: 'Student',
    understandable_recommendations: true,
    useful_prerequisites: true,
    useful_pathway: true,
    easy_to_use: true,
    would_use_system: true,
    comments: ''
  });

  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    const res = await api.getStakeholderStats();
    setStats(res.data || null);
    setIsOffline(res.isOffline);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.submitStakeholderFeedback(form);
    setSubmitted(true);
    fetchStats();
  };

  const hasResponses = stats && stats.total_responses > 0;

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      
      {/* Header */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-sky-400" />
            <span>Stakeholder Validation & User Feedback</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Evaluating system usability, prerequisite clarity, and career pathway satisfaction
          </p>
        </div>

        {hasResponses && (
          <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-semibold">
            {stats.total_responses} Recorded Responses
          </span>
        )}
      </div>

      {/* Live Validation Dashboard Statistics */}
      {hasResponses ? (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="glass-card p-4 rounded-xl border border-slate-800 text-center">
            <span className="text-xs text-slate-400 block">Understandable Recs</span>
            <span className="text-2xl font-extrabold text-emerald-400">{stats.understandable_pct}%</span>
          </div>

          <div className="glass-card p-4 rounded-xl border border-slate-800 text-center">
            <span className="text-xs text-slate-400 block">Useful Prerequisites</span>
            <span className="text-2xl font-extrabold text-sky-400">{stats.useful_prereqs_pct}%</span>
          </div>

          <div className="glass-card p-4 rounded-xl border border-slate-800 text-center">
            <span className="text-xs text-slate-400 block">Useful Pathway Graph</span>
            <span className="text-2xl font-extrabold text-indigo-400">{stats.useful_pathway_pct}%</span>
          </div>

          <div className="glass-card p-4 rounded-xl border border-slate-800 text-center">
            <span className="text-xs text-slate-400 block">Would Use System</span>
            <span className="text-2xl font-extrabold text-purple-400">{stats.would_use_pct}%</span>
          </div>
        </div>
      ) : (
        <div className="glass-panel p-8 rounded-2xl border border-slate-800 text-center space-y-2">
          <Info className="w-8 h-8 text-sky-400 mx-auto" />
          <h3 className="text-base font-bold text-white">No stakeholder responses recorded yet.</h3>
          <p className="text-xs text-slate-400">
            Submit the evaluation survey below to record authentic feedback from students, faculty, or academic advisors.
          </p>
        </div>
      )}

      {/* Recent Comments */}
      {hasResponses && stats.recent_comments && stats.recent_comments.length > 0 && (
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-3">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <MessageSquare className="w-4 h-4 text-sky-400" />
            <span>Recent Stakeholder Comments</span>
          </h3>
          <div className="space-y-2">
            {stats.recent_comments.map((c, idx) => (
              <div key={idx} className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 text-xs text-slate-300">
                "{c}"
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Feedback Submission Form */}
      {submitted ? (
        <div className="glass-panel p-8 rounded-2xl border border-emerald-500/40 text-center space-y-3">
          <CheckCircle2 className="w-12 h-12 text-emerald-400 mx-auto" />
          <h2 className="text-xl font-bold text-white">Thank You for Your Validation Feedback!</h2>
          <p className="text-xs text-slate-300">Your response has been saved to the database stakeholder evaluation table.</p>
          <button
            onClick={() => setSubmitted(false)}
            className="text-xs font-semibold text-sky-400 underline pt-2"
          >
            Submit another evaluation
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-6">
          <h2 className="text-lg font-bold text-white">Stakeholder Evaluation Survey</h2>

          {/* Role Selection */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-2">I am participating as a:</label>
            <div className="grid grid-cols-3 gap-3">
              {['Student', 'Instructor / Faculty', 'Academic Advisor'].map(r => (
                <button
                  type="button"
                  key={r}
                  onClick={() => setForm({ ...form, role: r })}
                  className={`py-2 px-3 rounded-xl text-xs font-semibold border transition-all ${
                    form.role === r
                      ? 'bg-sky-500/20 text-sky-300 border-sky-500'
                      : 'bg-slate-900 text-slate-400 border-slate-800'
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>
          </div>

          {/* 5 Validation Questions */}
          <div className="space-y-4 text-xs text-slate-200">
            <div className="flex items-center justify-between p-3 bg-slate-900/60 rounded-xl border border-slate-800">
              <span>1. Are the recommendation explanations easy to understand?</span>
              <button
                type="button"
                onClick={() => setForm({ ...form, understandable_recommendations: !form.understandable_recommendations })}
                className={`px-3 py-1 rounded-lg font-bold ${form.understandable_recommendations ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' : 'bg-rose-500/20 text-rose-400'}`}
              >
                {form.understandable_recommendations ? 'YES' : 'NO'}
              </button>
            </div>

            <div className="flex items-center justify-between p-3 bg-slate-900/60 rounded-xl border border-slate-800">
              <span>2. Are prerequisite checks and missing warnings useful?</span>
              <button
                type="button"
                onClick={() => setForm({ ...form, useful_prerequisites: !form.useful_prerequisites })}
                className={`px-3 py-1 rounded-lg font-bold ${form.useful_prerequisites ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' : 'bg-rose-500/20 text-rose-400'}`}
              >
                {form.useful_prerequisites ? 'YES' : 'NO'}
              </button>
            </div>

            <div className="flex items-center justify-between p-3 bg-slate-900/60 rounded-xl border border-slate-800">
              <span>3. Is the career pathway visualization helpful for elective choices?</span>
              <button
                type="button"
                onClick={() => setForm({ ...form, useful_pathway: !form.useful_pathway })}
                className={`px-3 py-1 rounded-lg font-bold ${form.useful_pathway ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' : 'bg-rose-500/20 text-rose-400'}`}
              >
                {form.useful_pathway ? 'YES' : 'NO'}
              </button>
            </div>

            <div className="flex items-center justify-between p-3 bg-slate-900/60 rounded-xl border border-slate-800">
              <span>4. Is the application user interface easy to navigate?</span>
              <button
                type="button"
                onClick={() => setForm({ ...form, easy_to_use: !form.easy_to_use })}
                className={`px-3 py-1 rounded-lg font-bold ${form.easy_to_use ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' : 'bg-rose-500/20 text-rose-400'}`}
              >
                {form.easy_to_use ? 'YES' : 'NO'}
              </button>
            </div>

            <div className="flex items-center justify-between p-3 bg-slate-900/60 rounded-xl border border-slate-800">
              <span>5. Would you recommend this system for institute elective selection?</span>
              <button
                type="button"
                onClick={() => setForm({ ...form, would_use_system: !form.would_use_system })}
                className={`px-3 py-1 rounded-lg font-bold ${form.would_use_system ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' : 'bg-rose-500/20 text-rose-400'}`}
              >
                {form.would_use_system ? 'YES' : 'NO'}
              </button>
            </div>
          </div>

          {/* Comments */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Additional Feedback & Comments</label>
            <textarea
              rows={3}
              placeholder="Share your thoughts on explanations, pathway nodes, or missing features..."
              value={form.comments}
              onChange={(e) => setForm({ ...form, comments: e.target.value })}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-sky-500"
            />
          </div>

          <button
            type="submit"
            className="w-full py-3 px-6 rounded-xl font-bold bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white shadow-lg shadow-sky-500/20 transition-all flex items-center justify-center gap-2 text-xs"
          >
            <Send className="w-4 h-4" />
            <span>Submit Stakeholder Validation</span>
          </button>
        </form>
      )}

    </div>
  );
}
