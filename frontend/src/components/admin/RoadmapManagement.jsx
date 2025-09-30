import React, { useState, useEffect } from "react";
import { Plus, Search, Edit, Trash2, Map, Calendar, User, Star, Target } from "lucide-react";
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

const RoadmapManagement = () => {
  const [roadmaps, setRoadmaps] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedRoadmap, setSelectedRoadmap] = useState(null);
  const { toast } = useToast();

  const [formData, setFormData] = useState({
    title: "",
    slug: "",
    description: "",
    category: "",
    difficulty_level: "",
    estimated_duration: "",
    prerequisites: "",
    learning_outcomes: "",
    content: "",
    resources: "",
    milestones: "",
    tags: "",
    featured_image: "",
    is_published: false,
    is_featured: false
  });

  useEffect(() => {
    fetchRoadmaps();
  }, []);

  const fetchRoadmaps = async () => {
    try {
      setLoading(true);
      const response = await adminApi.getRoadmaps();
      setRoadmaps(response);
    } catch (error) {
      console.error("Error fetching roadmaps:", error);
      toast({
        title: "Error",
        description: "Failed to fetch roadmaps",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const generateSlug = (title) => {
    return title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '');
  };

  const handleTitleChange = (title) => {
    setFormData({
      ...formData,
      title,
      slug: selectedRoadmap ? formData.slug : generateSlug(title)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Validate required fields
      if (!formData.title?.trim()) {
        throw new Error('Roadmap title is required');
      }
      if (!formData.description?.trim()) {
        throw new Error('Roadmap description is required');
      }
      if (!formData.content?.trim()) {
        throw new Error('Roadmap content is required');
      }

      const roadmapData = {
        ...formData,
        tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag),
        prerequisites: formData.prerequisites.split('\n').filter(req => req.trim()),
        learning_outcomes: formData.learning_outcomes.split('\n').filter(outcome => outcome.trim()),
        resources: formData.resources.split('\n').filter(resource => resource.trim()),
        milestones: formData.milestones.split('\n').filter(milestone => milestone.trim())
      };

      if (selectedRoadmap) {
        await adminApi.updateRoadmap(selectedRoadmap.id, roadmapData);
        toast({
          title: "Success!",
          description: "Roadmap updated successfully and saved to database"
        });
      } else {
        await adminApi.createRoadmap(roadmapData);
        toast({
          title: "Success!",
          description: "Roadmap created successfully and saved to database"
        });
      }
      
      setIsDialogOpen(false);
      resetForm();
      await fetchRoadmaps(); // Refresh the list
    } catch (error) {
      console.error("Error saving roadmap:", error);
      
      let errorMessage = "Failed to save roadmap. Please try again.";
      
      if (error.response?.status === 401) {
        errorMessage = "Authentication failed. Please log in again.";
      } else if (error.response?.status === 400) {
        errorMessage = error.response?.data?.detail || "Invalid roadmap data. Please check all fields.";
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

  const handleEdit = (roadmap) => {
    setSelectedRoadmap(roadmap);
    setFormData({
      title: roadmap.title,
      slug: roadmap.slug,
      description: roadmap.description,
      category: roadmap.category,
      difficulty_level: roadmap.difficulty_level,
      estimated_duration: roadmap.estimated_duration,
      prerequisites: roadmap.prerequisites?.join('\n') || '',
      learning_outcomes: roadmap.learning_outcomes?.join('\n') || '',
      content: roadmap.content,
      resources: roadmap.resources?.join('\n') || '',
      milestones: roadmap.milestones?.join('\n') || '',
      tags: roadmap.tags?.join(', ') || '',
      featured_image: roadmap.featured_image || '',
      is_published: roadmap.is_published,
      is_featured: roadmap.is_featured
    });
    setIsDialogOpen(true);
  };

  const handleDelete = async (roadmapId) => {
    if (window.confirm("Are you sure you want to delete this roadmap?")) {
      try {
        await adminApi.deleteRoadmap(roadmapId);
        toast({
          title: "Success",
          description: "Roadmap deleted successfully"
        });
        fetchRoadmaps();
      } catch (error) {
        console.error("Error deleting roadmap:", error);
        toast({
          title: "Error",
          description: "Failed to delete roadmap",
          variant: "destructive"
        });
      }
    }
  };

  const resetForm = () => {
    setFormData({
      title: "",
      slug: "",
      description: "",
      category: "",
      difficulty_level: "",
      estimated_duration: "",
      prerequisites: "",
      learning_outcomes: "",
      content: "",
      resources: "",
      milestones: "",
      tags: "",
      featured_image: "",
      is_published: false,
      is_featured: false
    });
    setSelectedRoadmap(null);
  };

  const filteredRoadmaps = roadmaps.filter(roadmap =>
    roadmap.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    roadmap.category?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    roadmap.difficulty_level?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getDifficultyColor = (level) => {
    switch (level) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Roadmap Management</h1>
        </div>
        <div className="text-center py-8">Loading roadmaps...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Roadmap Management</h1>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={resetForm}>
              <Plus className="w-4 h-4 mr-2" />
              Add New Roadmap
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>
                {selectedRoadmap ? "Edit Roadmap" : "Add New Roadmap"}
              </DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* AI Agent Section */}
              <div className="bg-gradient-to-r from-orange-50 to-red-50 p-4 rounded-lg border border-orange-200">
                <div className="flex items-center space-x-2 mb-3">
                  <div className="w-8 h-8 bg-orange-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">AI</span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">AI Roadmap Generator</h3>
                </div>
                <div className="space-y-3">
                  <div>
                    <Label htmlFor="ai-prompt">Describe the learning roadmap you want to create</Label>
                    <Textarea
                      id="ai-prompt"
                      placeholder="e.g., Complete roadmap to become a full-stack developer, data science learning path for beginners, cybersecurity career roadmap"
                      rows={2}
                      className="resize-none"
                    />
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                    <div>
                      <Label htmlFor="ai-category">Category</Label>
                      <Input
                        id="ai-category"
                        placeholder="e.g., web-development, data-science, ai-ml"
                        className="text-sm"
                      />
                    </div>
                    <div>
                      <Label htmlFor="ai-difficulty">Difficulty Level</Label>
                      <Input
                        id="ai-difficulty"
                        placeholder="e.g., beginner, intermediate, advanced"
                        className="text-sm"
                      />
                    </div>
                    <div>
                      <Label htmlFor="ai-duration">Duration (optional)</Label>
                      <Input
                        id="ai-duration"
                        placeholder="e.g., 6 months, 12 weeks"
                        className="text-sm"
                      />
                    </div>
                  </div>
                  <Button 
                    type="button" 
                    className="w-full bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700"
                    onClick={async () => {
                      const promptElement = document.getElementById('ai-prompt');
                      const durationElement = document.getElementById('ai-duration');
                      
                      const basePrompt = promptElement?.value || 'Generate a comprehensive learning roadmap';
                      const duration = durationElement?.value || '';
                      const categoryElement = document.getElementById('ai-category');
                      const difficultyElement = document.getElementById('ai-difficulty');
                      const category = categoryElement?.value || '';
                      const difficulty = difficultyElement?.value || '';
                      
                      let fullPrompt = basePrompt;
                      if (category) fullPrompt += ` for ${category}`;
                      if (difficulty) fullPrompt += ` at ${difficulty} level`;
                      if (duration) fullPrompt += ` with ${duration} duration`;
                      
                      try {
                        const response = await apiClient.post(`/ai/generate-roadmap?prompt=${encodeURIComponent(fullPrompt)}`);
                        const data = response.data;
                        
                        if (!data.content) {
                          throw new Error('No content received from AI');
                        }
                        
                        const content = data.content;
                        setFormData({
                          ...formData,
                          title: content.title || formData.title,
                          description: content.description || formData.description,
                          content: content.content || formData.content,
                          category: content.category || category || formData.category,
                          difficulty_level: content.difficulty_level || difficulty || formData.difficulty_level,
                          estimated_duration: content.estimated_duration || duration || formData.estimated_duration,
                          prerequisites: content.prerequisites?.join('\n') || formData.prerequisites,
                          learning_outcomes: content.learning_outcomes?.join('\n') || formData.learning_outcomes,
                          resources: content.resources?.join('\n') || formData.resources,
                          milestones: content.milestones?.join('\n') || formData.milestones,
                          tags: content.tags?.join(', ') || formData.tags,
                          slug: content.slug || generateSlug(content.title || formData.title)
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
                    🤖 Generate Roadmap with AI
                  </Button>
                </div>
              </div>
              
              {/* Roadmap Form Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="title">Roadmap Title</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => handleTitleChange(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="slug">Slug</Label>
                  <Input
                    id="slug"
                    value={formData.slug}
                    onChange={(e) => setFormData({...formData, slug: e.target.value})}
                    required
                    placeholder="roadmap-url-slug"
                  />
                </div>
                <div>
                  <Label htmlFor="category">Category</Label>
                  <Select value={formData.category} onValueChange={(value) => setFormData({...formData, category: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="web-development">Web Development</SelectItem>
                      <SelectItem value="mobile-development">Mobile Development</SelectItem>
                      <SelectItem value="data-science">Data Science</SelectItem>
                      <SelectItem value="devops">DevOps</SelectItem>
                      <SelectItem value="cybersecurity">Cybersecurity</SelectItem>
                      <SelectItem value="ai-ml">AI/ML</SelectItem>
                      <SelectItem value="backend">Backend Development</SelectItem>
                      <SelectItem value="frontend">Frontend Development</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="difficulty_level">Difficulty Level</Label>
                  <Select value={formData.difficulty_level} onValueChange={(value) => setFormData({...formData, difficulty_level: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select difficulty" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="beginner">Beginner</SelectItem>
                      <SelectItem value="intermediate">Intermediate</SelectItem>
                      <SelectItem value="advanced">Advanced</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="estimated_duration">Estimated Duration</Label>
                  <Input
                    id="estimated_duration"
                    value={formData.estimated_duration}
                    onChange={(e) => setFormData({...formData, estimated_duration: e.target.value})}
                    placeholder="e.g., 3 months, 6 weeks"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="featured_image">Featured Image URL</Label>
                  <Input
                    id="featured_image"
                    type="url"
                    value={formData.featured_image}
                    onChange={(e) => setFormData({...formData, featured_image: e.target.value})}
                    placeholder="https://example.com/image.jpg"
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  rows={3}
                  required
                  placeholder="Brief description of the roadmap..."
                />
              </div>
              
              <div>
                <Label htmlFor="content">Detailed Content</Label>
                <Textarea
                  id="content"
                  value={formData.content}
                  onChange={(e) => setFormData({...formData, content: e.target.value})}
                  rows={6}
                  required
                  placeholder="Detailed roadmap content and instructions..."
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="prerequisites">Prerequisites (one per line)</Label>
                  <Textarea
                    id="prerequisites"
                    value={formData.prerequisites}
                    onChange={(e) => setFormData({...formData, prerequisites: e.target.value})}
                    rows={4}
                    placeholder="Basic programming knowledge\nFamiliarity with HTML/CSS"
                  />
                </div>
                <div>
                  <Label htmlFor="learning_outcomes">Learning Outcomes (one per line)</Label>
                  <Textarea
                    id="learning_outcomes"
                    value={formData.learning_outcomes}
                    onChange={(e) => setFormData({...formData, learning_outcomes: e.target.value})}
                    rows={4}
                    placeholder="Build full-stack applications\nUnderstand API development"
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="resources">Resources (one per line)</Label>
                  <Textarea
                    id="resources"
                    value={formData.resources}
                    onChange={(e) => setFormData({...formData, resources: e.target.value})}
                    rows={4}
                    placeholder="Official documentation\nOnline courses\nBooks"
                  />
                </div>
                <div>
                  <Label htmlFor="milestones">Milestones (one per line)</Label>
                  <Textarea
                    id="milestones"
                    value={formData.milestones}
                    onChange={(e) => setFormData({...formData, milestones: e.target.value})}
                    rows={4}
                    placeholder="Complete basic syntax\nBuild first project\nDeploy application"
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="tags">Tags (comma separated)</Label>
                <Input
                  id="tags"
                  value={formData.tags}
                  onChange={(e) => setFormData({...formData, tags: e.target.value})}
                  placeholder="javascript, react, nodejs, career"
                />
              </div>
              
              <div className="flex items-center space-x-4">
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.is_published}
                    onChange={(e) => setFormData({...formData, is_published: e.target.checked})}
                  />
                  <span>Published</span>
                </label>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.is_featured}
                    onChange={(e) => setFormData({...formData, is_featured: e.target.checked})}
                  />
                  <span>Featured Roadmap</span>
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
                      {selectedRoadmap ? "Updating..." : "Creating..."}
                    </>
                  ) : (
                    selectedRoadmap ? "Update Roadmap" : "Create Roadmap"
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
            placeholder="Search roadmaps by title, category, or difficulty..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="grid gap-6">
        {filteredRoadmaps.length === 0 ? (
          <Card>
            <CardContent className="text-center py-8">
              <p className="text-gray-500">No roadmaps found</p>
            </CardContent>
          </Card>
        ) : (
          filteredRoadmaps.map((roadmap) => (
            <Card key={roadmap.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="space-y-2 flex-1">
                    <CardTitle className="text-xl">{roadmap.title}</CardTitle>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <div className="flex items-center space-x-1">
                        <Map className="w-4 h-4" />
                        <span>{roadmap.category}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Target className="w-4 h-4" />
                        <span>{roadmap.estimated_duration}</span>
                      </div>
                      {roadmap.created_at && (
                        <div className="flex items-center space-x-1">
                          <Calendar className="w-4 h-4" />
                          <span>{formatDate(roadmap.created_at)}</span>
                        </div>
                      )}
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge variant={roadmap.is_published ? 'default' : 'secondary'}>
                        {roadmap.is_published ? 'Published' : 'Draft'}
                      </Badge>
                      {roadmap.is_featured && (
                        <Badge variant="destructive">Featured</Badge>
                      )}
                      <Badge className={getDifficultyColor(roadmap.difficulty_level)}>
                        {roadmap.difficulty_level}
                      </Badge>
                      <Badge variant="outline">{roadmap.category}</Badge>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEdit(roadmap)}
                    >
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(roadmap.id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-4">{roadmap.description}</p>
                {roadmap.featured_image && (
                  <div className="mb-4">
                    <img 
                      src={roadmap.featured_image} 
                      alt={roadmap.title}
                      className="w-full h-48 object-cover rounded-lg"
                      onError={(e) => {
                        e.target.style.display = 'none';
                      }}
                    />
                  </div>
                )}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  {roadmap.prerequisites && roadmap.prerequisites.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-sm mb-2">Prerequisites:</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {roadmap.prerequisites.slice(0, 3).map((prereq, index) => (
                          <li key={index}>• {prereq}</li>
                        ))}
                        {roadmap.prerequisites.length > 3 && (
                          <li className="text-gray-400">... and {roadmap.prerequisites.length - 3} more</li>
                        )}
                      </ul>
                    </div>
                  )}
                  {roadmap.learning_outcomes && roadmap.learning_outcomes.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-sm mb-2">Learning Outcomes:</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {roadmap.learning_outcomes.slice(0, 3).map((outcome, index) => (
                          <li key={index}>• {outcome}</li>
                        ))}
                        {roadmap.learning_outcomes.length > 3 && (
                          <li className="text-gray-400">... and {roadmap.learning_outcomes.length - 3} more</li>
                        )}
                      </ul>
                    </div>
                  )}
                </div>
                {roadmap.tags && roadmap.tags.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="font-semibold text-sm">Tags:</h4>
                    <div className="flex flex-wrap gap-2">
                      {roadmap.tags.map((tag, index) => (
                        <Badge key={index} variant="outline">{tag}</Badge>
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

export default RoadmapManagement;