import React, { useState, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Alert, AlertDescription } from './ui/alert';
import { Upload, FileText, Star, AlertCircle, CheckCircle, TrendingUp, Brain } from 'lucide-react';

const ResumeReviewer = () => {
  const { user, login } = useContext(AuthContext);
  const [file, setFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [targetRole, setTargetRole] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('upload');

  const handleFileUpload = async () => {
    if (!file) {
      setError('Please select a resume file');
      return;
    }

    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('resume_file', file);
    if (jobDescription) formData.append('job_description', jobDescription);
    if (targetRole) formData.append('target_role', targetRole);

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/resume/upload-analyze`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        setAnalysis(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to analyze resume');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleTextAnalysis = async () => {
    if (!resumeText.trim()) {
      setError('Please enter resume text');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/resume/analyze-text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription || null,
          target_role: targetRole || null
        })
      });

      if (response.ok) {
        const data = await response.json();
        setAnalysis(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to analyze resume');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBg = (score) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
        <div className=\"max-w-md mx-auto\">
          <Card>
            <CardHeader className=\"text-center\">
              <Brain className=\"w-12 h-12 text-blue-600 mx-auto mb-4\" />
              <CardTitle className=\"text-2xl\">Resume Reviewer</CardTitle>
              <p className=\"text-gray-600\">Get AI-powered feedback on your resume</p>
            </CardHeader>
            <CardContent className=\"text-center\">
              <Alert className=\"mb-4\">
                <AlertCircle className=\"w-4 h-4\" />
                <AlertDescription>
                  Please sign in to access the Resume Reviewer feature
                </AlertDescription>
              </Alert>
              <Button onClick={login} className=\"w-full\">
                Sign in with Google
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className=\"min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4\">
      <div className=\"max-w-6xl mx-auto\">
        <div className=\"text-center mb-8\">
          <h1 className=\"text-4xl font-bold text-gray-900 mb-4\">
            AI Resume Reviewer
          </h1>
          <p className=\"text-xl text-gray-600\">
            Get comprehensive feedback and improve your resume's ATS compatibility
          </p>
        </div>

        {!analysis ? (
          <div className=\"grid lg:grid-cols-2 gap-8\">
            <Card>
              <CardHeader>
                <CardTitle className=\"flex items-center gap-2\">
                  <Upload className=\"w-5 h-5\" />
                  Upload Resume
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className=\"space-y-4\">
                  <div className=\"border-2 border-dashed border-gray-300 rounded-lg p-6 text-center\">
                    <input
                      type=\"file\"
                      accept=\".pdf,.doc,.docx,.txt\"
                      onChange={(e) => setFile(e.target.files[0])}
                      className=\"hidden\"
                      id=\"resume-upload\"
                    />
                    <label htmlFor=\"resume-upload\" className=\"cursor-pointer\">
                      <Upload className=\"w-12 h-12 text-gray-400 mx-auto mb-4\" />
                      <p className=\"text-gray-600\">Click to upload your resume</p>
                      <p className=\"text-sm text-gray-400\">PDF, DOC, DOCX, TXT files supported</p>
                    </label>
                  </div>
                  
                  {file && (
                    <div className=\"flex items-center gap-2 p-3 bg-blue-50 rounded-lg\">
                      <FileText className=\"w-4 h-4 text-blue-600\" />
                      <span className=\"text-sm text-blue-800\">{file.name}</span>
                    </div>
                  )}

                  <div className=\"space-y-3\">
                    <Input
                      placeholder=\"Target role (e.g., Software Engineer)\"
                      value={targetRole}
                      onChange={(e) => setTargetRole(e.target.value)}
                    />
                    <Textarea
                      placeholder=\"Job description (optional - for better matching)\"
                      value={jobDescription}
                      onChange={(e) => setJobDescription(e.target.value)}
                      rows={4}
                    />
                  </div>

                  <Button 
                    onClick={handleFileUpload} 
                    disabled={loading || !file}
                    className=\"w-full\"
                  >
                    {loading ? 'Analyzing...' : 'Analyze Resume'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className=\"flex items-center gap-2\">
                  <FileText className=\"w-5 h-5\" />
                  Paste Resume Text
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className=\"space-y-4\">
                  <Textarea
                    placeholder=\"Paste your resume text here...\"
                    value={resumeText}
                    onChange={(e) => setResumeText(e.target.value)}
                    rows={10}
                    className=\"min-h-[200px]\"
                  />

                  <div className=\"space-y-3\">
                    <Input
                      placeholder=\"Target role (e.g., Software Engineer)\"
                      value={targetRole}
                      onChange={(e) => setTargetRole(e.target.value)}
                    />
                    <Textarea
                      placeholder=\"Job description (optional)\"
                      value={jobDescription}
                      onChange={(e) => setJobDescription(e.target.value)}
                      rows={4}
                    />
                  </div>

                  <Button 
                    onClick={handleTextAnalysis} 
                    disabled={loading || !resumeText.trim()}
                    className=\"w-full\"
                  >
                    {loading ? 'Analyzing...' : 'Analyze Text'}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        ) : (
          <div className=\"space-y-6\">
            <div className=\"flex justify-between items-center\">
              <h2 className=\"text-2xl font-bold text-gray-900\">Analysis Results</h2>
              <Button 
                variant=\"outline\" 
                onClick={() => {
                  setAnalysis(null);
                  setFile(null);
                  setResumeText('');
                  setError('');
                }}
              >
                Analyze Another Resume
              </Button>
            </div>

            {/* Score Overview */}
            <div className=\"grid md:grid-cols-4 gap-4\">
              <Card>
                <CardContent className=\"p-4 text-center\">
                  <div className={`text-3xl font-bold ${getScoreColor(analysis.overall_score)}`}>
                    {Math.round(analysis.overall_score)}%
                  </div>
                  <p className=\"text-sm text-gray-600\">Overall Score</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className=\"p-4 text-center\">
                  <div className={`text-3xl font-bold ${getScoreColor(analysis.keyword_match_score)}`}>
                    {Math.round(analysis.keyword_match_score)}%
                  </div>
                  <p className=\"text-sm text-gray-600\">Keyword Match</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className=\"p-4 text-center\">
                  <div className={`text-3xl font-bold ${getScoreColor(analysis.formatting_score)}`}>
                    {Math.round(analysis.formatting_score)}%
                  </div>
                  <p className=\"text-sm text-gray-600\">ATS Format</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className=\"p-4 text-center\">
                  <div className=\"text-3xl font-bold text-blue-600\">
                    {analysis.recommendations.length}
                  </div>
                  <p className=\"text-sm text-gray-600\">Recommendations</p>
                </CardContent>
              </Card>
            </div>

            {/* Detailed Analysis */}
            <div className=\"grid lg:grid-cols-2 gap-6\">
              {/* Strengths */}
              <Card>
                <CardHeader>
                  <CardTitle className=\"flex items-center gap-2 text-green-600\">
                    <CheckCircle className=\"w-5 h-5\" />
                    Strengths
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className=\"space-y-2\">
                    {analysis.strengths.map((strength, index) => (
                      <li key={index} className=\"flex items-start gap-2\">
                        <CheckCircle className=\"w-4 h-4 text-green-500 mt-0.5 flex-shrink-0\" />
                        <span className=\"text-sm\">{strength}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* Weaknesses */}
              <Card>
                <CardHeader>
                  <CardTitle className=\"flex items-center gap-2 text-red-600\">
                    <AlertCircle className=\"w-5 h-5\" />
                    Areas for Improvement
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className=\"space-y-2\">
                    {analysis.weaknesses.map((weakness, index) => (
                      <li key={index} className=\"flex items-start gap-2\">
                        <AlertCircle className=\"w-4 h-4 text-red-500 mt-0.5 flex-shrink-0\" />
                        <span className=\"text-sm\">{weakness}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* Suggestions */}
              <Card className=\"lg:col-span-2\">
                <CardHeader>
                  <CardTitle className=\"flex items-center gap-2 text-blue-600\">
                    <TrendingUp className=\"w-5 h-5\" />
                    Actionable Suggestions
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className=\"grid md:grid-cols-2 gap-4\">
                    {analysis.suggestions.map((suggestion, index) => (
                      <div key={index} className=\"p-3 bg-blue-50 rounded-lg\">
                        <p className=\"text-sm text-blue-800\">{suggestion}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Priority Recommendations */}
              <Card className=\"lg:col-span-2\">
                <CardHeader>
                  <CardTitle className=\"flex items-center gap-2 text-purple-600\">
                    <Star className=\"w-5 h-5\" />
                    Priority Recommendations
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className=\"space-y-3\">
                    {analysis.recommendations.map((rec, index) => (
                      <div key={index} className=\"p-4 border border-purple-200 rounded-lg bg-purple-50\">
                        <div className=\"flex items-center gap-2 mb-1\">
                          <span className=\"bg-purple-600 text-white text-xs px-2 py-1 rounded-full\">
                            {index + 1}
                          </span>
                          <span className=\"font-medium text-purple-800\">Priority Action</span>
                        </div>
                        <p className=\"text-sm text-purple-700\">{rec}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {error && (
          <Alert className=\"mt-4 border-red-200 bg-red-50\">
            <AlertCircle className=\"w-4 h-4 text-red-600\" />
            <AlertDescription className=\"text-red-800\">{error}</AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  );
};

export default ResumeReviewer;