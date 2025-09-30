import React, { useState, useEffect } from "react";
import { Plus, Search, Edit, Trash2, DollarSign, MapPin, Calendar, Building } from "lucide-react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Badge } from "../ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "../ui/dialog";
import { Label } from "../ui/label";
import { Textarea } from "../ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { useToast } from "../ui/use-toast";
import { adminApi } from "../../services/api";

// Import apiClient for direct API calls
import axios from "axios";
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const apiClient = axios.create({
  baseURL: `${BACKEND_URL}/api`,
  timeout: 30000,
});

// Add auth interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('adminToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const JobManagement = () => {
  const [jobs, setJobs] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const { toast } = useToast();

  const [formData, setFormData] = useState({
    title: "",
    company: "",
    location: "",
    job_type: "",
    experience_level: "",
    salary_range: "",
    description: "",
    requirements: "",
    responsibilities: "",
    skills: "",
    application_url: "",
    expiration_date: "",
    is_featured: false,
    is_active: true
  });

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const response = await adminApi.getJobs();
      setJobs(response);
    } catch (error) {
      console.error("Error fetching jobs:", error);
      toast({
        title: "Error",
        description: "Failed to fetch jobs",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Validate required fields
      if (!formData.title?.trim()) {
        throw new Error('Job title is required');
      }
      if (!formData.company?.trim()) {
        throw new Error('Company name is required');
      }
      if (!formData.description?.trim()) {
        throw new Error('Job description is required');
      }

      const jobData = {
        ...formData,
        skills: formData.skills.split(',').map(skill => skill.trim()).filter(skill => skill),
        requirements: formData.requirements.split('\n').filter(req => req.trim()),
        responsibilities: formData.responsibilities.split('\n').filter(resp => resp.trim()),
        expiration_date: formData.expiration_date ? new Date(formData.expiration_date).toISOString() : null
      };

      let response;
      if (selectedJob) {
        response = await adminApi.updateJob(selectedJob.id, jobData);
        toast({
          title: "Success!",
          description: "Job updated successfully and saved to database"
        });
      } else {
        response = await adminApi.createJob(jobData);
        toast({
          title: "Success!",
          description: "Job created successfully and saved to database"
        });
      }

      setIsDialogOpen(false);
      resetForm();
      await fetchJobs(); // Refresh the list
    } catch (error) {
      console.error("Error saving job:", error);
      
      let errorMessage = "Failed to save job. Please try again.";
      
      if (error.response?.status === 401) {
        errorMessage = "Authentication failed. Please log in again.";
      } else if (error.response?.status === 400) {
        errorMessage = error.response?.data?.detail || "Invalid job data. Please check all fields.";
      } else if (error.response?.status >= 500) {
        errorMessage = "Server error. Please try again in a moment.";
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      toast({
        title: "Save Failed",
        description: errorMessage,
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (job) => {
    setSelectedJob(job);

    // Format expiration_date for datetime-local input
    let formattedExpirationDate = '';
    if (job.expiration_date) {
      const date = new Date(job.expiration_date);
      formattedExpirationDate = date.toISOString().slice(0, 16);
    }

    setFormData({
      title: job.title,
      company: job.company,
      location: job.location,
      job_type: job.job_type,
      experience_level: job.experience_level,
      salary_range: job.salary_range,
      description: job.description,
      requirements: job.requirements?.join('\n') || '',
      responsibilities: job.responsibilities?.join('\n') || '',
      skills: job.skills?.join(', ') || '',
      application_url: job.application_url,
      expiration_date: formattedExpirationDate,
      is_featured: job.is_featured,
      is_active: job.is_active
    });
    setIsDialogOpen(true);
  };

  const handleDelete = async (jobId) => {
    if (window.confirm("Are you sure you want to delete this job?")) {
      try {
        await adminApi.deleteJob(jobId);
        toast({
          title: "Success",
          description: "Job deleted successfully"
        });
        fetchJobs();
      } catch (error) {
        console.error("Error deleting job:", error);
        toast({
          title: "Error",
          description: "Failed to delete job",
          variant: "destructive"
        });
      }
    }
  };

  const resetForm = () => {
    setFormData({
      title: "",
      company: "",
      location: "",
      job_type: "",
      experience_level: "",
      salary_range: "",
      description: "",
      requirements: "",
      responsibilities: "",
      skills: "",
      application_url: "",
      expiration_date: "",
      is_featured: false,
      is_active: true
    });
    setSelectedJob(null);
  };

  const filteredJobs = jobs.filter(job =>
    job.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.company?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.location?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Job Management</h1>
        </div>
        <div className="text-center py-8">Loading jobs...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Job Management</h1>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={resetForm}>
              <Plus className="w-4 h-4 mr-2" />
              Add New Job
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>
                {selectedJob ? "Edit Job" : "Add New Job"}
              </DialogTitle>
              <p className="text-sm text-muted-foreground">
                {selectedJob ? "Modify the job details below" : "Fill in the details to create a new job posting"}
              </p>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* AI Agent Section */}
              <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg border border-blue-200">
                <div className="flex items-center space-x-2 mb-3">
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">AI</span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">AI Job Generator</h3>
                </div>
                <div className="space-y-3">
                  <div>
                    <Label htmlFor="ai-prompt">Describe the job you want to create</Label>
                    <Textarea
                      id="ai-prompt"
                      placeholder="e.g., Senior Frontend Developer at a fintech startup in Mumbai, React expertise required, remote work available, competitive salary"
                      rows={2}
                      className="resize-none"
                    />
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                    <div>
                      <Label htmlFor="ai-company">Company (optional)</Label>
                      <Input
                        id="ai-company"
                        placeholder="Company name"
                        className="text-sm"
                      />
                    </div>
                    <div>
                      <Label htmlFor="ai-location">Location (optional)</Label>
                      <Input
                        id="ai-location"
                        placeholder="City, Country"
                        className="text-sm"
                      />
                    </div>
                    <div>
                      <Label htmlFor="ai-level">Experience Level</Label>
                      <Input
                        id="ai-level"
                        placeholder="e.g., entry, mid, senior, lead"
                        className="text-sm"
                      />
                    </div>
                  </div>
                  <Button 
                    type="button" 
                    className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                    onClick={async () => {
                      const promptElement = document.getElementById('ai-prompt');
                      const companyElement = document.getElementById('ai-company');
                      const locationElement = document.getElementById('ai-location');
                      
                      const basePrompt = promptElement?.value || 'Generate a software developer job posting';
                      const company = companyElement?.value || '';
                      const location = locationElement?.value || '';
                      const levelElement = document.getElementById('ai-level');
                      const level = levelElement?.value || '';
                      
                      let fullPrompt = basePrompt;
                      if (company) fullPrompt += ` at ${company}`;
                      if (location) fullPrompt += ` in ${location}`;
                      if (level) fullPrompt += ` for ${level} level`;
                      
                      try {
                        const response = await apiClient.post(`/ai/generate-job?prompt=${encodeURIComponent(fullPrompt)}`);
                        const data = response.data;
                        
                        if (!data.content) {
                          throw new Error('No content received from AI');
                        }
                        
                        const content = data.content;
                        setFormData({
                          ...formData,
                          title: content.title || formData.title,
                          company: content.company || company || formData.company,
                          description: content.description || formData.description,
                          requirements: content.requirements?.join('\n') || formData.requirements,
                          responsibilities: content.responsibilities?.join('\n') || formData.responsibilities,
                          skills: content.skills_required?.join(', ') || formData.skills,
                          location: content.location || location || formData.location,
                          salary_range: content.salary_range || formData.salary_range,
                          job_type: content.job_type || formData.job_type,
                          experience_level: content.experience_level || level || formData.experience_level
                        });
                        
                        toast({
                          title: "Success!",
                          description: "Form auto-filled with AI-generated content. Review and modify as needed."
                        });
                      } catch (error) {
                        console.error('AI Generation Error:', error);
                        toast({
                          title: "AI Generation Failed",
                          description: error.message || "Please try again with a different prompt or check your connection.",
                          variant: "destructive"
                        });
                      }
                    }}
                  >
                    🤖 Generate Job with AI
                  </Button>
                </div>
              </div>
              
              {/* Job Form Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="title">Job Title</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="company">Company</Label>
                  <Input
                    id="company"
                    value={formData.company}
                    onChange={(e) => setFormData({...formData, company: e.target.value})}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="location">Location</Label>
                  <Input
                    id="location"
                    value={formData.location}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="job_type">Job Type</Label>
                  <Select value={formData.job_type} onValueChange={(value) => setFormData({...formData, job_type: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select job type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="full-time">Full Time</SelectItem>
                      <SelectItem value="part-time">Part Time</SelectItem>
                      <SelectItem value="contract">Contract</SelectItem>
                      <SelectItem value="remote">Remote</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="experience_level">Experience Level</Label>
                  <Select value={formData.experience_level} onValueChange={(value) => setFormData({...formData, experience_level: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select experience level" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="entry">Entry Level</SelectItem>
                      <SelectItem value="mid">Mid Level</SelectItem>
                      <SelectItem value="senior">Senior Level</SelectItem>
                      <SelectItem value="lead">Lead</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="salary_range">Salary Range</Label>
                  <Input
                    id="salary_range"
                    value={formData.salary_range}
                    onChange={(e) => setFormData({...formData, salary_range: e.target.value})}
                    placeholder="e.g., $50,000 - $80,000"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="description">Job Description</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  rows={4}
                  required
                />
              </div>

              <div>
                <Label htmlFor="requirements">Requirements (one per line)</Label>
                <Textarea
                  id="requirements"
                  value={formData.requirements}
                  onChange={(e) => setFormData({...formData, requirements: e.target.value})}
                  rows={4}
                  placeholder="Bachelor's degree in Computer Science\n3+ years of experience\nProficiency in JavaScript"
                />
              </div>

              <div>
                <Label htmlFor="responsibilities">Responsibilities (one per line)</Label>
                <Textarea
                  id="responsibilities"
                  value={formData.responsibilities}
                  onChange={(e) => setFormData({...formData, responsibilities: e.target.value})}
                  rows={4}
                  placeholder="Develop web applications\nCollaborate with team members\nWrite clean, maintainable code"
                />
              </div>

              <div>
                <Label htmlFor="skills">Skills (comma separated)</Label>
                <Input
                  id="skills"
                  value={formData.skills}
                  onChange={(e) => setFormData({...formData, skills: e.target.value})}
                  placeholder="JavaScript, React, Node.js, MongoDB"
                />
              </div>

              <div>
                <Label htmlFor="application_url">Application URL</Label>
                <Input
                  id="application_url"
                  type="url"
                  value={formData.application_url}
                  onChange={(e) => setFormData({...formData, application_url: e.target.value})}
                  placeholder="https://company.com/apply"
                />
              </div>

              <div>
                <Label htmlFor="expiration_date">Expiration Date (Auto-delete)</Label>
                <Input
                  id="expiration_date"
                  type="datetime-local"
                  value={formData.expiration_date || ''}
                  onChange={(e) => setFormData({...formData, expiration_date: e.target.value})}
                />
                <p className="text-sm text-gray-500 mt-1">Job will be automatically deleted from database on this date</p>
              </div>

              <div className="flex items-center space-x-4">
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.is_featured}
                    onChange={(e) => setFormData({...formData, is_featured: e.target.checked})}
                  />
                  <span>Featured Job</span>
                </label>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.is_active}
                    onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
                  />
                  <span>Active</span>
                </label>
              </div>

              <div className="flex justify-end space-x-2">
                <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                      {selectedJob ? "Updating..." : "Creating..."}
                    </>
                  ) : (
                    selectedJob ? "Update Job" : "Create Job"
                  )}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="flex items-center space-x-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            placeholder="Search jobs by title, company, or location..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="grid gap-6">
        {filteredJobs.length === 0 ? (
          <Card>
            <CardContent className="text-center py-8">
              <p className="text-gray-500">No jobs found</p>
            </CardContent>
          </Card>
        ) : (
          filteredJobs.map((job) => (
            <Card key={job.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="space-y-2">
                    <CardTitle className="text-xl">{job.title}</CardTitle>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <div className="flex items-center space-x-1">
                        <Building className="w-4 h-4" />
                        <span>{job.company}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <MapPin className="w-4 h-4" />
                        <span>{job.location}</span>
                      </div>
                      {job.salary_range && (
                        <div className="flex items-center space-x-1">
                          <DollarSign className="w-4 h-4" />
                          <span>{job.salary_range}</span>
                        </div>
                      )}
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge variant={job.job_type === 'full-time' ? 'default' : 'secondary'}>
                        {job.job_type}
                      </Badge>
                      <Badge variant="outline">
                        {job.experience_level}
                      </Badge>
                      {job.is_featured && (
                        <Badge variant="destructive">Featured</Badge>
                      )}
                      <Badge variant={job.is_active ? 'default' : 'secondary'}>
                        {job.is_active ? 'Active' : 'Inactive'}
                      </Badge>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEdit(job)}
                    >
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(job.id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-4">{job.description}</p>
                {job.skills && job.skills.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="font-semibold text-sm">Required Skills:</h4>
                    <div className="flex flex-wrap gap-2">
                      {job.skills.map((skill, index) => (
                        <Badge key={index} variant="outline">{skill}</Badge>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default JobManagement;