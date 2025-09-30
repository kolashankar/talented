import React, { useState } from 'react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Alert, AlertDescription } from '../ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Badge } from '../ui/badge';
import { 
  Briefcase, GraduationCap, FileText, Map, Code, 
  Wand2, Image, Building, Loader2, CheckCircle, 
  AlertCircle, Copy, ExternalLink
} from 'lucide-react';

const AIFormFiller = () => {
  const [activeTab, setActiveTab] = useState('job');
  const [userPrompt, setUserPrompt] = useState('');
  const [generateImages, setGenerateImages] = useState(true);
  const [generateLogos, setGenerateLogos] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const contentTypes = {
    job: {
      icon: Briefcase,
      title: 'Job Posting',
      description: 'Generate comprehensive job postings with company details',
      placeholder: 'e.g., "Senior React Developer at a fintech startup in Bangalore"',
      fields: ['title', 'company', 'description', 'requirements', 'responsibilities', 'salary_range', 'skills_required']
    },
    internship: {
      icon: GraduationCap,
      title: 'Internship',
      description: 'Create detailed internship opportunities for students',
      placeholder: 'e.g., "Machine Learning internship at AI research company"',
      fields: ['title', 'company', 'description', 'stipend', 'duration', 'skills_required']
    },
    article: {
      icon: FileText,
      title: 'Article',
      description: 'Write informative tech articles and career guides',
      placeholder: 'e.g., "Complete guide to becoming a full-stack developer in 2024"',
      fields: ['title', 'content', 'category', 'tags', 'reading_time_minutes']
    },
    roadmap: {
      icon: Map,
      title: 'Learning Roadmap',
      description: 'Create structured learning paths with detailed steps',
      placeholder: 'e.g., "Complete DevOps engineer roadmap for beginners"',
      fields: ['title', 'description', 'difficulty_level', 'steps', 'estimated_completion_time']
    },
    dsa: {
      icon: Code,
      title: 'DSA Problem',
      description: 'Generate coding interview problems with solutions',
      placeholder: 'e.g., "Medium difficulty array problem about finding duplicates"',
      fields: ['title', 'description', 'difficulty', 'examples', 'test_cases', 'hints']
    }
  };

  const handleGenerate = async () => {
    if (!userPrompt.trim()) {
      setError('Please enter a description for what you want to generate');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const token = localStorage.getItem('admin_token');
      const formData = new FormData();
      formData.append('user_prompt', userPrompt);
      formData.append('generate_images', generateImages);
      formData.append('generate_logos', generateLogos);

      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/ai-enhanced/form-filler/${activeTab}`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        }
      );

      if (response.ok) {
        const data = await response.json();
        setResult(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to generate content');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(JSON.stringify(text, null, 2));
  };

  const renderFormData = (data) => {
    const currentType = contentTypes[activeTab];
    
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Generated {currentType.title}</h3>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => copyToClipboard(data.form_data)}
            >
              <Copy className="w-4 h-4 mr-2" />
              Copy JSON
            </Button>
            <Badge variant="secondary">
              Confidence: {Math.round(data.confidence_score * 100)}%
            </Badge>
          </div>
        </div>

        {/* Key Fields Display */}
        <div className="grid gap-4">
          {currentType.fields.map(field => {
            const value = data.form_data[field];
            if (!value) return null;

            return (
              <Card key={field}>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm capitalize">
                    {field.replace('_', ' ')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {Array.isArray(value) ? (
                    <div className="flex flex-wrap gap-1">
                      {value.map((item, idx) => (
                        <Badge key={idx} variant="outline">
                          {typeof item === 'object' ? JSON.stringify(item) : item}
                        </Badge>
                      ))}
                    </div>
                  ) : typeof value === 'object' ? (
                    <pre className="text-xs bg-gray-100 p-2 rounded overflow-auto">
                      {JSON.stringify(value, null, 2)}
                    </pre>
                  ) : (
                    <p className="text-sm">{value}</p>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Generated Images */}
        {data.generated_images && Object.keys(data.generated_images).length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center">
                <Image className="w-4 h-4 mr-2" />
                Generated Images
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {Object.entries(data.generated_images).map(([key, url]) => (
                  <div key={key} className="space-y-2">
                    <img
                      src={url}
                      alt={key}
                      className="w-full h-32 object-cover rounded border"
                    />
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-600 capitalize">
                        {key.replace('_', ' ')}
                      </span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => window.open(url, '_blank')}
                      >
                        <ExternalLink className="w-3 h-3" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Generated Logos */}
        {data.generated_logos && Object.keys(data.generated_logos).length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center">
                <Building className="w-4 h-4 mr-2" />
                Generated Logos
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-4 md:grid-cols-6 gap-4">
                {Object.entries(data.generated_logos).map(([key, url]) => (
                  <div key={key} className="space-y-2">
                    <img
                      src={url}
                      alt={key}
                      className="w-full h-16 object-contain rounded border bg-white"
                    />
                    <span className="text-xs text-gray-600 capitalize text-center block">
                      {key.replace('_', ' ')}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Suggestions */}
        {data.suggestions && data.suggestions.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">AI Suggestions</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-1">
                {data.suggestions.map((suggestion, idx) => (
                  <li key={idx} className="text-sm text-gray-600 flex items-start">
                    <CheckCircle className="w-3 h-3 mt-1 mr-2 text-green-500 flex-shrink-0" />
                    {suggestion}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
      </div>
    );
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold flex items-center justify-center">
          <Wand2 className="w-8 h-8 mr-3 text-purple-600" />
          AI Form Filler
        </h1>
        <p className="text-gray-600">
          Generate comprehensive content with AI - complete with images, logos, and detailed information
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-5">
          {Object.entries(contentTypes).map(([key, type]) => {
            const Icon = type.icon;
            return (
              <TabsTrigger key={key} value={key} className="flex items-center">
                <Icon className="w-4 h-4 mr-2" />
                <span className="hidden sm:inline">{type.title}</span>
              </TabsTrigger>
            );
          })}
        </TabsList>

        {Object.entries(contentTypes).map(([key, type]) => {
          const Icon = type.icon;
          return (
            <TabsContent key={key} value={key}>
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Icon className="w-5 h-5 mr-2" />
                    Generate {type.title}
                  </CardTitle>
                  <p className="text-sm text-gray-600">{type.description}</p>
                </CardHeader>
                <CardContent className="space-y-4">
                  {error && (
                    <Alert variant="destructive">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>{error}</AlertDescription>
                    </Alert>
                  )}

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">
                        Describe what you want to generate
                      </label>
                      <Textarea
                        placeholder={type.placeholder}
                        value={userPrompt}
                        onChange={(e) => setUserPrompt(e.target.value)}
                        rows={3}
                        className="w-full"
                      />
                    </div>

                    <div className="flex flex-wrap gap-4">
                      <label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={generateImages}
                          onChange={(e) => setGenerateImages(e.target.checked)}
                          className="rounded"
                        />
                        <span className="text-sm">Generate Images</span>
                      </label>

                      {(key === 'job' || key === 'internship' || key === 'roadmap' || key === 'dsa') && (
                        <label className="flex items-center space-x-2">
                          <input
                            type="checkbox"
                            checked={generateLogos}
                            onChange={(e) => setGenerateLogos(e.target.checked)}
                            className="rounded"
                          />
                          <span className="text-sm">Generate Logos/Icons</span>
                        </label>
                      )}
                    </div>

                    <Button
                      onClick={handleGenerate}
                      disabled={loading || !userPrompt.trim()}
                      className="w-full"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          Generating...
                        </>
                      ) : (
                        <>
                          <Wand2 className="w-4 h-4 mr-2" />
                          Generate {type.title}
                        </>
                      )}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          );
        })}
      </Tabs>

      {/* Results */}
      {result && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center text-green-600">
              <CheckCircle className="w-5 h-5 mr-2" />
              Content Generated Successfully
            </CardTitle>
          </CardHeader>
          <CardContent>
            {renderFormData(result)}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default AIFormFiller;
