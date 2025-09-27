import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Admin API functions
export const adminApi = {
  // Dashboard
  getDashboardStats: async () => {
    const response = await axios.get(`${API}/admin/dashboard/stats`);
    return response.data;
  },

  // Jobs
  getJobs: async (params = {}) => {
    const response = await axios.get(`${API}/admin/jobs`, { params });
    return response.data;
  },
  
  createJob: async (jobData) => {
    const response = await axios.post(`${API}/admin/jobs`, jobData);
    return response.data;
  },
  
  updateJob: async (jobId, jobData) => {
    const response = await axios.put(`${API}/admin/jobs/${jobId}`, jobData);
    return response.data;
  },
  
  deleteJob: async (jobId) => {
    const response = await axios.delete(`${API}/admin/jobs/${jobId}`);
    return response.data;
  },

  // Internships
  getInternships: async (params = {}) => {
    const response = await axios.get(`${API}/admin/internships`, { params });
    return response.data;
  },
  
  createInternship: async (internshipData) => {
    const response = await axios.post(`${API}/admin/internships`, internshipData);
    return response.data;
  },
  
  updateInternship: async (internshipId, internshipData) => {
    const response = await axios.put(`${API}/admin/internships/${internshipId}`, internshipData);
    return response.data;
  },
  
  deleteInternship: async (internshipId) => {
    const response = await axios.delete(`${API}/admin/internships/${internshipId}`);
    return response.data;
  },

  // Articles
  getArticles: async (params = {}) => {
    const response = await axios.get(`${API}/admin/articles`, { params });
    return response.data;
  },
  
  createArticle: async (articleData) => {
    const response = await axios.post(`${API}/admin/articles`, articleData);
    return response.data;
  },
  
  updateArticle: async (articleId, articleData) => {
    const response = await axios.put(`${API}/admin/articles/${articleId}`, articleData);
    return response.data;
  },
  
  deleteArticle: async (articleId) => {
    const response = await axios.delete(`${API}/admin/articles/${articleId}`);
    return response.data;
  },

  // Roadmaps
  getRoadmaps: async (params = {}) => {
    const response = await axios.get(`${API}/admin/roadmaps`, { params });
    return response.data;
  },
  
  createRoadmap: async (roadmapData) => {
    const response = await axios.post(`${API}/admin/roadmaps`, roadmapData);
    return response.data;
  },
  
  updateRoadmap: async (roadmapId, roadmapData) => {
    const response = await axios.put(`${API}/admin/roadmaps/${roadmapId}`, roadmapData);
    return response.data;
  },
  
  deleteRoadmap: async (roadmapId) => {
    const response = await axios.delete(`${API}/admin/roadmaps/${roadmapId}`);
    return response.data;
  }
};

// AI API functions
export const aiApi = {
  generateContent: async (contentType, prompt, additionalContext = {}) => {
    const response = await axios.post(`${API}/ai/generate-content`, {
      content_type: contentType,
      prompt,
      additional_context: additionalContext
    });
    return response.data;
  },
  
  generateJobContent: async (prompt) => {
    const response = await axios.post(`${API}/ai/generate-job`, null, {
      params: { prompt }
    });
    return response.data;
  },
  
  generateInternshipContent: async (prompt) => {
    const response = await axios.post(`${API}/ai/generate-internship`, null, {
      params: { prompt }
    });
    return response.data;
  },
  
  generateArticleContent: async (prompt) => {
    const response = await axios.post(`${API}/ai/generate-article`, null, {
      params: { prompt }
    });
    return response.data;
  },
  
  generateRoadmapContent: async (prompt) => {
    const response = await axios.post(`${API}/ai/generate-roadmap`, null, {
      params: { prompt }
    });
    return response.data;
  },
  
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