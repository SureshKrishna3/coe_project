import React, { useState, useEffect } from 'react';
import { GitBranch, CheckCircle2, ArrowRight, BookOpen, Target, Sparkles, Award, HelpCircle } from 'lucide-react';
import { api } from '../services/api';

export default function CareerPathwayPage({ activeStudent }) {
  const [careers, setCareers] = useState([]);
  const [selectedCareer, setSelectedCareer] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [nodeDetail, setNodeDetail] = useState(null);
  const [coursesMap, setCoursesMap] = useState({});

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (activeStudent && careers.length > 0) {
      const match = careers.find(c => c.career_name.toLowerCase() === (activeStudent.career_goal || '').toLowerCase());
      if (match) {
        setSelectedCareer(match);
      } else {
        setSelectedCareer(careers[0]);
      }
    }
  }, [activeStudent, careers]);

  const loadData = async () => {
    const cRes = await api.getCareers();
    setCareers(cRes.data || []);
    const crRes = await api.getCourses();
    const map = {};
    (crRes.data || []).forEach(c => { map[c.course_id] = c; });
    setCoursesMap(map);
  };

  const handleSelectNode = (stepName) => {
    setSelectedNode(stepName);
    const courseObj = coursesMap[stepName];
    if (courseObj) {
      setNodeDetail({
        id: courseObj.course_id,
        name: courseObj.course_name,
        category: courseObj.category,
        description: courseObj.description,
        difficulty: courseObj.difficulty,
        credits: courseObj.credits,
        isCourse: true
      });
    } else {
      setNodeDetail({
        id: 'GOAL',
        name: stepName,
        category: 'Career Outcome',
        description: `Target professional role: ${stepName}`,
        isCourse: false
      });
    }
  };

  const completedList = activeStudent?.completed_courses ? activeStudent.completed_courses.split(';') : [];

  // Parse sequence graph string e.g. "CS101 -> CS201 -> DS201 -> DS301 -> AI Engineer"
  const sequenceSteps = selectedCareer?.pathway_sequence
    ? selectedCareer.pathway_sequence.split('->').map(s => s.strip ? s.strip() : s.trim())
    : [];

  return (
    <div className="space-y-8 pb-12">
      
      {/* Header */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white flex items-center gap-2">
            <GitBranch className="w-6 h-6 text-sky-400" />
            <span>Interactive Career Pathway Explorer</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Visualizing course dependencies, skill progression, and future career consequences
          </p>
        </div>

        {/* Career Selector */}
        <div className="flex items-center gap-2 bg-slate-900/80 p-2.5 rounded-xl border border-slate-800">
          <Target className="w-4 h-4 text-sky-400" />
          <select
            value={selectedCareer?.career_id || ''}
            onChange={(e) => {
              const match = careers.find(c => c.career_id === e.target.value);
              setSelectedCareer(match);
              setSelectedNode(null);
              setNodeDetail(null);
            }}
            className="bg-transparent text-xs font-bold text-white outline-none cursor-pointer"
          >
            {careers.map(c => (
              <option key={c.career_id} value={c.career_id} className="bg-slate-900 text-white">
                {c.career_name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Selected Career Description */}
      {selectedCareer && (
        <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white">{selectedCareer.career_name} Pathway</h2>
            <span className="text-xs px-3 py-1 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/30">
              {selectedCareer.skills ? selectedCareer.skills.split(';').length : 0} Core Skills
            </span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">{selectedCareer.description}</p>
        </div>
      )}

      {/* Visual Sequence Chain Graph */}
      <div className="glass-panel p-8 rounded-2xl border border-slate-800">
        <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-6 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-sky-400" />
          <span>Pathway Sequence Nodes (Click Node for Details)</span>
        </h3>

        <div className="flex items-center justify-start overflow-x-auto py-6 px-2 gap-3 min-h-[140px]">
          {sequenceSteps.map((step, idx) => {
            const isCompleted = completedList.includes(step);
            const isGoal = idx === sequenceSteps.length - 1;
            const isSelected = selectedNode === step;
            const courseObj = coursesMap[step];

            let nodeColor = "bg-slate-900 border-slate-700 text-slate-300";
            if (isGoal) {
              nodeColor = "bg-gradient-to-r from-indigo-950 to-purple-950 border-purple-500/50 text-purple-300";
            } else if (isCompleted) {
              nodeColor = "bg-emerald-950/60 border-emerald-500/50 text-emerald-300";
            } else {
              nodeColor = "bg-sky-950/40 border-sky-500/40 text-sky-200";
            }

            if (isSelected) {
              nodeColor += " ring-2 ring-sky-400 shadow-lg shadow-sky-500/20";
            }

            return (
              <React.Fragment key={step}>
                <button
                  onClick={() => handleSelectNode(step)}
                  className={`flex-shrink-0 p-4 rounded-xl border text-center transition-all min-w-[140px] hover:scale-105 ${nodeColor}`}
                >
                  <div className="flex items-center justify-center gap-1 mb-1">
                    {isCompleted ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ) : isGoal ? (
                      <Target className="w-4 h-4 text-purple-400" />
                    ) : (
                      <BookOpen className="w-4 h-4 text-sky-400" />
                    )}
                    <span className="text-[10px] font-mono font-bold uppercase">{isGoal ? 'Goal' : step}</span>
                  </div>
                  <p className="text-xs font-bold truncate max-w-[130px]">
                    {courseObj ? courseObj.course_name : step}
                  </p>
                  <span className="text-[9px] block text-slate-400 mt-1">
                    {isCompleted ? 'Completed' : (isGoal ? 'Career Target' : 'Elective Node')}
                  </span>
                </button>

                {idx < sequenceSteps.length - 1 && (
                  <ArrowRight className="w-5 h-5 text-slate-600 flex-shrink-0" />
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>

      {/* Selected Node Details Card */}
      {nodeDetail && (
        <div className="glass-card p-6 rounded-2xl border border-sky-500/30 animate-fadeIn">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono text-sky-400 uppercase tracking-widest">{nodeDetail.category}</span>
            <span className="text-xs font-bold px-2.5 py-1 rounded bg-slate-800 text-slate-300">
              {nodeDetail.id}
            </span>
          </div>

          <h3 className="text-xl font-bold text-white mb-2">{nodeDetail.name}</h3>
          <p className="text-xs text-slate-300 leading-relaxed mb-4">{nodeDetail.description}</p>

          {nodeDetail.isCourse && (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs bg-slate-900/80 p-3 rounded-xl border border-slate-800">
              <div>
                <span className="text-slate-400 block">Difficulty</span>
                <span className="font-semibold text-white">{nodeDetail.difficulty}</span>
              </div>
              <div>
                <span className="text-slate-400 block">Credits</span>
                <span className="font-semibold text-white">{nodeDetail.credits}</span>
              </div>
              <div>
                <span className="text-slate-400 block">Status</span>
                <span className={`font-semibold ${completedList.includes(nodeDetail.id) ? 'text-emerald-400' : 'text-sky-400'}`}>
                  {completedList.includes(nodeDetail.id) ? 'Completed' : 'Available Elective'}
                </span>
              </div>
            </div>
          )}
        </div>
      )}

    </div>
  );
}
