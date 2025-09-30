import React, { useState, useEffect } from "react";
import { Plus, Search, Edit, Trash2, MapPin, Calendar, Building, GraduationCap } from "lucide-react";
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

const InternshipManagement = () => {
  const [internships, setInternships] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedInternship, setSelectedInternship] = useState(null);
  const { toast } = useToast();

  const [formData, setFormData] = useState({
    title: "",
    company: "",
    location: "",
    duration: "",
    stipend: "",
    description: "",
    requirements: "",
    responsibilities: "",
    skills: "",
    application_url: "",
    expiration_date: "",
    is_paid: false,
    is_remote: false,
    is_featured: false,
    is_active: true
  });

  useEffect(() => {
    fetchInternships();
  }, []);

  const fetchInternships = async () => {
    try {
      setLoading(true);
      const response = await adminApi.getInternships();
      setInternships(response);
    } catch (error) {
      console.error("Error fetching internships:", error);
      toast({
        title: "Error",
        description: "Failed to fetch internships",
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
        throw new Error('Internship title is required');
      }
      if (!formData.company?.trim()) {
        throw new Error('Company name is required');
      }
      if (!formData.description?.trim()) {
        throw new Error('Internship description is required');
      }

      const internshipData = {
        ...formData,
        skills: formData.skills.split(',').map(skill => skill.trim()).filter(skill => skill),
        requirements: formData.requirements.split('\n').filter(req => req.trim()),
        responsibilities: formData.responsibilities.split('\n').filter(resp => resp.trim()),
        expiration_date: formData.expiration_date ? new Date(formData.expiration_date).toISOString() : null
      };

      if (selectedInternship) {
        await adminApi.updateInternship(selectedInternship.id, internshipData);
        toast({
          title: "Success!",
          description: "Internship updated successfully and saved to database"
        });
      } else {
        await adminApi.createInternship(internshipData);
        toast({
          title: "Success!",
          description: "Internship created successfully and saved to database"
        });
      }
      
      setIsDialogOpen(false);
      resetForm();
      await fetchInternships(); // Refresh the list
    } catch (error) {
      console.error("Error saving internship:", error);
      
      let errorMessage = "Failed to save internship. Please try again.";
      
      if (error.response?.status === 401) {
        errorMessage = "Authentication failed. Please log in again.";
      } else if (error.response?.status === 400) {
        errorMessage = error.response?.data?.detail || "Invalid internship data. Please check all fields.";
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

  const handleEdit = (internship) => {
    setSelectedInternship(internship);
    setFormData({
      title: internship.title,
      company: internship.company,
      location: internship.location,
      duration: internship.duration,
      stipend: internship.stipend || '',
      description: internship.description,
      requirements: internship.requirements?.join('\n') || '',
      responsibilities: internship.responsibilities?.join('\n') || '',
      skills: internship.skills?.join(', ') || '',
      application_url: internship.application_url,
      is_paid: internship.is_paid || false,
      is_remote: internship.is_remote || false,
      is_featured: internship.is_featured,
      is_active: internship.is_active
    });
    setIsDialogOpen(true);
  };

  const handleDelete = async (internshipId) => {
    if (window.confirm("Are you sure you want to delete this internship?")) {
      try {
        await adminApi.deleteInternship(internshipId);
        toast({
          title: "Success",
          description: "Internship deleted successfully"
        });
        fetchInternships();
      } catch (error) {
        console.error("Error deleting internship:", error);
        toast({
          title: "Error",
          description: "Failed to delete internship",
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
      duration: "",
      stipend: "",
      description: "",
      requirements: "",
      responsibilities: "",
      skills: "",
      application_url: "",
      is_paid: false,
      is_remote: false,
      is_featured: false,
      is_active: true
    });
    setSelectedInternship(null);
  };

  const filteredInternships = internships.filter(internship =>
    internship.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    internship.company?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    internship.location?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Internship Management</h1>
        </div>
        <div className="text-center py-8">Loading internships...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Internship Management</h1>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={resetForm}>
              <Plus className="w-4 h-4 mr-2" />
              Add New Internship
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>
                {selectedInternship ? "Edit Internship" : "Add New Internship"}
              </DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* AI Agent Section */}
              <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg border border-green-200">
                <div className="flex items-center space-x-2 mb-3">
                  <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">AI</span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">AI Internship Generator</h3>
                </div>
                <div className="space-y-3">
                  <div>
                    <Label htmlFor="ai-prompt">Describe the internship you want to create</Label>
                    <Textarea
                      id="ai-prompt"
                      placeholder="e.g., Summer internship for computer science students in web development, 3 months duration, mentorship provided, stipend included"
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
                      <Label htmlFor="ai-duration">Duration (optional)</Label>
                      <Input
                        id="ai-duration"
                        placeholder="e.g., 3 months"
                        className="text-sm"
                      />
                    </div>
                  </div>
                  <Button 
                    type="button" 
                    className="w-full bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700"
                    onClick={async () => {
                      const promptElement = document.getElementById('ai-prompt');
                      const companyElement = document.getElementById('ai-company');
                      const locationElement = document.getElementById('ai-location');
                      const durationElement = document.getElementById('ai-duration');
                      
                      const basePrompt = promptElement?.value || 'Generate an internship posting for students';
                      const company = companyElement?.value || '';
                      const location = locationElement?.value || '';
                      const duration = durationElement?.value || '';
                      
                      let fullPrompt = basePrompt;
                      if (company) fullPrompt += ` at ${company}`;
                      if (location) fullPrompt += ` in ${location}`;
                      if (duration) fullPrompt += ` for ${duration}`;
                      
                      try {
                        const response = await apiClient.post(`/ai/generate-internship?prompt=${encodeURIComponent(fullPrompt)}`);
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
                          duration: content.duration || duration || formData.duration,
                          stipend: content.stipend || formData.stipend
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
                    🤖 Generate Internship with AI
                  </Button>
                </div>
              </div>
              
              {/* Internship Form Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="title">Internship Title</Label>
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
                  <Label htmlFor="duration">Duration</Label>
                  <Input
                    id="duration"
                    value={formData.duration}
                    onChange={(e) => setFormData({...formData, duration: e.target.value})}
                    placeholder="e.g., 3 months, 6 months"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="stipend">Stipend</Label>
                  <Input
                    id="stipend"
                    value={formData.stipend}
                    onChange={(e) => setFormData({...formData, stipend: e.target.value})}
                    placeholder="e.g., $500/month, Unpaid"
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
                  <p className="text-sm text-gray-500 mt-1">Internship will be automatically deleted from database on this date</p>
                </div>
              </div>
              
              <div>
                <Label htmlFor="description">Internship Description</Label>
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
                  placeholder="Currently pursuing Bachelor's degree\nBasic knowledge of programming\nStrong communication skills"
                />
              </div>
              
              <div>
                <Label htmlFor="responsibilities">Responsibilities (one per line)</Label>
                <Textarea
                  id="responsibilities"
                  value={formData.responsibilities}
                  onChange={(e) => setFormData({...formData, responsibilities: e.target.value})}
                  rows={4}
                  placeholder="Assist in software development\nParticipate in team meetings\nComplete assigned projects"
                />
              </div>
              
              <div>
                <Label htmlFor="skills">Skills (comma separated)</Label>
                <Input
                  id="skills"
                  value={formData.skills}
                  onChange={(e) => setFormData({...formData, skills: e.target.value})}
                  placeholder="JavaScript, React, Communication, Problem Solving"
                />
              </div>
              
              <div className="flex items-center space-x-4 flex-wrap">
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.is_paid}
                    onChange={(e) => setFormData({...formData, is_paid: e.target.checked})}
                  />
                  <span>Paid Internship</span>
                </label>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.is_remote}
                    onChange={(e) => setFormData({...formData, is_remote: e.target.checked})}
                  />
                  <span>Remote</span>
                </label>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.is_featured}
                    onChange={(e) => setFormData({...formData, is_featured: e.target.checked})}
                  />
                  <span>Featured</span>
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
                      {selectedInternship ? "Updating..." : "Creating..."}
                    </>
                  ) : (
                    selectedInternship ? "Update Internship" : "Create Internship"
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
            placeholder="Search internships by title, company, or location..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="grid gap-6">
        {filteredInternships.length === 0 ? (
          <Card>
            <CardContent className="text-center py-8">
              <p className="text-gray-500">No internships found</p>
            </CardContent>
          </Card>
        ) : (
          filteredInternships.map((internship) => (
            <Card key={internship.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="space-y-2">
                    <CardTitle className="text-xl">{internship.title}</CardTitle>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <div className="flex items-center space-x-1">
                        <Building className="w-4 h-4" />
                        <span>{internship.company}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <MapPin className="w-4 h-4" />
                        <span>{internship.location}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Calendar className="w-4 h-4" />
                        <span>{internship.duration}</span>
                      </div>
                      {internship.stipend && (
                        <div className="flex items-center space-x-1">
                          <GraduationCap className="w-4 h-4" />
                          <span>{internship.stipend}</span>
                        </div>
                      )}
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge variant={internship.is_paid ? 'default' : 'secondary'}>
                        {internship.is_paid ? 'Paid' : 'Unpaid'}
                      </Badge>
                      {internship.is_remote && (
                        <Badge variant="outline">Remote</Badge>
                      )}
                      {internship.is_featured && (
                        <Badge variant="destructive">Featured</Badge>
                      )}
                      <Badge variant={internship.is_active ? 'default' : 'secondary'}>
                        {internship.is_active ? 'Active' : 'Inactive'}
                      </Badge>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEdit(internship)}
                    >
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(internship.id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-4">{internship.description}</p>
                {internship.skills && internship.skills.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="font-semibold text-sm">Required Skills:</h4>
                    <div className="flex flex-wrap gap-2">
                      {internship.skills.map((skill, index) => (
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

export default InternshipManagement;