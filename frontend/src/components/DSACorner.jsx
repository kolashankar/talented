import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from './ui/button';
import { Input } from './ui/input';
import Header from './Header';

const DSACorner = () => {
  const navigate = useNavigate();
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [selectedDifficulty, setSelectedDifficulty] = useState('');

  // Mock data for DSA topics and problems (will be replaced with API data later)
  const dsaTopics = [
    {
      id: 1,
      name: 'Arrays',
      description: 'Linear data structure storing elements in contiguous memory',
      problemCount: 45,
      icon: '📊'
    },
    {
      id: 2,
      name: 'Strings',
      description: 'Character sequence manipulation and processing',
      problemCount: 32,
      icon: '📝'
    },
    {
      id: 3,
      name: 'Linked Lists',
      description: 'Dynamic data structure with nodes containing data and pointers',
      problemCount: 28,
      icon: '🔗'
    },
    {
      id: 4,
      name: 'Stacks & Queues',
      description: 'LIFO and FIFO data structures for specific operations',
      problemCount: 24,
      icon: '📚'
    },
    {
      id: 5,
      name: 'Trees',
      description: 'Hierarchical data structure with root, nodes, and leaves',
      problemCount: 38,
      icon: '🌳'
    },
    {
      id: 6,
      name: 'Graphs',
      description: 'Collection of vertices connected by edges',
      problemCount: 31,
      icon: '🕸️'
    },
    {
      id: 7,
      name: 'Dynamic Programming',
      description: 'Optimization technique using overlapping subproblems',
      problemCount: 42,
      icon: '⚡'
    },
    {
      id: 8,
      name: 'Sorting & Searching',
      description: 'Algorithms for organizing and finding data',
      problemCount: 26,
      icon: '🔍'
    }
  ];

  const mockProblems = [
    {
      id: 1,
      title: 'Two Sum',
      difficulty: 'Easy',
      topic: 'Arrays',
      companies: ['Google', 'Apple', 'Microsoft'],
      solved: false
    },
    {
      id: 2,
      title: 'Reverse Linked List',
      difficulty: 'Easy',
      topic: 'Linked Lists',
      companies: ['Amazon', 'Facebook', 'Netflix'],
      solved: true
    },
    {
      id: 3,
      title: 'Binary Tree Inorder Traversal',
      difficulty: 'Medium',
      topic: 'Trees',
      companies: ['Google', 'Microsoft', 'Adobe'],
      solved: false
    }
  ];

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Easy':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'Hard':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const handleProblemAction = (problem) => {
    // Navigate to the detailed problem page
    navigate(`/dsa-corner/problem/${problem.id}`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">⚡ DSA Corner</h1>
          <p className="text-gray-600">Master Data Structures and Algorithms with our curated problem sets</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Topics Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Topics</h2>
              <div className="space-y-2">
                {dsaTopics.map((topic) => (
                  <div
                    key={topic.id}
                    onClick={() => setSelectedTopic(topic)}
                    className={`p-3 rounded-lg cursor-pointer transition-colors ${
                      selectedTopic?.id === topic.id
                        ? 'bg-blue-50 border-blue-200 border'
                        : 'hover:bg-gray-50 border border-transparent'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <span className="text-xl">{topic.icon}</span>
                        <div>
                          <h3 className="font-medium text-gray-900">{topic.name}</h3>
                          <p className="text-xs text-gray-500">{topic.problemCount} problems</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Progress Stats */}
            <div className="bg-white rounded-lg shadow-sm border p-6 mt-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Your Progress</h2>
              <div className="space-y-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">0/266</div>
                  <div className="text-sm text-gray-600">Problems Solved</div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: '0%' }}></div>
                </div>
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div>
                    <div className="text-sm font-medium text-green-600">0</div>
                    <div className="text-xs text-gray-500">Easy</div>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-yellow-600">0</div>
                    <div className="text-xs text-gray-500">Medium</div>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-red-600">0</div>
                    <div className="text-xs text-gray-500">Hard</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Problems Main Content */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border">
              {/* Filter Header */}
              <div className="p-6 border-b">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-gray-900">
                    {selectedTopic ? `${selectedTopic.name} Problems` : 'All Problems'}
                  </h2>
                  <select
                    value={selectedDifficulty}
                    onChange={(e) => setSelectedDifficulty(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">All Difficulties</option>
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>
                <Input
                  placeholder="Search problems..."
                  className="w-full"
                />
              </div>

              {/* Problems List */}
              <div className="p-6">
                {selectedTopic ? (
                  <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className="text-2xl">{selectedTopic.icon}</span>
                      <h3 className="text-lg font-semibold text-gray-900">{selectedTopic.name}</h3>
                    </div>
                    <p className="text-gray-600 text-sm">{selectedTopic.description}</p>
                    <p className="text-blue-600 text-sm mt-2 font-medium">{selectedTopic.problemCount} problems available</p>
                  </div>
                ) : null}

                <div className="space-y-4">
                  {mockProblems.map((problem) => (
                    <div key={problem.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-3">
                          <div className={`w-4 h-4 rounded-full border-2 ${
                            problem.solved ? 'bg-green-500 border-green-500' : 'border-gray-300'
                          }`}>
                            {problem.solved && (
                              <div className="w-full h-full flex items-center justify-center">
                                <span className="text-white text-xs">✓</span>
                              </div>
                            )}
                          </div>
                          <h4 className="font-medium text-gray-900">{problem.title}</h4>
                        </div>
                        <span className={`px-2 py-1 text-xs rounded-full border ${getDifficultyColor(problem.difficulty)}`}>
                          {problem.difficulty}
                        </span>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4 text-sm text-gray-600">
                          <span>Topic: {problem.topic}</span>
                          <span>Companies: {problem.companies.slice(0, 2).join(', ')}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Button 
                            size="sm" 
                            variant={problem.solved ? "outline" : "default"}
                            onClick={() => handleProblemAction(problem)}
                            className={problem.solved ? "bg-green-50 text-green-600 border-green-200" : ""}
                          >
                            {problem.solved ? '📋 Review' : '🚀 Solve'}
                          </Button>
                          {problem.solved && (
                            <span className="text-xs text-green-600 font-medium">✅</span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Coming Soon Message */}
                <div className="text-center py-8 mt-8 border-t">
                  <div className="text-gray-500">
                    <div className="text-4xl mb-4">🚧</div>
                    <h3 className="text-lg font-medium mb-2">DSA Corner Coming Soon!</h3>
                    <p className="text-sm">We're building an amazing DSA practice platform. Stay tuned!</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DSACorner;