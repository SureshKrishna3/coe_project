const CACHE_KEYS = {
  COURSES: 'vee_cache_courses',
  CAREERS: 'vee_cache_careers',
  STUDENTS: 'vee_cache_students',
  RECOMMENDATIONS: 'vee_cache_recommendations_',
  ACTIVE_STUDENT: 'vee_active_student'
};

export const offlineCache = {
  set(key, data) {
    try {
      localStorage.setItem(key, JSON.stringify(data));
    } catch (e) {
      console.warn('LocalStorage quota exceeded or unavailable:', e);
    }
  },

  get(key) {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (e) {
      return null;
    }
  },

  saveCourses(courses) {
    this.set(CACHE_KEYS.COURSES, courses);
  },

  getCourses() {
    return this.get(CACHE_KEYS.COURSES) || [];
  },

  saveCareers(careers) {
    this.set(CACHE_KEYS.CAREERS, careers);
  },

  getCareers() {
    return this.get(CACHE_KEYS.CAREERS) || [];
  },

  saveStudents(students) {
    this.set(CACHE_KEYS.STUDENTS, students);
  },

  getStudents() {
    return this.get(CACHE_KEYS.STUDENTS) || [];
  },

  saveRecommendations(studentId, recs) {
    this.set(CACHE_KEYS.RECOMMENDATIONS + studentId, recs);
  },

  getRecommendations(studentId) {
    return this.get(CACHE_KEYS.RECOMMENDATIONS + studentId) || [];
  },

  saveActiveStudent(student) {
    this.set(CACHE_KEYS.ACTIVE_STUDENT, student);
  },

  getActiveStudent() {
    return this.get(CACHE_KEYS.ACTIVE_STUDENT);
  }
};
