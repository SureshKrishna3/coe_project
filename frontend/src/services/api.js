import axios from 'axios';
import { offlineCache } from './offlineCache';

const API_BASE_URL = '/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const api = {
  async getStudents() {
    try {
      const res = await client.get('/students');
      offlineCache.saveStudents(res.data);
      return { data: res.data, isOffline: false };
    } catch (err) {
      console.warn('Backend unavailable, returning cached students.');
      const cached = offlineCache.getStudents();
      return { data: cached, isOffline: true };
    }
  },

  async getStudent(studentId) {
    try {
      const res = await client.get(`/students/${studentId}`);
      return { data: res.data, isOffline: false };
    } catch (err) {
      const cachedList = offlineCache.getStudents();
      const match = cachedList.find(s => s.student_id === studentId);
      return { data: match || null, isOffline: true };
    }
  },

  async saveStudent(studentData) {
    try {
      const res = await client.post('/students', studentData);
      return { data: res.data, isOffline: false };
    } catch (err) {
      const cached = offlineCache.getStudents();
      const updated = [studentData, ...cached.filter(s => s.student_id !== studentData.student_id)];
      offlineCache.saveStudents(updated);
      offlineCache.saveActiveStudent(studentData);
      return { data: studentData, isOffline: true };
    }
  },

  async getCourses(filters = {}) {
    try {
      const res = await client.get('/courses', { params: filters });
      if (!filters.category && !filters.search) {
        offlineCache.saveCourses(res.data);
      }
      return { data: res.data, isOffline: false };
    } catch (err) {
      console.warn('Backend unavailable, returning cached courses.');
      let cached = offlineCache.getCourses();
      if (filters.search) {
        cached = cached.filter(c => c.course_name.toLowerCase().includes(filters.search.toLowerCase()));
      }
      return { data: cached, isOffline: true };
    }
  },

  async getCourseDetail(courseId) {
    try {
      const res = await client.get(`/courses/${courseId}`);
      return { data: res.data, isOffline: false };
    } catch (err) {
      const cached = offlineCache.getCourses();
      const match = cached.find(c => c.course_id === courseId);
      return { data: match || null, isOffline: true };
    }
  },

  async getCareers() {
    try {
      const res = await client.get('/careers');
      offlineCache.saveCareers(res.data);
      return { data: res.data, isOffline: false };
    } catch (err) {
      const cached = offlineCache.getCareers();
      return { data: cached, isOffline: true };
    }
  },

  async getCareerDetail(careerId) {
    try {
      const res = await client.get(`/careers/${careerId}`);
      return { data: res.data, isOffline: false };
    } catch (err) {
      const cached = offlineCache.getCareers();
      const match = cached.find(c => c.career_id === careerId || c.career_name === careerId);
      return { data: match || null, isOffline: true };
    }
  },

  async getRecommendations(studentId) {
    try {
      const res = await client.get(`/recommendations/${studentId}`);
      offlineCache.saveRecommendations(studentId, res.data);
      return { data: res.data, isOffline: false };
    } catch (err) {
      console.warn('Backend unavailable, using cached recommendations.');
      const cached = offlineCache.getRecommendations(studentId);
      return { data: cached, isOffline: true };
    }
  },

  async runEvaluation(numSamples = 150) {
    try {
      const res = await client.post(`/evaluation/run?num_samples=${numSamples}`);
      if (res.data) {
        offlineCache.set('vee_last_evaluation_results', res.data);
      }
      return { data: res.data, isOffline: false };
    } catch (err) {
      console.warn('Backend unavailable for evaluation run.');
      const cached = offlineCache.get('vee_last_evaluation_results');
      return { data: cached || null, isOffline: true };
    }
  },

  async getEvaluationResults() {
    try {
      const res = await client.get('/evaluation/results');
      if (res.data) {
        offlineCache.set('vee_last_evaluation_results', res.data);
      }
      return { data: res.data, isOffline: false };
    } catch (err) {
      const cached = offlineCache.get('vee_last_evaluation_results');
      return { data: cached || null, isOffline: true };
    }
  },

  async submitStakeholderFeedback(feedbackData) {
    try {
      const res = await client.post('/stakeholder/feedback', feedbackData);
      return { data: res.data, isOffline: false };
    } catch (err) {
      return { data: { status: "saved_locally", message: "Recorded locally in offline mode." }, isOffline: true };
    }
  },

  async getStakeholderStats() {
    try {
      const res = await client.get('/stakeholder/stats');
      return { data: res.data, isOffline: false };
    } catch (err) {
      return { data: null, isOffline: true };
    }
  }
};
