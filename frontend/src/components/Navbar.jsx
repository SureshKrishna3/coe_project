import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Compass, User, BookOpen, GitBranch, BarChart2, ShieldCheck, Wifi, WifiOff, Settings } from 'lucide-react';
import { offlineCache } from '../services/offlineCache';

export default function Navbar({ activeStudent, isOffline }) {
  const location = useLocation();

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: BarChart2 },
    { path: '/profile', label: 'Student Profile', icon: User },
    { path: '/explorer', label: 'Elective Explorer', icon: BookOpen },
    { path: '/career-pathway', label: 'Career Pathway', icon: GitBranch },
    { path: '/evaluation', label: 'Evaluation', icon: Compass },
    { path: '/instructor', label: 'Instructor Portal', icon: Settings },
    { path: '/validation', label: 'Feedback', icon: ShieldCheck },
  ];

  return (
    <nav className="glass-panel sticky top-0 z-40 border-b border-slate-800 px-4 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-sky-500/20 group-hover:scale-105 transition-transform">
            <Compass className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-sky-400 bg-clip-text text-transparent">
              Vocational Elective Explorer
            </h1>
            <p className="text-xs text-slate-400">Explainable Prerequisite & Career Navigator</p>
          </div>
        </Link>

        {/* Navigation Links */}
        <div className="hidden lg:flex items-center gap-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-sky-500/15 text-sky-400 border border-sky-500/30'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </div>

        {/* Right Status Panel */}
        <div className="flex items-center gap-3">
          {/* Active Student Badge */}
          {activeStudent ? (
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800/80 border border-slate-700 text-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              <span className="text-slate-400">Student:</span>
              <span className="font-semibold text-sky-300 max-w-[120px] truncate">{activeStudent.name}</span>
            </div>
          ) : (
            <Link
              to="/profile"
              className="text-xs text-sky-400 hover:underline flex items-center gap-1 bg-sky-950/50 px-3 py-1.5 rounded-full border border-sky-800/50"
            >
              <User className="w-3.5 h-3.5" />
              <span>Select Profile</span>
            </Link>
          )}

          {/* Network / Offline Mode Indicator */}
          <div
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border ${
              isOffline
                ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
            }`}
            title={isOffline ? 'Using locally cached database' : 'Connected to live FastAPI backend'}
          >
            {isOffline ? <WifiOff className="w-3.5 h-3.5" /> : <Wifi className="w-3.5 h-3.5" />}
            <span className="hidden md:inline">{isOffline ? 'Offline Mode' : 'Online'}</span>
          </div>
        </div>
      </div>
    </nav>
  );
}
