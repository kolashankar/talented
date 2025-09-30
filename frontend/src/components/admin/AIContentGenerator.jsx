import React, { useState } from "react";
import { Sparkles, Wand2, FileText, Briefcase, Map, GraduationCap, Loader2 } from "lucide-react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Textarea } from "../ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { useToast } from "../ui/use-toast";
import { aiApi, adminApi } from "../../services/api";

const AIContentGenerator = () => {
  const [loading, setLoading] = useState(false);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [activeTab, setActiveTab] = useState("job");
  const { toast } = useToast();

  const [jobPrompt, setJobPrompt] = useState("");
  const [internshipPrompt, setInternshipPrompt] = useState("");
  const [articlePrompt, setArticlePrompt] = useState("");
  const [roadmapPrompt, setRoadmapPrompt] = useState("");
  
  const [contentType, setContentType] = useState("");
  const [customPrompt, setCustomPrompt] = useState("");
  const [bulkCount, setBulkCount] = useState(1);
  const [autoSave, setAutoSave] = useState(false);

  const generateJobContent = async () => {
    if (!jobPrompt.trim()) {
      toast({
        title: "Error",
        description: "Please enter a job prompt",
        variant: "destructive"
      });
      return;
    }

    try {
      setLoading(true);
      const response = await aiApi.aiGenerateJob(jobPrompt);
      setGeneratedContent(response.content);
      
      if (autoSave) {
        await adminApi.createJob(response.content);
        toast({
          title: "Success",
          description: "Job content generated and saved successfully"
        });
      } else {
        toast({
          title: "Success",
          description: "Job content generated successfully"
        });
      }
    } catch (error) {
      console.error("Error generating job content:", error);
      toast({
        title: "Error",
        description: "Failed to generate job content",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const generateInternshipContent = async () => {
    if (!internshipPrompt.trim()) {
      toast({
        title: "Error",
        description: "Please enter an internship prompt",
        variant: "destructive"
      });
      return;
    }

    try {
      setLoading(true);
      const response = await aiApi.aiGenerateInternship(internshipPrompt);
      setGeneratedContent(response.content);
      
      if (autoSave) {
        await adminApi.createInternship(response.content);
        toast({
          title: "Success",
          description: "Internship content generated and saved successfully"
        });
      } else {
        toast({
          title: "Success",
          description: "Internship content generated successfully"
        });
      }
    } catch (error) {
      console.error("Error generating internship content:", error);
      toast({
        title: "Error",
        description: "Failed to generate internship content",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const generateArticleContent = async () => {
    if (!articlePrompt.trim()) {
      toast({
        title: "Error",
        description: "Please enter an article prompt",
        variant: "destructive"
      });
      return;
    }

    try {
      setLoading(true);
      const response = await aiApi.generateArticleContent(articlePrompt);
      setGeneratedContent(response);
      toast({
        title: "Success",
        description: "Article content generated successfully"
      });
    } catch (error) {
      console.error("Error generating article content:", error);
      toast({
        title: "Error",
        description: "Failed to generate article content",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const generateRoadmapContent = async () => {
    if (!roadmapPrompt.trim()) {
      toast({
        title: "Error",
        description: "Please enter a roadmap prompt",
        variant: "destructive"
      });
      return;
    }

    try {
      setLoading(true);
      const response = await aiApi.generateRoadmapContent(roadmapPrompt);
      setGeneratedContent(response);
      toast({
        title: "Success",
        description: "Roadmap content generated successfully"
      });
    } catch (error) {
      console.error("Error generating roadmap content:", error);
      toast({
        title: "Error",
        description: "Failed to generate roadmap content",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const generateCustomContent = async () => {
    if (!contentType || !customPrompt.trim()) {
      toast({
        title: "Error",
        description: "Please select content type and enter a prompt",
        variant: "destructive"
      });
      return;
    }

    try {
      setLoading(true);
      const response = await aiApi.generateContent(contentType, customPrompt);
      setGeneratedContent(response);
      toast({
        title: "Success",
        description: "Custom content generated successfully"
      });
    } catch (error) {
      console.error("Error generating custom content:", error);
      toast({
        title: "Error",
        description: "Failed to generate custom content",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      toast({
        title: "Success",
        description: "Content copied to clipboard"
      });
    });
  };

  const clearContent = () => {
    setGeneratedContent(null);
  };

  const generateBulkContent = async () => {
    if (!contentType || !customPrompt.trim()) {
      toast({
        title: "Error",
        description: "Please select content type and enter a prompt",
        variant: "destructive"
      });
      return;
    }

    try {
      setLoading(true);
      const response = await aiApi.aiGenerateMultiple(contentType, customPrompt, bulkCount);
      setGeneratedContent(response.content);
      
      if (autoSave) {
        let savedCount = 0;
        for (const item of response.content) {
          try {
            if (contentType === "job") {
              await adminApi.createJob(item);
            } else if (contentType === "internship") {
              await adminApi.createInternship(item);
            } else if (contentType === "article") {
              await adminApi.createArticle(item);
            } else if (contentType === "roadmap") {
              await adminApi.createRoadmap(item);
            }
            savedCount++;
          } catch (error) {
            console.error(`Error saving item:`, error);
          }
        }
        toast({
          title: "Success",
          description: `Generated ${bulkCount} items, saved ${savedCount} successfully`
        });
      } else {
        toast({
          title: "Success",
          description: `Generated ${bulkCount} ${contentType} items successfully`
        });
      }
    } catch (error) {
      console.error("Error generating bulk content:", error);
      toast({
        title: "Error",
        description: "Failed to generate bulk content",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Content Generator</h1>
          <p className="text-gray-600 mt-2">Generate professional content for jobs, internships, articles, and learning roadmaps</p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <Sparkles className="w-4 h-4" />
          <span>Powered by AI</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Generator Panel */}
        <div className="space-y-6">
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="job">Jobs</TabsTrigger>
              <TabsTrigger value="internship">Internships</TabsTrigger>
              <TabsTrigger value="article">Articles</TabsTrigger>
              <TabsTrigger value="roadmap">Roadmaps</TabsTrigger>
            </TabsList>

            <TabsContent value="job" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Briefcase className="w-5 h-5" />
                    Generate Job Posting
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Job Description Prompt</label>
                    <Textarea
                      placeholder="e.g. Senior Frontend Developer at a fintech startup, React expertise required, remote work available..."
                      value={jobPrompt}
                      onChange={(e) => setJobPrompt(e.target.value)}
                      rows={4}
                    />
                  </div>
                  <Button 
                    onClick={generateJobContent} 
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? (
                      <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Generating...</>
                    ) : (
                      <><Wand2 className="w-4 h-4 mr-2" />Generate Job Content</>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="internship" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <GraduationCap className="w-5 h-5" />
                    Generate Internship Posting
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Internship Description Prompt</label>
                    <Textarea
                      placeholder="e.g. Summer internship for computer science students, web development focus, 3 months duration, mentorship provided..."
                      value={internshipPrompt}
                      onChange={(e) => setInternshipPrompt(e.target.value)}
                      rows={4}
                    />
                  </div>
                  <Button 
                    onClick={generateInternshipContent} 
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? (
                      <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Generating...</>
                    ) : (
                      <><Wand2 className="w-4 h-4 mr-2" />Generate Internship Content</>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="article" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="w-5 h-5" />
                    Generate Article Content
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Article Topic Prompt</label>
                    <Textarea
                      placeholder="e.g. How to prepare for technical interviews, best practices for remote work, career transition from marketing to tech..."
                      value={articlePrompt}
                      onChange={(e) => setArticlePrompt(e.target.value)}
                      rows={4}
                    />
                  </div>
                  <Button 
                    onClick={generateArticleContent} 
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? (
                      <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Generating...</>
                    ) : (
                      <><Wand2 className="w-4 h-4 mr-2" />Generate Article Content</>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="roadmap" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Map className="w-5 h-5" />
                    Generate Learning Roadmap
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Roadmap Topic Prompt</label>
                    <Textarea
                      placeholder="e.g. Complete roadmap to become a full-stack developer, data science learning path for beginners, cybersecurity career roadmap..."
                      value={roadmapPrompt}
                      onChange={(e) => setRoadmapPrompt(e.target.value)}
                      rows={4}
                    />
                  </div>
                  <Button 
                    onClick={generateRoadmapContent} 
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? (
                      <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Generating...</>
                    ) : (
                      <><Wand2 className="w-4 h-4 mr-2" />Generate Roadmap Content</>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          {/* Custom Content Generator */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="w-5 h-5" />
                Custom Content Generator
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Content Type</label>
                <Select value={contentType} onValueChange={setContentType}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select content type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="job_description">Job Description</SelectItem>
                    <SelectItem value="company_overview">Company Overview</SelectItem>
                    <SelectItem value="skill_assessment">Skill Assessment</SelectItem>
                    <SelectItem value="interview_questions">Interview Questions</SelectItem>
                    <SelectItem value="career_advice">Career Advice</SelectItem>
                    <SelectItem value="course_outline">Course Outline</SelectItem>
                    <SelectItem value="project_ideas">Project Ideas</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Custom Prompt</label>
                <Textarea
                  placeholder="Describe what you want to generate in detail..."
                  value={customPrompt}
                  onChange={(e) => setCustomPrompt(e.target.value)}
                  rows={3}
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Bulk Generate Count</label>
                  <Input
                    type="number"
                    min="1"
                    max="10"
                    value={bulkCount}
                    onChange={(e) => setBulkCount(parseInt(e.target.value) || 1)}
                    placeholder="Number of items"
                  />
                </div>
                <div className="flex items-center space-x-2 pt-6">
                  <input
                    type="checkbox"
                    id="autoSave"
                    checked={autoSave}
                    onChange={(e) => setAutoSave(e.target.checked)}
                  />
                  <label htmlFor="autoSave" className="text-sm">Auto-save to database</label>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-2">
                <Button 
                  onClick={generateCustomContent} 
                  disabled={loading}
                  className="w-full"
                >
                  {loading ? (
                    <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Generating...</>
                  ) : (
                    <><Wand2 className="w-4 h-4 mr-2" />Generate Single</>
                  )}
                </Button>
                <Button 
                  onClick={generateBulkContent} 
                  disabled={loading || bulkCount < 2}
                  className="w-full bg-purple-600 hover:bg-purple-700"
                >
                  {loading ? (
                    <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Generating...</>
                  ) : (
                    <><Sparkles className="w-4 h-4 mr-2" />Bulk Generate ({bulkCount})</>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Results Panel */}
        <div className="space-y-6">
          <Card className="h-fit">
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle>Generated Content</CardTitle>
                {generatedContent && (
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => copyToClipboard(JSON.stringify(generatedContent, null, 2))}
                    >
                      Copy JSON
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={clearContent}
                    >
                      Clear
                    </Button>
                  </div>
                )}
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
                </div>
              ) : generatedContent ? (
                <div className="space-y-4">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <pre className="whitespace-pre-wrap text-sm text-gray-800">
                      {JSON.stringify(generatedContent, null, 2)}
                    </pre>
                  </div>
                  <div className="text-sm text-gray-500">
                    You can copy this content and use it in your forms, or modify it as needed.
                  </div>
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <Sparkles className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                  <p>Generated content will appear here</p>
                  <p className="text-sm mt-2">Select a content type and enter a prompt to get started</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Quick Tips */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Tips for Better Results</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start space-x-2">
                  <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0"></span>
                  <span>Be specific about the role, company, and requirements</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0"></span>
                  <span>Mention the industry, company size, and work environment</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0"></span>
                  <span>Include skill level requirements and preferred experience</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0"></span>
                  <span>Specify any unique benefits or selling points</span>
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default AIContentGenerator;