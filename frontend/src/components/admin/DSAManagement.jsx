
import React, { useState, useEffect } from "react";
import { Plus, Search, Edit, Trash2, Code, BookOpen, Target } from "lucide-react";
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

const DSAManagement = () => {
  const [dsaProblems, setDSAProblems] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedProblem, setSelectedProblem] = useState(null);
  const { toast } = useToast();

  const [formData, setFormData] = useState({
    title: "",
    description: "",
    difficulty: "",
    topic: "",
    problem_statement: "",
    input_format: "",
    output_format: "",
    constraints: "",
    examples: "",
    solution_approach: "",
    code_solution: "",
    time_complexity: "",
    space_complexity: "",
    tags: "",
    companies: "",
    is_premium: false,
    is_active: true
  });

  useEffect(() => {
    fetchDSAProblems();
  }, []);

  const fetchDSAProblems = async () => {
    try {
      setLoading(true);
      const response = await adminApi.getDSAProblems();
      setDSAProblems(response);
    } catch (error) {
      console.error("Error fetching DSA problems:", error);
      toast({
        title: "Error",
        description: "Failed to fetch DSA problems",
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
        throw new Error('Problem title is required');
      }
      if (!formData.description?.trim()) {
        throw new Error('Problem description is required');
      }
      if (!formData.problem_statement?.trim()) {
        throw new Error('Problem statement is required');
      }

      const problemData = {
        ...formData,
        tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag),
        companies: formData.companies.split(',').map(company => company.trim()).filter(company => company),
        examples: formData.examples.split('\n').filter(example => example.trim()),
        constraints: formData.constraints.split('\n').filter(constraint => constraint.trim())
      };

      if (selectedProblem) {
        await adminApi.updateDSAProblem(selectedProblem.id, problemData);
        toast({
          title: "Success!",
          description: "DSA problem updated successfully and saved to database"
        });
      } else {
        await adminApi.createDSAProblem(problemData);
        toast({
          title: "Success!",
          description: "DSA problem created successfully and saved to database"
        });
      }
      
      setIsDialogOpen(false);
      resetForm();
      await fetchDSAProblems(); // Refresh the list
    } catch (error) {
      console.error("Error saving DSA problem:", error);
      
      let errorMessage = "Failed to save DSA problem. Please try again.";
      
      if (error.response?.status === 401) {
        errorMessage = "Authentication failed. Please log in again.";
      } else if (error.response?.status === 400) {
        errorMessage = error.response?.data?.detail || "Invalid problem data. Please check all fields.";
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

  const handleEdit = (problem) => {
    setSelectedProblem(problem);
    setFormData({
      title: problem.title,
      description: problem.description,
      difficulty: problem.difficulty,
      topic: problem.topic,
      problem_statement: problem.problem_statement,
      input_format: problem.input_format,
      output_format: problem.output_format,
      constraints: problem.constraints?.join('\n') || '',
      examples: problem.examples?.join('\n') || '',
      solution_approach: problem.solution_approach,
      code_solution: problem.code_solution,
      time_complexity: problem.time_complexity,
      space_complexity: problem.space_complexity,
      tags: problem.tags?.join(', ') || '',
      companies: problem.companies?.join(', ') || '',
      is_premium: problem.is_premium,
      is_active: problem.is_active
    });
    setIsDialogOpen(true);
  };

  const handleDelete = async (problemId) => {
    if (window.confirm("Are you sure you want to delete this DSA problem?")) {
      try {
        await adminApi.deleteDSAProblem(problemId);
        toast({
          title: "Success",
          description: "DSA problem deleted successfully"
        });
        fetchDSAProblems();
      } catch (error) {
        console.error("Error deleting DSA problem:", error);
        toast({
          title: "Error",
          description: "Failed to delete DSA problem",
          variant: "destructive"
        });
      }
    }
  };

  const resetForm = () => {
    setFormData({
      title: "",
      description: "",
      difficulty: "",
      topic: "",
      problem_statement: "",
      input_format: "",
      output_format: "",
      constraints: "",
      examples: "",
      solution_approach: "",
      code_solution: "",
      time_complexity: "",
      space_complexity: "",
      tags: "",
      companies: "",
      is_premium: false,
      is_active: true
    });
    setSelectedProblem(null);
  };

  const filteredProblems = dsaProblems.filter(problem =>
    problem.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    problem.topic?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    problem.difficulty?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">DSA Corner Management</h1>
        </div>
        <div className="text-center py-8">Loading DSA problems...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">DSA Corner Management</h1>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={resetForm}>
              <Plus className="w-4 h-4 mr-2" />
              Add New DSA Problem
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>
                {selectedProblem ? "Edit DSA Problem" : "Add New DSA Problem"}
              </DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* AI Agent Section */}
              <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-4 rounded-lg border border-indigo-200">
                <div className="flex items-center space-x-2 mb-3">
                  <div className="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">AI</span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">AI DSA Problem Generator</h3>
                </div>
                <div className="space-y-3">
                  <div>
                    <Label htmlFor="ai-prompt">Describe the DSA problem you want to create</Label>
                    <Textarea
                      id="ai-prompt"
                      placeholder="e.g., Generate a medium difficulty array problem involving two pointers, create a tree traversal problem for interviews"
                      rows={2}
                      className="resize-none"
                    />
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                    <div>
                      <Label htmlFor="ai-difficulty">Difficulty</Label>
                      <Input
                        id="ai-difficulty"
                        placeholder="e.g., Easy, Medium, Hard"
                        className="text-sm"
                      />
                    </div>
                    <div>
                      <Label htmlFor="ai-topic">Topic</Label>
                      <Input
                        id="ai-topic"
                        placeholder="e.g., Arrays, Trees, Dynamic Programming"
                        className="text-sm"
                      />
                    </div>
                    <div>
                      <Label htmlFor="ai-companies">Companies (optional)</Label>
                      <Input
                        id="ai-companies"
                        placeholder="Google, Amazon, etc."
                        className="text-sm"
                      />
                    </div>
                  </div>
                  <Button 
                    type="button" 
                    className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700"
                    onClick={async () => {
                      const promptElement = document.getElementById('ai-prompt');
                      const companiesElement = document.getElementById('ai-companies');
                      
                      const basePrompt = promptElement?.value || 'Generate a coding interview DSA problem';
                      const companies = companiesElement?.value || '';
                      const difficultyElement = document.getElementById('ai-difficulty');
                      const topicElement = document.getElementById('ai-topic');
                      const difficulty = difficultyElement?.value || '';
                      const topic = topicElement?.value || '';
                      
                      let fullPrompt = basePrompt;
                      if (difficulty) fullPrompt += ` with ${difficulty} difficulty`;
                      if (topic) fullPrompt += ` focused on ${topic}`;
                      if (companies) fullPrompt += ` asked by companies like ${companies}`;
                      
                      try {
                        const response = await apiClient.post(`/ai/generate-dsa-problem?prompt=${encodeURIComponent(fullPrompt)}`);
                        const data = response.data;
                        
                        if (!data.content) {
                          throw new Error('No content received from AI');
                        }
                        
                        const content = data.content;
                        setFormData({
                          ...formData,
                          title: content.title || formData.title,
                          description: content.description || formData.description,
                          difficulty: content.difficulty || difficulty || formData.difficulty,
                          topic: content.topic || topic || formData.topic,
                          problem_statement: content.problem_statement || formData.problem_statement,
                          input_format: content.input_format || formData.input_format,
                          output_format: content.output_format || formData.output_format,
                          examples: content.examples?.join('\n') || formData.examples,
                          constraints: content.constraints?.join('\n') || formData.constraints,
                          solution_approach: content.solution_approach || formData.solution_approach,
                          code_solution: content.code_solution || formData.code_solution,
                          time_complexity: content.time_complexity || formData.time_complexity,
                          space_complexity: content.space_complexity || formData.space_complexity,
                          tags: content.tags?.join(', ') || formData.tags,
                          companies: content.companies?.join(', ') || companies || formData.companies
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
                    🤖 Generate DSA Problem with AI
                  </Button>
                </div>
              </div>
              
              {/* DSA Problem Form Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="title">Problem Title</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="difficulty">Difficulty</Label>
                  <Select value={formData.difficulty} onValueChange={(value) => setFormData({...formData, difficulty: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select difficulty" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Easy">Easy</SelectItem>
                      <SelectItem value="Medium">Medium</SelectItem>
                      <SelectItem value="Hard">Hard</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="topic">Topic</Label>
                  <Select value={formData.topic} onValueChange={(value) => setFormData({...formData, topic: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select topic" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Arrays">Arrays</SelectItem>
                      <SelectItem value="Strings">Strings</SelectItem>
                      <SelectItem value="Linked Lists">Linked Lists</SelectItem>
                      <SelectItem value="Trees">Trees</SelectItem>
                      <SelectItem value="Graphs">Graphs</SelectItem>
                      <SelectItem value="Dynamic Programming">Dynamic Programming</SelectItem>
                      <SelectItem value="Sorting">Sorting</SelectItem>
                      <SelectItem value="Searching">Searching</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="companies">Companies (comma separated)</Label>
                  <Input
                    id="companies"
                    value={formData.companies}
                    onChange={(e) => setFormData({...formData, companies: e.target.value})}
                    placeholder="Google, Amazon, Microsoft"
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
                />
              </div>

              <div>
                <Label htmlFor="problem_statement">Problem Statement</Label>
                <Textarea
                  id="problem_statement"
                  value={formData.problem_statement}
                  onChange={(e) => setFormData({...formData, problem_statement: e.target.value})}
                  rows={4}
                  required
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="input_format">Input Format</Label>
                  <Textarea
                    id="input_format"
                    value={formData.input_format}
                    onChange={(e) => setFormData({...formData, input_format: e.target.value})}
                    rows={3}
                  />
                </div>
                <div>
                  <Label htmlFor="output_format">Output Format</Label>
                  <Textarea
                    id="output_format"
                    value={formData.output_format}
                    onChange={(e) => setFormData({...formData, output_format: e.target.value})}
                    rows={3}
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="examples">Examples (one per line)</Label>
                <Textarea
                  id="examples"
                  value={formData.examples}
                  onChange={(e) => setFormData({...formData, examples: e.target.value})}
                  rows={4}
                />
              </div>

              <div>
                <Label htmlFor="constraints">Constraints (one per line)</Label>
                <Textarea
                  id="constraints"
                  value={formData.constraints}
                  onChange={(e) => setFormData({...formData, constraints: e.target.value})}
                  rows={3}
                />
              </div>

              <div>
                <Label htmlFor="solution_approach">Solution Approach</Label>
                <Textarea
                  id="solution_approach"
                  value={formData.solution_approach}
                  onChange={(e) => setFormData({...formData, solution_approach: e.target.value})}
                  rows={4}
                />
              </div>

              <div>
                <Label htmlFor="code_solution">Code Solution</Label>
                <Textarea
                  id="code_solution"
                  value={formData.code_solution}
                  onChange={(e) => setFormData({...formData, code_solution: e.target.value})}
                  rows={6}
                  className="font-mono"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="time_complexity">Time Complexity</Label>
                  <Input
                    id="time_complexity"
                    value={formData.time_complexity}
                    onChange={(e) => setFormData({...formData, time_complexity: e.target.value})}
                    placeholder="O(n)"
                  />
                </div>
                <div>
                  <Label htmlFor="space_complexity">Space Complexity</Label>
                  <Input
                    id="space_complexity"
                    value={formData.space_complexity}
                    onChange={(e) => setFormData({...formData, space_complexity: e.target.value})}
                    placeholder="O(1)"
                  />
                </div>
                <div>
                  <Label htmlFor="tags">Tags (comma separated)</Label>
                  <Input
                    id="tags"
                    value={formData.tags}
                    onChange={(e) => setFormData({...formData, tags: e.target.value})}
                    placeholder="array, two-pointer"
                  />
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.is_premium}
                    onChange={(e) => setFormData({...formData, is_premium: e.target.checked})}
                  />
                  <span>Premium Problem</span>
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
                      {selectedProblem ? "Updating..." : "Creating..."}
                    </>
                  ) : (
                    selectedProblem ? "Update Problem" : "Create Problem"
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
            placeholder="Search problems by title, topic, or difficulty..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="grid gap-6">
        {filteredProblems.length === 0 ? (
          <Card>
            <CardContent className="text-center py-8">
              <p className="text-gray-500">No DSA problems found</p>
            </CardContent>
          </Card>
        ) : (
          filteredProblems.map((problem) => (
            <Card key={problem.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="space-y-2 flex-1">
                    <CardTitle className="text-xl">{problem.title}</CardTitle>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <div className="flex items-center space-x-1">
                        <Code className="w-4 h-4" />
                        <span>{problem.topic}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Target className="w-4 h-4" />
                        <span>{problem.time_complexity} / {problem.space_complexity}</span>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge className={getDifficultyColor(problem.difficulty)}>
                        {problem.difficulty}
                      </Badge>
                      {problem.is_premium && (
                        <Badge variant="destructive">Premium</Badge>
                      )}
                      <Badge variant={problem.is_active ? 'default' : 'secondary'}>
                        {problem.is_active ? 'Active' : 'Inactive'}
                      </Badge>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEdit(problem)}
                    >
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(problem.id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-4">{problem.description}</p>
                {problem.companies && problem.companies.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="font-semibold text-sm">Asked by:</h4>
                    <div className="flex flex-wrap gap-2">
                      {problem.companies.map((company, index) => (
                        <Badge key={index} variant="outline">{company}</Badge>
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

export default DSAManagement;
