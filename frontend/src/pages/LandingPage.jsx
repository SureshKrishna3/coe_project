import React from 'react';
import { Link } from 'react-router-dom';
import { Compass, CheckCircle2, ShieldAlert, GitBranch, Sparkles, ArrowRight, BookOpen, Layers, Cpu, Award } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="space-y-16 pb-16">
      
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-8 rounded-3xl glass-panel border border-slate-800 p-8 md:p-12 text-center max-w-5xl mx-auto mt-6">
        <div className="absolute -top-24 -left-24 w-72 h-72 bg-sky-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute -bottom-24 -right-24 w-72 h-72 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 text-xs font-semibold mb-6">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Explainable Prerequisite & Career Navigator</span>
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-sky-400 bg-clip-text text-transparent mb-6 max-w-3xl mx-auto leading-tight">
          Select Vocational Electives with Complete Career Clarity
        </h1>

        <p className="text-base md:text-lg text-slate-300 max-w-2xl mx-auto mb-8 leading-relaxed">
          Stop choosing courses blindly. Analyze prerequisites, detect schedule conflicts, evaluate learning outcomes, and align electives with your target career pathway.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            to="/profile"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-bold bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white shadow-lg shadow-sky-500/25 transition-all flex items-center justify-center gap-2 group"
          >
            <span>Get Started — Setup Profile</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>

          <Link
            to="/explorer"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all flex items-center justify-center gap-2"
          >
            <BookOpen className="w-4 h-4 text-sky-400" />
            <span>Explore Courses</span>
          </Link>
        </div>
      </section>

      {/* Problem & Solution Feature Cards */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-2xl md:text-3xl font-extrabold text-white">Why Vocational Students Need This Solution</h2>
          <p className="text-sm text-slate-400 mt-2">Solving real-world elective selection challenges in technical education.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="glass-card p-6 rounded-2xl border border-slate-800">
            <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400 mb-4">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white mb-2">Prerequisite Blindness</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Students often register for advanced courses without verifying mandatory prerequisite chains, leading to high drop-out rates.
            </p>
          </div>

          <div className="glass-card p-6 rounded-2xl border border-slate-800">
            <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 mb-4">
              <Layers className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white mb-2">Timetable Overlaps</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Selected electives frequently clash with compulsory lab or lecture slots, causing scheduling chaos during registration.
            </p>
          </div>

          <div className="glass-card p-6 rounded-2xl border border-slate-800">
            <div className="w-12 h-12 rounded-xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 mb-4">
              <GitBranch className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white mb-2">Career Misalignment</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Electives are chosen based on peer popularity rather than whether they build skills required for target career roles like AI Engineer or Robotics Specialist.
            </p>
          </div>
        </div>
      </section>

      {/* How it Works Workflow */}
      <section className="max-w-6xl mx-auto px-4 bg-slate-900/60 rounded-3xl p-8 border border-slate-800">
        <h2 className="text-2xl font-extrabold text-white text-center mb-8">System Architecture Workflow</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 bg-slate-900 rounded-xl border border-slate-800 text-center">
            <div className="w-8 h-8 rounded-full bg-sky-500/20 text-sky-400 font-extrabold flex items-center justify-center mx-auto mb-2 text-sm">1</div>
            <h4 className="font-bold text-sm text-white mb-1">Student Profile</h4>
            <p className="text-xs text-slate-400">Enter completed courses, skills, and target career goal.</p>
          </div>

          <div className="p-4 bg-slate-900 rounded-xl border border-slate-800 text-center">
            <div className="w-8 h-8 rounded-full bg-sky-500/20 text-sky-400 font-extrabold flex items-center justify-center mx-auto mb-2 text-sm">2</div>
            <h4 className="font-bold text-sm text-white mb-1">Engine Checks</h4>
            <p className="text-xs text-slate-400">Prerequisite AND/OR logic & schedule overlap detection.</p>
          </div>

          <div className="p-4 bg-slate-900 rounded-xl border border-slate-800 text-center">
            <div className="w-8 h-8 rounded-full bg-sky-500/20 text-sky-400 font-extrabold flex items-center justify-center mx-auto mb-2 text-sm">3</div>
            <h4 className="font-bold text-sm text-white mb-1">Pathway Ranking</h4>
            <p className="text-xs text-slate-400">Score electives (0–100) based on goal alignment and downstream value.</p>
          </div>

          <div className="p-4 bg-slate-900 rounded-xl border border-slate-800 text-center">
            <div className="w-8 h-8 rounded-full bg-sky-500/20 text-sky-400 font-extrabold flex items-center justify-center mx-auto mb-2 text-sm">4</div>
            <h4 className="font-bold text-sm text-white mb-1">Clear Explanation</h4>
            <p className="text-xs text-slate-400">Get plain-language rationales and alternative step pathways.</p>
          </div>
        </div>
      </section>

    </div>
  );
}
