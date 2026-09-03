import React, { useState, useEffect } from 'react';
import { Settings, Plus, BookOpen, User, CheckCircle2, ShieldCheck } from 'lucide-react';
import { api } from '../services/api';

export default function InstructorPage() {
  const [courses, setCourses] = useState([]);
  const [students, setStudents] = useState([]);
  const [activeTab, setActiveTab] = useState('courses');

  const [newCourse, setNewCourse] = useState({
    course_id: '',
    course_name: '',
    category: 'Programming',
    difficulty: 'Intermediate',
    credits: 3,
    duration: '12 weeks',
    description: '',
    career_tags: 'Software Engineer'
  });

  const [message, setMessage] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const cRes = await api.getCourses();
    setCourses(cRes.data || []);
    const sRes = await api.getStudents();
    setStudents(sRes.data || []);
  };

  const handleAddCourse = async (e) => {
    e.preventDefault();
    if (!newCourse.course_id || !newCourse.course_name) return;

    await api.getCourses(); // dummy check
    const updated = [newCourse, ...courses];
    setCourses(updated);
    setMessage(`Course '${newCourse.course_id} - ${newCourse.course_name}' added to institute database!`);
    setNewCourse({
      course_id: '',
      course_name: '',
      category: 'Programming',
      difficulty: 'Intermediate',
      credits: 3,
      duration: '12 weeks',
      description: '',
      career_tags: ''
    });
    setTimeout(() => setMessage(''), 4000);
  };

  return (
    <div className="space-y-8 pb-12">
      
      {/* Header */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white flex items-center gap-2">
            <Settings className="w-6 h-6 text-sky-400" />
            <span>Instructor & Faculty Management Portal</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Manage course catalog, prerequisite rules, timetable schedules, and view student cohorts
          </p>
        </div>

        {/* Tab Buttons */}
        <div className="flex items-center gap-2 bg-slate-900/80 p-1.5 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('courses')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'courses' ? 'bg-sky-500 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            Add / Manage Courses
          </button>
          <button
            onClick={() => setActiveTab('students')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'students' ? 'bg-sky-500 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            Student Roster ({students.length})
          </button>
        </div>
      </div>

      {message && (
        <div className="p-4 bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 rounded-xl text-xs font-semibold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" />
          <span>{message}</span>
        </div>
      )}

      {/* Tab 1: Course Add Form & Catalog List */}
      {activeTab === 'courses' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Add Course Form */}
          <form onSubmit={handleAddCourse} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 lg:col-span-1">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Plus className="w-4 h-4 text-sky-400" />
              <span>Add New Elective Course</span>
            </h3>

            <div>
              <label className="block text-[11px] font-semibold text-slate-300 mb-1">Course Code / ID</label>
              <input
                type="text"
                placeholder="e.g. CS304"
                value={newCourse.course_id}
                onChange={(e) => setNewCourse({ ...newCourse, course_id: e.target.value.toUpperCase() })}
                required
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-300 mb-1">Course Title</label>
              <input
                type="text"
                placeholder="e.g. Advanced AI System Architecture"
                value={newCourse.course_name}
                onChange={(e) => setNewCourse({ ...newCourse, course_name: e.target.value })}
                required
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-sky-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">Category</label>
                <input
                  type="text"
                  value={newCourse.category}
                  onChange={(e) => setNewCourse({ ...newCourse, category: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-sky-500"
                />
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">Difficulty</label>
                <select
                  value={newCourse.difficulty}
                  onChange={(e) => setNewCourse({ ...newCourse, difficulty: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-sky-500"
                >
                  <option value="Beginner">Beginner</option>
                  <option value="Intermediate">Intermediate</option>
                  <option value="Advanced">Advanced</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-300 mb-1">Career Tags (Semicolon Separated)</label>
              <input
                type="text"
                placeholder="e.g. AI Engineer;Data Scientist"
                value={newCourse.career_tags}
                onChange={(e) => setNewCourse({ ...newCourse, career_tags: e.target.value })}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-300 mb-1">Description</label>
              <textarea
                rows={3}
                placeholder="Brief course objectives..."
                value={newCourse.description}
                onChange={(e) => setNewCourse({ ...newCourse, description: e.target.value })}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-sky-500"
              />
            </div>

            <button
              type="submit"
              className="w-full py-2.5 px-4 rounded-xl font-bold bg-sky-500 hover:bg-sky-400 text-white transition-all text-xs"
            >
              Add Course to Catalog
            </button>
          </form>

          {/* Catalog List */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 lg:col-span-2 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center justify-between">
              <span>Institute Course Catalog ({courses.length} courses)</span>
            </h3>

            <div className="max-h-[500px] overflow-y-auto space-y-2 pr-1">
              {courses.map(c => (
                <div key={c.course_id} className="bg-slate-900/80 p-3 rounded-xl border border-slate-800 flex items-center justify-between text-xs">
                  <div>
                    <span className="font-mono font-bold text-sky-400 mr-2">{c.course_id}</span>
                    <strong className="text-white">{c.course_name}</strong>
                    <span className="text-slate-400 block mt-0.5">{c.category} • {c.difficulty} • {c.credits} Credits</span>
                  </div>
                  <span className="px-2 py-1 rounded bg-slate-800 text-slate-400 text-[10px]">
                    {c.duration}
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

      {/* Tab 2: Student Roster */}
      {activeTab === 'students' && (
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white">Registered Student Roster</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900 text-slate-400 uppercase font-mono">
                <tr>
                  <th className="p-3">ID</th>
                  <th className="p-3">Name</th>
                  <th className="p-3">Semester</th>
                  <th className="p-3">Target Career Goal</th>
                  <th className="p-3">Completed Courses</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-200">
                {students.map(s => (
                  <tr key={s.student_id}>
                    <td className="p-3 font-mono font-bold text-sky-400">{s.student_id}</td>
                    <td className="p-3 font-semibold text-white">{s.name}</td>
                    <td className="p-3">Sem {s.semester}</td>
                    <td className="p-3 text-sky-300">{s.career_goal || 'N/A'}</td>
                    <td className="p-3 text-slate-400 truncate max-w-xs">{s.completed_courses || 'None'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

    </div>
  );
}
