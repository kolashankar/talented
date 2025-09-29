import React, { useState, useEffect } from "react";
import { Plus, Search, Edit, Trash2, FileText, Calendar, User, Eye } from "lucide-react";
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

const ArticleManagement = () => {
  const [articles, setArticles] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const { toast } = useToast();

  const [formData, setFormData] = useState({
    title: "",
    slug: "",
    content: "",
    excerpt: "",
    author: "",
    category: "",
    tags: "",
    featured_image: "",
    is_published: false,
    is_featured: false
  });

  useEffect(() => {
    fetchArticles();
  }, []);

  const fetchArticles = async () => {
    try {
      setLoading(true);
      const response = await adminApi.getArticles();
      setArticles(response);
    } catch (error) {
      console.error("Error fetching articles:", error);
      toast({
        title: "Error",
        description: "Failed to fetch articles",
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
      slug: selectedArticle ? formData.slug : generateSlug(title)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Validate required fields
      if (!formData.title?.trim()) {
        throw new Error('Article title is required');
      }
      if (!formData.content?.trim()) {
        throw new Error('Article content is required');
      }
      if (!formData.author?.trim()) {
        throw new Error('Author is required');
      }

      const articleData = {
        ...formData,
        tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
      };

      if (selectedArticle) {
        await adminApi.updateArticle(selectedArticle.id, articleData);
        toast({
          title: "Success!",
          description: "Article updated successfully and saved to database"
        });
      } else {
        await adminApi.createArticle(articleData);
        toast({
          title: "Success!",
          description: "Article created successfully and saved to database"
        });
      }
      
      setIsDialogOpen(false);
      resetForm();
      await fetchArticles(); // Refresh the list
    } catch (error) {
      console.error("Error saving article:", error);
      
      let errorMessage = "Failed to save article. Please try again.";
      
      if (error.response?.status === 401) {
        errorMessage = "Authentication failed. Please log in again.";
      } else if (error.response?.status === 400) {
        errorMessage = error.response?.data?.detail || "Invalid article data. Please check all fields.";
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

  const handleEdit = (article) => {
    setSelectedArticle(article);
    setFormData({
      title: article.title,
      slug: article.slug,
      content: article.content,
      excerpt: article.excerpt || '',
      author: article.author,
      category: article.category,
      tags: article.tags?.join(', ') || '',
      featured_image: article.featured_image || '',
      is_published: article.is_published,
      is_featured: article.is_featured
    });
    setIsDialogOpen(true);
  };

  const handleDelete = async (articleId) => {
    if (window.confirm("Are you sure you want to delete this article?")) {
      try {
        await adminApi.deleteArticle(articleId);
        toast({
          title: "Success",
          description: "Article deleted successfully"
        });
        fetchArticles();
      } catch (error) {
        console.error("Error deleting article:", error);
        toast({
          title: "Error",
          description: "Failed to delete article",
          variant: "destructive"
        });
      }
    }
  };

  const resetForm = () => {
    setFormData({
      title: "",
      slug: "",
      content: "",
      excerpt: "",
      author: "",
      category: "",
      tags: "",
      featured_image: "",
      is_published: false,
      is_featured: false
    });
    setSelectedArticle(null);
  };

  const filteredArticles = articles.filter(article =>
    article.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    article.author?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    article.category?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Article Management</h1>
        </div>
        <div className="text-center py-8">Loading articles...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Article Management</h1>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={resetForm}>
              <Plus className="w-4 h-4 mr-2" />
              Add New Article
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>
                {selectedArticle ? "Edit Article" : "Add New Article"}
              </DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* AI Agent Section */}
              <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg border border-purple-200">
                <div className="flex items-center space-x-2 mb-3">
                  <div className="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">AI</span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">AI Article Generator</h3>
                </div>
                <div className="space-y-3">
                  <div>
                    <Label htmlFor="ai-prompt">Describe the article you want to create</Label>
                    <Textarea
                      id="ai-prompt"
                      placeholder="e.g., How to prepare for technical interviews in 2024, best practices for remote work, career transition from marketing to tech"
                      rows={2}
                      className="resize-none"
                    />
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                    <div>
                      <Label htmlFor="ai-author">Author (optional)</Label>
                      <Input
                        id="ai-author"
                        placeholder="Author name"
                        className="text-sm"
                      />
                    </div>
                    <div>
                      <Label htmlFor="ai-category">Category</Label>
                      <Input
                        id="ai-category"
                        placeholder="e.g., career-advice, technical, tutorials"
                        className="text-sm"
                      />
                    </div>
                    <div>
                      <Label htmlFor="ai-length">Article Length</Label>
                      <Input
                        id="ai-length"
                        placeholder="e.g., short, medium, long"
                        className="text-sm"
                      />
                    </div>
                  </div>
                  <Button 
                    type="button" 
                    className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
                    onClick={async () => {
                      const promptElement = document.getElementById('ai-prompt');
                      const authorElement = document.getElementById('ai-author');
                      
                      const basePrompt = promptElement?.value || 'Generate a professional article about career development';
                      const author = authorElement?.value || '';
                      const categoryElement = document.getElementById('ai-category');
                      const lengthElement = document.getElementById('ai-length');
                      const category = categoryElement?.value || '';
                      const length = lengthElement?.value || '';
                      
                      let fullPrompt = basePrompt;
                      if (category) fullPrompt += ` in the ${category} category`;
                      if (length) fullPrompt += ` with ${length} length`;
                      if (author) fullPrompt += ` written by ${author}`;
                      
                      try {
                        const response = await apiClient.post(`/ai/generate-article?prompt=${encodeURIComponent(fullPrompt)}`);
                        const data = response.data;
                        
                        if (!data.content) {
                          throw new Error('No content received from AI');
                        }
                        
                        const content = data.content;
                        setFormData({
                          ...formData,
                          title: content.title || formData.title,
                          content: content.content || formData.content,
                          excerpt: content.excerpt || formData.excerpt,
                          author: content.author || author || formData.author,
                          category: content.category || category || formData.category,
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
                    🤖 Generate Article with AI
                  </Button>
                </div>
              </div>
              
              {/* Article Form Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="title">Article Title</Label>
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
                    placeholder="article-url-slug"
                  />
                </div>
                <div>
                  <Label htmlFor="author">Author</Label>
                  <Input
                    id="author"
                    value={formData.author}
                    onChange={(e) => setFormData({...formData, author: e.target.value})}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="category">Category</Label>
                  <Select value={formData.category} onValueChange={(value) => setFormData({...formData, category: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="career-advice">Career Advice</SelectItem>
                      <SelectItem value="technical">Technical</SelectItem>
                      <SelectItem value="interview-tips">Interview Tips</SelectItem>
                      <SelectItem value="industry-news">Industry News</SelectItem>
                      <SelectItem value="tutorials">Tutorials</SelectItem>
                      <SelectItem value="company-culture">Company Culture</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="md:col-span-2">
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
                <Label htmlFor="excerpt">Excerpt</Label>
                <Textarea
                  id="excerpt"
                  value={formData.excerpt}
                  onChange={(e) => setFormData({...formData, excerpt: e.target.value})}
                  rows={3}
                  placeholder="Brief description of the article..."
                />
              </div>
              
              <div>
                <Label htmlFor="content">Article Content</Label>
                <Textarea
                  id="content"
                  value={formData.content}
                  onChange={(e) => setFormData({...formData, content: e.target.value})}
                  rows={8}
                  required
                  placeholder="Write your article content here..."
                />
              </div>
              
              <div>
                <Label htmlFor="tags">Tags (comma separated)</Label>
                <Input
                  id="tags"
                  value={formData.tags}
                  onChange={(e) => setFormData({...formData, tags: e.target.value})}
                  placeholder="career, programming, tips, advice"
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
                  <span>Featured Article</span>
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
                      {selectedArticle ? "Updating..." : "Creating..."}
                    </>
                  ) : (
                    selectedArticle ? "Update Article" : "Create Article"
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
            placeholder="Search articles by title, author, or category..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="grid gap-6">
        {filteredArticles.length === 0 ? (
          <Card>
            <CardContent className="text-center py-8">
              <p className="text-gray-500">No articles found</p>
            </CardContent>
          </Card>
        ) : (
          filteredArticles.map((article) => (
            <Card key={article.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="space-y-2 flex-1">
                    <CardTitle className="text-xl">{article.title}</CardTitle>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <div className="flex items-center space-x-1">
                        <User className="w-4 h-4" />
                        <span>{article.author}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <FileText className="w-4 h-4" />
                        <span>{article.category}</span>
                      </div>
                      {article.created_at && (
                        <div className="flex items-center space-x-1">
                          <Calendar className="w-4 h-4" />
                          <span>{formatDate(article.created_at)}</span>
                        </div>
                      )}
                      {article.views && (
                        <div className="flex items-center space-x-1">
                          <Eye className="w-4 h-4" />
                          <span>{article.views} views</span>
                        </div>
                      )}
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge variant={article.is_published ? 'default' : 'secondary'}>
                        {article.is_published ? 'Published' : 'Draft'}
                      </Badge>
                      {article.is_featured && (
                        <Badge variant="destructive">Featured</Badge>
                      )}
                      <Badge variant="outline">{article.category}</Badge>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEdit(article)}
                    >
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(article.id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {article.excerpt && (
                  <p className="text-gray-600 mb-4">{article.excerpt}</p>
                )}
                {article.featured_image && (
                  <div className="mb-4">
                    <img 
                      src={article.featured_image} 
                      alt={article.title}
                      className="w-full h-48 object-cover rounded-lg"
                      onError={(e) => {
                        e.target.style.display = 'none';
                      }}
                    />
                  </div>
                )}
                {article.tags && article.tags.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="font-semibold text-sm">Tags:</h4>
                    <div className="flex flex-wrap gap-2">
                      {article.tags.map((tag, index) => (
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

export default ArticleManagement;