const CACHE_KEYS = {
  COURSES: 'vee_cache_courses',
  CAREERS: 'vee_cache_careers',
  STUDENTS: 'vee_cache_students',
  RECOMMENDATIONS: 'vee_cache_recommendations_',
  ACTIVE_STUDENT: 'vee_active_student'
};

const DEFAULT_FALLBACK_COURSES = [
  { course_id: 'CS101', course_name: 'Python Programming Fundamentals', category: 'Computer Science', difficulty: 'Beginner', career_tags: 'AI, Data Science, Software', description: 'Core programming logic, syntax, functions, and data structures in Python.' },
  { course_id: 'CS102', course_name: 'Data Structures & Algorithms', category: 'Computer Science', difficulty: 'Intermediate', career_tags: 'AI, Software Engineering', description: 'Arrays, linked lists, trees, graphs, sorting, and algorithmic complexity.' },
  { course_id: 'DS201', course_name: 'Machine Learning Foundations', category: 'Artificial Intelligence', difficulty: 'Intermediate', career_tags: 'AI, Data Science', description: 'Supervised and unsupervised learning, regression, classification, and scikit-learn.' },
  { course_id: 'DS301', course_name: 'Deep Learning & Neural Networks', category: 'Artificial Intelligence', difficulty: 'Advanced', career_tags: 'AI, Computer Vision', description: 'Convolutional networks, transformers, PyTorch, and deep model optimization.' },
  { course_id: 'ELEC101', course_name: 'Circuit Analysis & Electronics', category: 'Electronics', difficulty: 'Beginner', career_tags: 'Robotics, Embedded Systems', description: 'Ohm’s law, Kirchhoff’s laws, operational amplifiers, and analog circuits.' },
  { course_id: 'ROB101', course_name: 'Robotics Engineering & Control', category: 'Robotics', difficulty: 'Intermediate', career_tags: 'Robotics, Automation', description: 'Kinematics, sensors, microcontrollers, motor control, and ROS.' }
];

const DEFAULT_FALLBACK_CAREERS = [
  { career_id: 'C1', career_name: 'AI & Machine Learning Engineer', description: 'Designs, trains, and deploys intelligent machine learning models and neural networks.', required_skills: 'Python, Machine Learning, Data Structures, PyTorch' },
  { career_id: 'C2', career_name: 'Robotics Systems Engineer', description: 'Integrates mechanical, electronic, and software systems for industrial automation and autonomous robotics.', required_skills: 'Robotics, Electronics, Microcontrollers, Control Theory' },
  { career_id: 'C3', career_name: 'Software Systems Engineer', description: 'Builds scalable backend applications, systems infrastructure, and databases.', required_skills: 'Python, Data Structures, Algorithms, Software Engineering' }
];

const DEFAULT_FALLBACK_STUDENTS = [
  { student_id: 'STU-1001', name: 'Alex Chen', semester: 3, completed_courses: 'CS101', skills: 'Python, Basic Math', career_goal: 'AI & Machine Learning Engineer', preferred_schedule: 'Morning', availability: 'Mon,Wed,Fri' }
];

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
    const cached = this.get(CACHE_KEYS.COURSES);
    return (cached && cached.length > 0) ? cached : DEFAULT_FALLBACK_COURSES;
  },

  saveCareers(careers) {
    this.set(CACHE_KEYS.CAREERS, careers);
  },

  getCareers() {
    const cached = this.get(CACHE_KEYS.CAREERS);
    return (cached && cached.length > 0) ? cached : DEFAULT_FALLBACK_CAREERS;
  },

  saveStudents(students) {
    this.set(CACHE_KEYS.STUDENTS, students);
  },

  getStudents() {
    const cached = this.get(CACHE_KEYS.STUDENTS);
    return (cached && cached.length > 0) ? cached : DEFAULT_FALLBACK_STUDENTS;
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
    const cached = this.get(CACHE_KEYS.ACTIVE_STUDENT);
    return cached || DEFAULT_FALLBACK_STUDENTS[0];
  }
};
