import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { publicApi } from '../services/api';
import { Button } from './ui/button';
import { Input } from './ui/input';
import Header from './Header';
import Footer from './Footer';
import { useAuth } from '../contexts/AuthContext';

const Articles = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [interactions, setInteractions] = useState({}); // Store like/save status for each article

  useEffect(() => {
    fetchArticles();
  }, [searchTerm, categoryFilter]);

  useEffect(() => {
    if (user && articles.length > 0) {
      fetchInteractionStatus();
    }
  }, [articles, user]);

  const fetchArticles = async () => {
    try {
      setLoading(true);
      const params = {};
      if (searchTerm) params.search = searchTerm;
      if (categoryFilter) params.category = categoryFilter;
      
      const data = await publicApi.getArticles(params);
      setArticles(data);
    } catch (err) {
      setError('Failed to fetch articles');
      console.error('Error fetching articles:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchInteractionStatus = async () => {
    if (!user) return;

    try {
      const token = localStorage.getItem('token');
      const interactionData = {};
      
      for (const article of articles) {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/interactions/article/${article.id}/status`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          interactionData[article.id] = data;
        }
      }
      
      setInteractions(interactionData);
    } catch (error) {
      console.error('Error fetching interaction status:', error);
    }
  };

  const handleInteraction = async (articleId, interactionType) => {
    if (!user) {
      navigate('/login');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/interactions/article/${articleId}/${interactionType}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        
        // Update local interaction state
        setInteractions(prev => ({
          ...prev,
          [articleId]: {
            ...prev[articleId],
            [interactionType === 'like' ? 'liked' : 'saved']: interactionType === 'like' ? data.liked : data.saved,
            ...(interactionType === 'like' && { total_likes: data.total_likes })
          }
        }));

        if (interactionType === 'save') {
          alert(data.message);
        }
      }
    } catch (error) {
      console.error(`Error ${interactionType}:`, error);
    }
  };

  const handleShare = async (articleId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/interactions/article/${articleId}/share`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        
        // Copy to clipboard
        navigator.clipboard.writeText(data.share_url);
        alert('Article link copied to clipboard!');
      }
    } catch (error) {
      console.error('Error sharing:', error);
    }
  };

  const handleDownload = async (articleId, articleTitle) => {
    if (!user) {
      navigate('/login');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/interactions/article/${articleId}/download`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        alert(`${data.message}. Download feature will be available soon!`);
        // In a real implementation, you would trigger the actual download here
        // window.open(data.download_url, '_blank');
      }
    } catch (error) {
      console.error('Error downloading:', error);
    }
  };

  const handleApplyNow = async (articleId) => {
    if (!user) {
      navigate('/login');
      return;
    }

    // This would typically be for job-related articles
    alert('Apply Now functionality - would redirect to job application form');
  };

  const handleViewCompanyProfile = (companyId) => {
    navigate(`/companies/${companyId}`);
  };

  const handleReadMore = (article) => {
    navigate(`/articles/${article.id}`);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getReadingTime = (content) => {
    const wordsPerMinute = 200;
    const words = content ? content.split(' ').length : 0;
    const minutes = Math.ceil(words / wordsPerMinute);
    return `${minutes} min read`;
  };

  const categories = [
    'Career Tips', 'Interview Prep', 'Skill Development', 'Industry News', 
    'Technology', 'Job Search', 'Resume Tips', 'Salary Negotiation'
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">📖 Articles</h1>
          <p className="text-gray-600">Expert insights and career guidance to boost your professional journey</p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              placeholder="Search articles..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full"
            />
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Categories</option>
              {categories.map((category) => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Articles Grid */}
        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading articles...</p>
          </div>
        ) : error ? (
          <div className="text-center py-8">
            <p className="text-red-600">{error}</p>
          </div>
        ) : articles.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-600">No articles found matching your criteria</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article) => (
              <div key={article.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden border">
                {article.featured_image && (
                  <img 
                    src={article.featured_image} 
                    alt={article.title}
                    className="w-full h-48 object-cover"
                  />
                )}
                
                <div className="p-6">
                  <div className="mb-3">
                    <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">
                      {article.category}
                    </span>
                  </div>
                  
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                    {article.title}
                  </h3>
                  
                  {article.summary && (
                    <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                      {article.summary}
                    </p>
                  )}

                  <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                    <span>{article.author}</span>
                    <span>{getReadingTime(article.content)}</span>
                  </div>

                  {article.tags && article.tags.length > 0 && (
                    <div className="mb-4">
                      <div className="flex flex-wrap gap-1">
                        {article.tags.slice(0, 3).map((tag, index) => (
                          <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                            #{tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="flex items-center justify-between mb-4">
                    <span className="text-xs text-gray-500">
                      {formatDate(article.created_at)} • {article.views} views
                    </span>
                    <div className="flex items-center space-x-2">
                      {interactions[article.id] && (
                        <span className="text-xs text-gray-500">
                          {interactions[article.id].total_likes || 0} likes
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleInteraction(article.id, 'like')}
                          className={`${
                            interactions[article.id]?.liked 
                              ? 'bg-red-50 text-red-600 border-red-200' 
                              : 'hover:bg-gray-50'
                          }`}
                        >
                          {interactions[article.id]?.liked ? '❤️' : '🤍'} Like
                        </Button>
                        
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleInteraction(article.id, 'save')}
                          className={`${
                            interactions[article.id]?.saved 
                              ? 'bg-blue-50 text-blue-600 border-blue-200' 
                              : 'hover:bg-gray-50'
                          }`}
                        >
                          {interactions[article.id]?.saved ? '📌' : '🔖'} Save
                        </Button>
                        
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleShare(article.id)}
                          className="hover:bg-gray-50"
                        >
                          📤 Share
                        </Button>
                      </div>
                      
                      <Button 
                        size="sm" 
                        className="bg-purple-600 hover:bg-purple-700"
                        onClick={() => handleReadMore(article)}
                      >
                        Read More
                      </Button>
                    </div>

                    {/* Additional Action Buttons */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleDownload(article.id, article.title)}
                          className="hover:bg-gray-50 text-green-600 border-green-200"
                        >
                          📄 Download
                        </Button>
                        
                        {article.category === 'Career Tips' && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleApplyNow(article.id)}
                            className="hover:bg-gray-50 text-blue-600 border-blue-200"
                          >
                            🚀 Apply Now
                          </Button>
                        )}
                        
                        {article.company_id && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleViewCompanyProfile(article.company_id)}
                            className="hover:bg-gray-50 text-orange-600 border-orange-200"
                          >
                            🏢 Company
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default Articles;