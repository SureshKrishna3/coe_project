import React, { useState, useEffect } from 'react';
import { User, Check, Plus, Save, BookOpen, Target, Award, Sparkles } from 'lucide-react';
import { api } from '../services/api';

const CAREERS = [
  "AI Engineer", "Data Scientist", "Data Analyst", "Software Engineer",
  "Fullstack Developer", "Backend Developer", "Frontend Developer",
  "Cybersecurity Specialist", "Embedded Systems Engineer", "Robotics Engineer",
  "IoT Specialist", "Industrial Automation Engineer", "PLC Engineer",
  "Cloud Solutions Architect", "DevOps Engineer", "CAD Design Engineer",
  "Smart Manufacturing Specialist", "VLSI Engineer"
];

export default function StudentProfilePage({ activeStudent, setActiveStudent }) {
  const [students, setStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [formData, setFormData] = useState({
    student_id: '',
    name: '',
    semester: 1,
    completed_courses: [],
    skills: [],
    career_goal: 'AI Engineer',
    preferred_schedule: 'Monday 09:00-11:00'
  });

  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    if (activeStudent) {
      setFormData({
        student_id: activeStudent.student_id,
        name: activeStudent.name,
        semester: activeStudent.semester || 1,
        completed_courses: activeStudent.completed_courses ? activeStudent.completed_courses.split(';').filter(Boolean) : [],
        skills: activeStudent.skills ? activeStudent.skills.split(';').filter(Boolean) : [],
        career_goal: activeStudent.career_goal || 'AI Engineer',
        preferred_schedule: activeStudent.preferred_schedule || ''
      });
    }
  }, [activeStudent]);

  const loadInitialData = async () => {
    const sRes = await api.getStudents();
    setStudents(sRes.data || []);
    const cRes = await api.getCourses();
    setCourses(cRes.data || []);
  };

  const handleToggleCourse = (courseId) => {
    setFormData(prev => {
      const exists = prev.completed_courses.includes(courseId);
      const updated = exists
        ? prev.completed_courses.filter(c => c !== courseId)
        : [...prev.completed_courses, courseId];
      return { ...prev, completed_courses: updated };
    });
  };

  const handleSelectExisting = (sId) => {
    const match = students.find(s => s.student_id === sId);
    if (match) {
      setActiveStudent(match);
    }
  };

  const handleCreateNew = () => {
    const newId = `STU${Math.floor(100 + Math.random() * 900)}`;
    const newObj = {
      student_id: newId,
      name: 'New Student',
      semester: 1,
      completed_courses: [],
      skills: [],
      career_goal: 'Software Engineer',
      preferred_schedule: 'Monday 10:00-12:00'
    };
    setFormData(newObj);
    setActiveStudent(newObj);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');

    const payload = {
      ...formData,
      completed_courses: formData.completed_courses.join(';'),
      skills: formData.skills.join(';')
    };

    const res = await api.saveStudent(payload);
    setActiveStudent(res.data);
    setSaving(false);
    setMessage('Student profile successfully saved and cached!');
    setTimeout(() => setMessage(''), 4000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      
      {/* Page Title */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <User className="w-6 h-6 text-sky-400" />
            <span>Student Profile Setup</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">Field-friendly entry form for course history and career goals</p>
        </div>

        <button
          onClick={handleCreateNew}
          className="py-2.5 px-4 rounded-xl text-xs font-bold bg-sky-500 hover:bg-sky-400 text-white transition-all flex items-center gap-2 shadow-lg shadow-sky-500/20"
        >
          <Plus className="w-4 h-4" />
          <span>New Profile</span>
        </button>
      </div>

      {message && (
        <div className="p-4 bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 rounded-xl text-xs font-semibold flex items-center gap-2">
          <Check className="w-4 h-4" />
          <span>{message}</span>
        </div>
      )}

      {/* Main Profile Form */}
      <form onSubmit={handleSubmit} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-6">
        
        {/* Row 1: Select Existing or Edit ID & Name */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Select Existing Profile</label>
            <select
              value={formData.student_id}
              onChange={(e) => handleSelectExisting(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-xs text-white outline-none focus:border-sky-500"
            >
              {students.map(s => (
                <option key={s.student_id} value={s.student_id}>
                  {s.student_id} — {s.name} ({s.career_goal})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Student Full Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-xs text-white outline-none focus:border-sky-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Current Semester</label>
            <select
              value={formData.semester}
              onChange={(e) => setFormData({ ...formData, semester: parseInt(e.target.value) })}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-xs text-white outline-none focus:border-sky-500"
            >
              {[1, 2, 3, 4, 5, 6].map(sem => (
                <option key={sem} value={sem}>Semester {sem}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Row 2: Target Career Goal */}
        <div>
          <label className="block text-xs font-semibold text-slate-300 mb-2 flex items-center gap-1.5">
            <Target className="w-4 h-4 text-sky-400" />
            <span>Target Vocational Career Pathway Goal</span>
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
            {CAREERS.map(c => {
              const isSelected = formData.career_goal === c;
              return (
                <button
                  type="button"
                  key={c}
                  onClick={() => setFormData({ ...formData, career_goal: c })}
                  className={`p-2.5 rounded-xl text-xs font-semibold text-left transition-all border ${
                    isSelected
                      ? 'bg-sky-500/20 text-sky-300 border-sky-500'
                      : 'bg-slate-900/60 text-slate-400 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <span className="block truncate">{c}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Row 3: Completed Courses Multi-Select Chips */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
              <BookOpen className="w-4 h-4 text-amber-400" />
              <span>Completed Course History ({formData.completed_courses.length} selected)</span>
            </label>
            <span className="text-[10px] text-slate-400">Click chips to toggle completed status</span>
          </div>

          <div className="max-h-56 overflow-y-auto p-3 bg-slate-900/80 rounded-xl border border-slate-800 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
            {courses.map(c => {
              const isChecked = formData.completed_courses.includes(c.course_id);
              return (
                <button
                  type="button"
                  key={c.course_id}
                  onClick={() => handleToggleCourse(c.course_id)}
                  className={`p-2 rounded-lg text-xs flex items-center justify-between border transition-all ${
                    isChecked
                      ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-300 font-semibold'
                      : 'bg-slate-900 border-slate-800 text-slate-400 hover:bg-slate-800'
                  }`}
                >
                  <span className="truncate">{c.course_id} — {c.course_name}</span>
                  {isChecked && <Check className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />}
                </button>
              );
            })}
          </div>
        </div>

        {/* Submit Action Button */}
        <div className="pt-4 border-t border-slate-800 flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="py-3 px-8 rounded-xl font-bold bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white shadow-lg shadow-sky-500/25 transition-all flex items-center gap-2 text-xs"
          >
            <Save className="w-4 h-4" />
            <span>{saving ? 'Saving Profile...' : 'Save & Analyze Elective Recommendations'}</span>
          </button>
        </div>

      </form>
    </div>
  );
}
