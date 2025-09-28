import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from './ui/button';
import { Input } from './ui/input';
import Header from './Header';
import { useAuth } from '../contexts/AuthContext';
import { publicApi } from '../services/api';

const DSAProblemDetail = () => {
  const { problemId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [problem, setProblem] = useState(null);
  const [userProgress, setUserProgress] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('problem');
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [hints, setHints] = useState([]);
  const [solution, setSolution] = useState(null);
  const [discussions, setDiscussions] = useState([]);
  const [newDiscussion, setNewDiscussion] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [testResults, setTestResults] = useState(null);
  const [showHints, setShowHints] = useState([]);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchProblem();
  }, [problemId, user]);

  const fetchProblem = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/dsa/problems/${problemId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setProblem(data.problem);
        setUserProgress(data.user_progress);
        setSubmissions(data.recent_submissions || []);
      }
    } catch (error) {
      console.error('Error fetching problem:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchHints = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/dsa/problems/${problemId}/hints`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setHints(data.hints || []);
      }
    } catch (error) {
      console.error('Error fetching hints:', error);
    }
  };

  const fetchSolution = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/dsa/problems/${problemId}/solution`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setSolution(data);
      } else if (response.status === 403) {
        alert('Please attempt the problem first to view the solution');
      }
    } catch (error) {
      console.error('Error fetching solution:', error);
    }
  };

  const fetchDiscussions = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/dsa/problems/${problemId}/discussions`);
      
      if (response.ok) {
        const data = await response.json();
        setDiscussions(data.discussions || []);
      }
    } catch (error) {
      console.error('Error fetching discussions:', error);
    }
  };

  const submitSolution = async () => {
    if (!code.trim()) {
      alert('Please write some code before submitting');
      return;
    }

    setIsSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/dsa/problems/${problemId}/submit`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          code,
          language
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        alert(`Submission ${data.status}! ${data.test_cases_passed}/${data.total_test_cases} test cases passed.`);
        fetchProblem(); // Refresh to get updated progress
      }
    } catch (error) {
      console.error('Error submitting solution:', error);
      alert('Failed to submit solution');
    } finally {
      setIsSubmitting(false);
    }
  };

  const postDiscussion = async () => {
    if (!newDiscussion.trim()) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/dsa/problems/${problemId}/discussions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          content: newDiscussion
        })
      });
      
      if (response.ok) {
        setNewDiscussion('');
        fetchDiscussions();
      }
    } catch (error) {
      console.error('Error posting discussion:', error);
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'hard':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading problem...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">
            <p className="text-gray-600">Problem not found</p>
            <Button onClick={() => navigate('/dsa-corner')} className="mt-4">
              Back to DSA Corner
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="mb-6">
          <Button 
            variant="outline" 
            onClick={() => navigate('/dsa-corner')}
            className="mb-4"
          >
            ← Back to DSA Corner
          </Button>
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{problem.title}</h1>
              <div className="flex items-center space-x-4 mt-2">
                <span className={`px-2 py-1 text-xs rounded-full border ${getDifficultyColor(problem.difficulty)}`}>
                  {problem.difficulty?.charAt(0).toUpperCase() + problem.difficulty?.slice(1)}
                </span>
                {userProgress && (
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    userProgress.status === 'solved' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-orange-100 text-orange-800'
                  }`}>
                    {userProgress.status === 'solved' ? 'Solved' : 'In Progress'}
                  </span>
                )}
              </div>
            </div>
            
            <div className="text-right text-sm text-gray-600">
              <div>Attempts: {problem.attempts || 0}</div>
              <div>Success Rate: {problem.success_rate || 0}%</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Panel - Problem Description & Tabs */}
          <div className="bg-white rounded-lg shadow-sm border">
            {/* Tab Navigation */}
            <div className="border-b">
              <nav className="flex space-x-8 px-6">
                {['problem', 'hints', 'solution', 'discussions'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => {
                      setActiveTab(tab);
                      if (tab === 'hints' && hints.length === 0) fetchHints();
                      if (tab === 'solution' && !solution) fetchSolution();
                      if (tab === 'discussions' && discussions.length === 0) fetchDiscussions();
                    }}
                    className={`py-4 px-1 border-b-2 font-medium text-sm capitalize ${
                      activeTab === tab
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </nav>
            </div>

            {/* Tab Content */}
            <div className="p-6">
              {activeTab === 'problem' && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold mb-3">Description</h3>
                    <div className="prose max-w-none text-gray-700">
                      {problem.description}
                    </div>
                  </div>

                  {problem.examples && problem.examples.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold mb-3">Examples</h3>
                      {problem.examples.map((example, index) => (
                        <div key={index} className="mb-4 p-4 bg-gray-50 rounded-lg">
                          <div className="font-medium text-sm text-gray-600 mb-2">Example {index + 1}:</div>
                          <div className="space-y-2">
                            <div><strong>Input:</strong> <code className="bg-gray-200 px-1 rounded">{example.input}</code></div>
                            <div><strong>Output:</strong> <code className="bg-gray-200 px-1 rounded">{example.output}</code></div>
                            {example.explanation && (
                              <div><strong>Explanation:</strong> {example.explanation}</div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {problem.constraints && problem.constraints.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold mb-3">Constraints</h3>
                      <ul className="list-disc list-inside space-y-1 text-gray-700">
                        {problem.constraints.map((constraint, index) => (
                          <li key={index}>{constraint}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {problem.companies && problem.companies.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold mb-3">Asked in Companies</h3>
                      <div className="flex flex-wrap gap-2">
                        {problem.companies.map((company, index) => (
                          <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                            {company}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'hints' && (
                <div>
                  <h3 className="text-lg font-semibold mb-3">Hints</h3>
                  {hints.length > 0 ? (
                    <div className="space-y-3">
                      {hints.map((hint, index) => (
                        <div key={index} className="p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                          <div className="font-medium text-yellow-800 mb-1">Hint {index + 1}</div>
                          <div className="text-yellow-700">{hint}</div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500">No hints available for this problem.</p>
                  )}
                </div>
              )}

              {activeTab === 'solution' && (
                <div>
                  <h3 className="text-lg font-semibold mb-3">Solution</h3>
                  {solution ? (
                    <div className="space-y-4">
                      {solution.solution_approach && (
                        <div>
                          <h4 className="font-medium mb-2">Approach</h4>
                          <div className="prose max-w-none text-gray-700">
                            {solution.solution_approach}
                          </div>
                        </div>
                      )}
                      
                      <div className="grid grid-cols-2 gap-4">
                        <div className="p-3 bg-green-50 rounded-lg">
                          <div className="font-medium text-green-800">Time Complexity</div>
                          <div className="text-green-700">{solution.time_complexity || 'N/A'}</div>
                        </div>
                        <div className="p-3 bg-blue-50 rounded-lg">
                          <div className="font-medium text-blue-800">Space Complexity</div>
                          <div className="text-blue-700">{solution.space_complexity || 'N/A'}</div>
                        </div>
                      </div>

                      {solution.user_best_solution && (
                        <div>
                          <h4 className="font-medium mb-2">Your Best Solution</h4>
                          <pre className="bg-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                            <code>{solution.user_best_solution}</code>
                          </pre>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-gray-500">Solution not available. Try the problem first!</p>
                  )}
                </div>
              )}

              {activeTab === 'discussions' && (
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold">Discussions</h3>
                  
                  {/* New Discussion Form */}
                  <div className="border rounded-lg p-4">
                    <textarea
                      value={newDiscussion}
                      onChange={(e) => setNewDiscussion(e.target.value)}
                      placeholder="Share your thoughts, ask questions, or help others..."
                      className="w-full p-3 border rounded-lg resize-none"
                      rows="3"
                    />
                    <div className="flex justify-end mt-2">
                      <Button onClick={postDiscussion} size="sm">
                        Post Discussion
                      </Button>
                    </div>
                  </div>

                  {/* Discussions List */}
                  <div className="space-y-4">
                    {discussions.map((discussion) => (
                      <div key={discussion.id} className="border rounded-lg p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-medium text-gray-900">{discussion.user_name}</span>
                          <span className="text-sm text-gray-500">
                            {new Date(discussion.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        <div className="text-gray-700 mb-2">{discussion.content}</div>
                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <button className="hover:text-blue-600">👍 {discussion.likes}</button>
                          <button className="hover:text-blue-600">Reply</button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right Panel - Code Editor */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-4 border-b flex items-center justify-between">
              <h3 className="font-semibold">Code Editor</h3>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="px-3 py-1 border rounded-md text-sm"
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
              </select>
            </div>
            
            <div className="p-4">
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Write your solution here..."
                className="w-full h-96 p-4 border rounded-lg font-mono text-sm resize-none"
                style={{ fontFamily: 'Monaco, Menlo, "Ubuntu Mono", monospace' }}
              />
              
              <div className="flex justify-between items-center mt-4">
                <div className="text-sm text-gray-600">
                  {userProgress && (
                    <span>Attempts: {userProgress.attempts} • Status: {userProgress.status}</span>
                  )}
                </div>
                <Button 
                  onClick={submitSolution} 
                  disabled={isSubmitting}
                  className="bg-green-600 hover:bg-green-700"
                >
                  {isSubmitting ? 'Submitting...' : 'Submit Solution'}
                </Button>
              </div>
            </div>

            {/* Recent Submissions */}
            {submissions.length > 0 && (
              <div className="border-t p-4">
                <h4 className="font-medium mb-3">Recent Submissions</h4>
                <div className="space-y-2">
                  {submissions.slice(0, 3).map((submission) => (
                    <div key={submission.id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                      <div className="flex items-center space-x-3">
                        <span className={`w-2 h-2 rounded-full ${
                          submission.status === 'accepted' ? 'bg-green-500' : 'bg-red-500'
                        }`}></span>
                        <span className="text-sm text-gray-600">
                          {new Date(submission.submitted_at).toLocaleString()}
                        </span>
                        <span className="text-sm font-medium">{submission.language}</span>
                      </div>
                      <span className={`text-sm ${
                        submission.status === 'accepted' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {submission.test_cases_passed}/{submission.total_test_cases}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DSAProblemDetail;