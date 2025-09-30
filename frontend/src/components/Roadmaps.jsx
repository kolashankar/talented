import React, { useState, useEffect } from 'react';
import { publicApi } from '../services/api';
import { Button } from './ui/button';
import { Input } from './ui/input';
import Header from './Header';

const Roadmaps = () => {
  const [roadmaps, setRoadmaps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState('');

  useEffect(() => {
    fetchRoadmaps();
  }, [searchTerm, difficultyFilter]);

  const fetchRoadmaps = async () => {
    try {
      setLoading(true);
      const params = {};
      if (searchTerm) params.search = searchTerm;
      if (difficultyFilter) params.difficulty = difficultyFilter;
      
      const data = await publicApi.getRoadmaps(params);
      setRoadmaps(data);
    } catch (err) {
      setError('Failed to fetch roadmaps');
      console.error('Error fetching roadmaps:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'beginner':
        return 'bg-green-100 text-green-800';
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-800';
      case 'advanced':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getEstimatedTime = (phases) => {
    if (!phases || !Array.isArray(phases)) return 'Variable';
    const totalWeeks = phases.reduce((acc, phase) => {
      return acc + (phase.estimated_weeks || 0);
    }, 0);
    
    if (totalWeeks < 4) return `${totalWeeks} weeks`;
    if (totalWeeks < 52) return `${Math.ceil(totalWeeks / 4)} months`;
    return `${Math.ceil(totalWeeks / 52)} years`;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">🗺️ Roadmaps</h1>
          <p className="text-gray-600">Structured learning paths to master new skills and advance your career</p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              placeholder="Search roadmaps..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full"
            />
            <select
              value={difficultyFilter}
              onChange={(e) => setDifficultyFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Difficulty Levels</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
        </div>

        {/* Roadmaps Grid */}
        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading roadmaps...</p>
          </div>
        ) : error ? (
          <div className="text-center py-8">
            <p className="text-red-600">{error}</p>
          </div>
        ) : roadmaps.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-600">No roadmaps found matching your criteria</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {roadmaps.map((roadmap) => (
              <div key={roadmap.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6 border">
                <div className="mb-4">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-lg font-semibold text-gray-900 flex-1">{roadmap.title}</h3>
                    <span className={`px-2 py-1 text-xs rounded-full ${getDifficultyColor(roadmap.difficulty_level)}`}>
                      {roadmap.difficulty_level}
                    </span>
                  </div>
                  
                  {roadmap.description && (
                    <p className="text-gray-600 text-sm line-clamp-3 mb-3">
                      {roadmap.description}
                    </p>
                  )}
                </div>

                <div className="space-y-2 mb-4">
                  <div className="flex items-center text-sm text-gray-600">
                    <span className="mr-1">⏱️</span>
                    Duration: {getEstimatedTime(roadmap.phases)}
                  </div>
                  {roadmap.phases && roadmap.phases.length > 0 && (
                    <div className="flex items-center text-sm text-gray-600">
                      <span className="mr-1">📚</span>
                      {roadmap.phases.length} learning phases
                    </div>
                  )}
                  <div className="flex items-center text-sm text-gray-600">
                    <span className="mr-1">👁️</span>
                    {roadmap.views} views
                  </div>
                </div>

                {roadmap.tags && roadmap.tags.length > 0 && (
                  <div className="mb-4">
                    <div className="flex flex-wrap gap-1">
                      {roadmap.tags.slice(0, 3).map((tag, index) => (
                        <span key={index} className="px-2 py-1 bg-indigo-100 text-indigo-800 text-xs rounded-full">
                          {tag}
                        </span>
                      ))}
                      {roadmap.tags.length > 3 && (
                        <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                          +{roadmap.tags.length - 3} more
                        </span>
                      )}
                    </div>
                  </div>
                )}

                {roadmap.phases && roadmap.phases.length > 0 && (
                  <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Learning Path:</h4>
                    <div className="space-y-1">
                      {roadmap.phases.slice(0, 3).map((phase, index) => (
                        <div key={index} className="flex items-center text-sm text-gray-600">
                          <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full mr-2"></div>
                          <span className="truncate">{phase.title}</span>
                        </div>
                      ))}
                      {roadmap.phases.length > 3 && (
                        <div className="text-xs text-gray-500 pl-3.5">
                          +{roadmap.phases.length - 3} more phases
                        </div>
                      )}
                    </div>
                  </div>
                )}

                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-500">
                    Updated {formatDate(roadmap.updated_at)}
                  </span>
                  <Button size="sm" className="bg-indigo-600 hover:bg-indigo-700">
                    Start Learning
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Roadmaps;