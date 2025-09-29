import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Token management
export const getToken = () => {
  return localStorage.getItem('admin_token');
};

export const setToken = (token) => {
  if (token) {
    localStorage.setItem('admin_token', token);
  }
};

export const removeToken = () => {
  localStorage.removeItem('admin_token');
};

// Create axios instance with interceptors
const apiClient = axios.create({
  baseURL: API,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token && token.trim() !== '') {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for better error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data);

    if (error.response?.status === 401 || error.response?.status === 403) {
      console.log('Authentication failed, redirecting to login...');
      removeToken();
      if (window.location.pathname.includes('/admin')) {
        window.location.href = '/admin/login';
      }
    }
    return Promise.reject(error);
  }
);

// Admin API functions
export const adminApi = {
  // Dashboard
  getDashboardStats: async () => {
    const response = await apiClient.get('/admin/dashboard/stats');
    return response.data;
  },

  // Jobs
  getJobs: async (params = {}) => {
    const response = await apiClient.get('/admin/jobs', { params });
    return response.data;
  },

  createJob: async (jobData) => {
    const response = await apiClient.post('/admin/jobs', jobData);
    return response.data;
  },

  updateJob: async (jobId, jobData) => {
    const response = await apiClient.put(`/admin/jobs/${jobId}`, jobData);
    return response.data;
  },

  deleteJob: async (jobId) => {
    const response = await apiClient.delete(`/admin/jobs/${jobId}`);
    return response.data;
  },

  // Internships
  getInternships: async (params = {}) => {
    const response = await apiClient.get('/admin/internships', { params });
    return response.data;
  },

  createInternship: async (internshipData) => {
    const response = await apiClient.post('/admin/internships', internshipData);
    return response.data;
  },

  updateInternship: async (internshipId, internshipData) => {
    const response = await apiClient.put(`/admin/internships/${internshipId}`, internshipData);
    return response.data;
  },

  deleteInternship: async (internshipId) => {
    const response = await apiClient.delete(`/admin/internships/${internshipId}`);
    return response.data;
  },

  // Articles
  getArticles: async (params = {}) => {
    const response = await apiClient.get('/admin/articles', { params });
    return response.data;
  },

  createArticle: async (articleData) => {
    const response = await apiClient.post('/admin/articles', articleData);
    return response.data;
  },

  updateArticle: async (articleId, articleData) => {
    const response = await apiClient.put(`/admin/articles/${articleId}`, articleData);
    return response.data;
  },

  deleteArticle: async (articleId) => {
    const response = await apiClient.delete(`/admin/articles/${articleId}`);
    return response.data;
  },

  // Roadmaps
  getRoadmaps: async (params = {}) => {
    const response = await apiClient.get('/admin/roadmaps', { params });
    return response.data;
  },

  createRoadmap: async (roadmapData) => {
    const response = await apiClient.post('/admin/roadmaps', roadmapData);
    return response.data;
  },

  updateRoadmap: async (roadmapId, roadmapData) => {
    const response = await apiClient.put(`/admin/roadmaps/${roadmapId}`, roadmapData);
    return response.data;
  },

  deleteRoadmap: async (roadmapId) => {
    const response = await apiClient.delete(`/admin/roadmaps/${roadmapId}`);
    return response.data;
  },

  // DSA Corner management
  getDSAProblems: async (params = {}) => {
    const response = await apiClient.get('/admin/dsa-problems', { params });
    return response.data;
  },

  createDSAProblem: async (dsaProblemData) => {
    const response = await apiClient.post('/admin/dsa-problems', dsaProblemData);
    return response.data;
  },

  updateDSAProblem: async (dsaProblemId, dsaProblemData) => {
    const response = await apiClient.put(`/admin/dsa-problems/${dsaProblemId}`, dsaProblemData);
    return response.data;
  },

  deleteDSAProblem: async (dsaProblemId) => {
    const response = await apiClient.delete(`/admin/dsa-problems/${dsaProblemId}`);
    return response.data;
  }
};

// AI API functions
export const aiApi = {
  // AI Agent Routes
  generateJobContent: (prompt) =>
    axios.post(`${API}/ai-agent/generate/job`, { prompt }),
  generateInternshipContent: (prompt) =>
    axios.post(`${API}/ai-agent/generate/internship`, { prompt }),
  generateArticleContent: (prompt) =>
    axios.post(`${API}/ai-agent/generate/article`, { prompt }),
  generateRoadmapContent: (prompt) =>
    axios.post(`${API}/ai-agent/generate/roadmap`, { prompt }),
  generateDSAProblemContent: (prompt) =>
    axios.post(`${API}/ai-agent/generate/dsa-problem`, { prompt }),


  // New AI Routes
  aiGenerateJob: (prompt) =>
    apiClient.post(`/ai/generate-job?prompt=${encodeURIComponent(prompt)}`),
  aiGenerateInternship: (prompt) =>
    apiClient.post(`/ai/generate-internship?prompt=${encodeURIComponent(prompt)}`),
  aiGenerateArticle: (prompt) =>
    apiClient.post(`/ai/generate-article?prompt=${encodeURIComponent(prompt)}`),
  aiGenerateRoadmap: (prompt) =>
    apiClient.post(`/ai/generate-roadmap?prompt=${encodeURIComponent(prompt)}`),
  aiGenerateDSAProblem: (prompt) =>
    apiClient.post(`/ai/generate-dsa-problem?prompt=${encodeURIComponent(prompt)}`),
  aiGenerateMultiple: (contentType, prompt, count) =>
    apiClient.post(`/ai/generate-all?content_type=${contentType}&prompt=${encodeURIComponent(prompt)}&count=${count}`),


  analyzeResume: async (resumeText, jobDescription = null, targetRole = null) => {
    const response = await axios.post(`${API}/public-ai/analyze-resume`, {
      resume_text: resumeText,
      job_description: jobDescription,
      target_role: targetRole
    });
    return response.data;
  }
};

// Public API functions
export const publicApi = {
  getJobs: async (params = {}) => {
    const response = await axios.get(`${API}/public/jobs`, { params });
    return response.data;
  },

  getJob: async (jobId) => {
    const response = await axios.get(`${API}/public/jobs/${jobId}`);
    return response.data;
  },

  getInternships: async (params = {}) => {
    const response = await axios.get(`${API}/public/internships`, { params });
    return response.data;
  },

  getInternship: async (internshipId) => {
    const response = await axios.get(`${API}/public/internships/${internshipId}`);
    return response.data;
  },

  getArticles: async (params = {}) => {
    const response = await axios.get(`${API}/public/articles`, { params });
    return response.data;
  },

  getArticle: async (slug) => {
    const response = await axios.get(`${API}/public/articles/${slug}`);
    return response.data;
  },

  getRoadmaps: async (params = {}) => {
    const response = await axios.get(`${API}/public/roadmaps`, { params });
    return response.data;
  },

  getRoadmap: async (slug) => {
    const response = await axios.get(`${API}/public/roadmaps/${slug}`);
    return response.data;
  },

  getDSAProblems: async (params = {}) => {
    const response = await axios.get(`${API}/public/dsa-problems`, { params });
    return response.data;
  },

  getDSAProblem: async (slug) => {
    const response = await axios.get(`${API}/public/dsa-problems/${slug}`);
    return response.data;
  },

  getStats: async () => {
    const response = await axios.get(`${API}/public/stats`);
    return response.data;
  },

  search: async (query, contentType = null, limit = 10) => {
    const response = await axios.get(`${API}/public/search`, {
      params: { q: query, content_type: contentType, limit }
    });
    return response.data;
  }
};