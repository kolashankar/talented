import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Upload, FileText, Globe, Eye, Share, Download, 
  User, Briefcase, Code, GraduationCap, Award,
  AlertCircle, CheckCircle, Palette, Zap
} from 'lucide-react';

const PortfolioBuilder = () => {
  const { user, login } = useContext(AuthContext);
  const [step, setStep] = useState(1);
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [parsedData, setParsedData] = useState(null);
  const [userPrompt, setUserPrompt] = useState('');
  const [generatedPortfolio, setGeneratedPortfolio] = useState(null);
  const [myPortfolios, setMyPortfolios] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('create');

  useEffect(() => {
    if (user) {
      fetchTemplates();
      fetchMyPortfolios();
    }
  }, [user]);

  const fetchTemplates = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/portfolio/templates`);
      if (response.ok) {
        const data = await response.json();
        setTemplates(data);
      }
    } catch (err) {
      console.error('Error fetching templates:', err);
    }
  };

  const fetchMyPortfolios = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/portfolio/my-portfolios`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setMyPortfolios(data);
      }
    } catch (err) {
      console.error('Error fetching portfolios:', err);
    }
  };

  const parseResume = async () => {
    setLoading(true);
    setError('');

    try {
      let response;
      
      if (resumeFile) {
        const formData = new FormData();
        formData.append('resume_file', resumeFile);
        
        response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/resume/upload-parse`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: formData
        });
      } else {
        response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/resume/parse`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({ resume_text: resumeText })
        });
      }

      if (response.ok) {
        const data = await response.json();
        setParsedData(data.parsed_data);
        setStep(3);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to parse resume');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const generatePortfolio = async () => {
    if (!selectedTemplate || !parsedData) {
      setError('Please select a template and parse your resume first');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/portfolio/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          template_id: selectedTemplate.id,
          resume_data: parsedData,
          user_prompt: userPrompt || 'Create a professional portfolio website',
          additional_preferences: {}
        })
      });

      if (response.ok) {
        const data = await response.json();
        setGeneratedPortfolio(data);
        setStep(4);
        fetchMyPortfolios(); // Refresh the list
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to generate portfolio');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const resetBuilder = () => {
    setStep(1);
    setSelectedTemplate(null);
    setResumeFile(null);
    setResumeText('');
    setParsedData(null);
    setUserPrompt('');
    setGeneratedPortfolio(null);
    setError('');
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 py-12 px-4">
        <div className="max-w-md mx-auto">
          <Card>
            <CardHeader className="text-center">
              <Globe className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              <CardTitle className="text-2xl">Portfolio Builder</CardTitle>
              <p className="text-gray-600">Create stunning portfolio websites instantly</p>
            </CardHeader>
            <CardContent className="text-center">
              <Alert className="mb-4">
                <AlertCircle className="w-4 h-4" />
                <AlertDescription>
                  Please sign in to access the Portfolio Builder feature
                </AlertDescription>
              </Alert>
              <Button onClick={login} className="w-full">
                Sign in with Google
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI Portfolio Builder
          </h1>
          <p className="text-xl text-gray-600">
            Transform your resume into a stunning portfolio website in minutes
          </p>
        </div>

        <div className="mb-8">
          <div className="flex justify-center space-x-4">
            <Button
              variant={activeTab === 'create' ? 'default' : 'outline'}
              onClick={() => setActiveTab('create')}
              className="flex items-center gap-2"
            >
              <Zap className="w-4 h-4" />
              Create New
            </Button>
            <Button
              variant={activeTab === 'my-portfolios' ? 'default' : 'outline'}
              onClick={() => setActiveTab('my-portfolios')}
              className="flex items-center gap-2"
            >
              <Globe className="w-4 h-4" />
              My Portfolios
            </Button>
          </div>
        </div>

        {activeTab === 'create' && (
          <div className="max-w-4xl mx-auto">
            {/* Progress Steps */}
            <div className="mb-8">
              <div className="flex items-center justify-center space-x-4">
                {[1, 2, 3, 4].map((num) => (
                  <div key={num} className="flex items-center">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                      step >= num ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-600'
                    }`}>
                      {num}
                    </div>
                    {num < 4 && <div className={`w-12 h-1 ${
                      step > num ? 'bg-purple-600' : 'bg-gray-200'
                    }`} />}
                  </div>
                ))}
              </div>
              <div className="flex justify-center mt-2">
                <div className="text-sm text-gray-600">
                  {step === 1 && 'Choose Template'}
                  {step === 2 && 'Upload Resume'}
                  {step === 3 && 'Customize'}
                  {step === 4 && 'Preview & Share'}
                </div>
              </div>
            </div>

            {/* Step 1: Template Selection */}
            {step === 1 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Palette className="w-5 h-5" />
                    Choose Your Template
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {templates.map((template) => (
                      <div
                        key={template.id}
                        className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
                          selectedTemplate?.id === template.id
                            ? 'border-purple-500 bg-purple-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                        onClick={() => setSelectedTemplate(template)}
                      >
                        <div className="aspect-video bg-gray-100 rounded-lg mb-3 flex items-center justify-center">
                          <Globe className="w-8 h-8 text-gray-400" />
                        </div>
                        <h3 className="font-semibold text-lg mb-1">{template.name}</h3>
                        <p className="text-sm text-gray-600">{template.description}</p>
                      </div>
                    ))}
                  </div>
                  
                  <div className="flex justify-center mt-6">
                    <Button
                      onClick={() => setStep(2)}
                      disabled={!selectedTemplate}
                      className="px-8"
                    >
                      Continue
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Step 2: Resume Upload */}
            {step === 2 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Upload className="w-5 h-5" />
                    Upload Your Resume
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="font-medium mb-3">Upload File</h3>
                      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                        <input
                          type="file"
                          accept=".pdf,.doc,.docx,.txt"
                          onChange={(e) => setResumeFile(e.target.files[0])}
                          className="hidden"
                          id="resume-upload"
                        />
                        <label htmlFor="resume-upload" className="cursor-pointer">
                          <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                          <p className="text-gray-600">Click to upload</p>
                          <p className="text-xs text-gray-400">PDF, DOC, DOCX, TXT</p>
                        </label>
                      </div>
                      {resumeFile && (
                        <div className="mt-3 p-3 bg-green-50 rounded-lg">
                          <div className="flex items-center gap-2">
                            <FileText className="w-4 h-4 text-green-600" />
                            <span className="text-sm text-green-800">{resumeFile.name}</span>
                          </div>
                        </div>
                      )}
                    </div>

                    <div>
                      <h3 className="font-medium mb-3">Or Paste Text</h3>
                      <Textarea
                        placeholder="Paste your resume text here..."
                        value={resumeText}
                        onChange={(e) => setResumeText(e.target.value)}
                        rows={8}
                      />
                    </div>
                  </div>

                  <div className="flex justify-center gap-4 mt-6">
                    <Button variant="outline" onClick={() => setStep(1)}>
                      Back
                    </Button>
                    <Button
                      onClick={parseResume}
                      disabled={loading || (!resumeFile && !resumeText.trim())}
                    >
                      {loading ? 'Processing...' : 'Parse Resume'}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Step 3: Customization */}
            {step === 3 && parsedData && (
              <div className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <User className="w-5 h-5" />
                      Parsed Information
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-medium mb-3">Personal Details</h4>
                        <div className="space-y-2 text-sm">
                          <p><strong>Name:</strong> {parsedData.personal_details.full_name}</p>
                          <p><strong>Email:</strong> {parsedData.personal_details.email}</p>
                          {parsedData.personal_details.phone && (
                            <p><strong>Phone:</strong> {parsedData.personal_details.phone}</p>
                          )}
                          {parsedData.personal_details.location && (
                            <p><strong>Location:</strong> {parsedData.personal_details.location}</p>
                          )}
                        </div>
                      </div>
                      
                      <div>
                        <h4 className="font-medium mb-3">Summary</h4>
                        <div className="space-y-1 text-sm">
                          <p><strong>Experience:</strong> {parsedData.experience.length} positions</p>
                          <p><strong>Projects:</strong> {parsedData.projects.length} projects</p>
                          <p><strong>Skills:</strong> {parsedData.skills.length} skills</p>
                          <p><strong>Education:</strong> {parsedData.education.length} entries</p>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Customization Prompt</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Textarea
                      placeholder="Describe any specific requirements for your portfolio (e.g., 'Make it suitable for software engineering roles', 'Emphasize my design projects', etc.)"
                      value={userPrompt}
                      onChange={(e) => setUserPrompt(e.target.value)}
                      rows={4}
                    />
                    
                    <div className="flex justify-center gap-4 mt-6">
                      <Button variant="outline" onClick={() => setStep(2)}>
                        Back
                      </Button>
                      <Button
                        onClick={generatePortfolio}
                        disabled={loading}
                      >
                        {loading ? 'Generating Portfolio...' : 'Generate Portfolio'}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {/* Step 4: Generated Portfolio */}
            {step === 4 && generatedPortfolio && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    Portfolio Generated Successfully!
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center space-y-4">
                    <div className="p-6 bg-green-50 rounded-lg">
                      <Globe className="w-12 h-12 text-green-600 mx-auto mb-4" />
                      <p className="text-lg font-medium text-green-800 mb-2">
                        Your portfolio is ready!
                      </p>
                      <p className="text-sm text-green-600">
                        Share your portfolio with potential employers
                      </p>
                    </div>

                    <div className="flex flex-wrap justify-center gap-4">
                      <Button
                        onClick={() => window.open(`${process.env.REACT_APP_BACKEND_URL}${generatedPortfolio.live_url}`, '_blank')}
                        className="flex items-center gap-2"
                      >
                        <Eye className="w-4 h-4" />
                        Preview Portfolio
                      </Button>
                      
                      <Button
                        variant="outline"
                        onClick={() => {
                          navigator.clipboard.writeText(`${process.env.REACT_APP_BACKEND_URL}${generatedPortfolio.live_url}`);
                          // You could add a toast notification here
                        }}
                        className="flex items-center gap-2"
                      >
                        <Share className="w-4 h-4" />
                        Copy Link
                      </Button>
                      
                      <Button
                        variant="outline"
                        onClick={resetBuilder}
                        className="flex items-center gap-2"
                      >
                        <Zap className="w-4 h-4" />
                        Create Another
                      </Button>
                    </div>

                    <div className="text-left mt-6 p-4 bg-blue-50 rounded-lg">
                      <p className="text-sm text-blue-800">
                        <strong>Share URL:</strong> {process.env.REACT_APP_BACKEND_URL}{generatedPortfolio.live_url}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {activeTab === 'my-portfolios' && (
          <div className="max-w-4xl mx-auto">
            <Card>
              <CardHeader>
                <CardTitle>My Portfolios</CardTitle>
              </CardHeader>
              <CardContent>
                {myPortfolios.length === 0 ? (
                  <div className="text-center py-8">
                    <Globe className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-600 mb-4">You haven't created any portfolios yet</p>
                    <Button onClick={() => setActiveTab('create')}>
                      Create Your First Portfolio
                    </Button>
                  </div>
                ) : (
                  <div className="grid md:grid-cols-2 gap-4">
                    {myPortfolios.map((portfolio) => (
                      <div key={portfolio.id} className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-lg mb-2">{portfolio.title}</h3>
                        <p className="text-sm text-gray-600 mb-3">
                          Created: {new Date(portfolio.created_at).toLocaleDateString()}
                        </p>
                        <p className="text-sm text-gray-600 mb-4">
                          Views: {portfolio.views}
                        </p>
                        
                        <div className="flex gap-2">
                          <Button
                            size="sm"
                            onClick={() => window.open(`${process.env.REACT_APP_BACKEND_URL}${portfolio.live_url}`, '_blank')}
                          >
                            <Eye className="w-4 h-4 mr-1" />
                            View
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => {
                              navigator.clipboard.writeText(`${process.env.REACT_APP_BACKEND_URL}${portfolio.live_url}`);
                            }}
                          >
                            <Share className="w-4 h-4 mr-1" />
                            Share
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {error && (
          <Alert className="mt-4 max-w-4xl mx-auto border-red-200 bg-red-50">
            <AlertCircle className="w-4 h-4 text-red-600" />
            <AlertDescription className="text-red-800">{error}</AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  );
};

export default PortfolioBuilder;