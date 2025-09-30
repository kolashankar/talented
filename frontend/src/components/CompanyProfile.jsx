import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import { Button } from './ui/button';
import { useAuth } from '../contexts/AuthContext';

const CompanyProfile = () => {
  const { companyId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [company, setCompany] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [internships, setInternships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('about');

  useEffect(() => {
    fetchCompanyData();
  }, [companyId]);

  const fetchCompanyData = async () => {
    try {
      setLoading(true);
      
      // Fetch company details
      const companyResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/companies/${companyId}`);
      if (companyResponse.ok) {
        const companyData = await companyResponse.json();
        setCompany(companyData);
      }

      // Fetch company jobs
      const jobsResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/companies/${companyId}/jobs`);
      if (jobsResponse.ok) {
        const jobsData = await jobsResponse.json();
        setJobs(jobsData.jobs || []);
      }

      // Fetch company internships
      const internshipsResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/companies/${companyId}/internships`);
      if (internshipsResponse.ok) {
        const internshipsData = await internshipsResponse.json();
        setInternships(internshipsData.internships || []);
      }

    } catch (err) {
      setError('Failed to load company information');
      console.error('Error fetching company data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApply = (jobId, type) => {
    if (!user) {
      navigate('/login');
      return;
    }
    
    // Navigate to job/internship details or application page
    navigate(`/${type}/${jobId}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading company profile...</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (error || !company) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">
            <div className="text-6xl mb-4">🏢</div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Company Not Found</h1>
            <p className="text-gray-600">The company profile you're looking for could not be found.</p>
            <Button onClick={() => navigate('/')} className="mt-4">
              Back to Home
            </Button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Company Header */}
        <div className="bg-white rounded-lg shadow-sm border p-8 mb-6">
          <div className="flex items-start space-x-6">
            <div className="w-24 h-24 bg-gray-200 rounded-lg flex items-center justify-center">
              {company.logo ? (
                <img src={company.logo} alt={company.name} className="w-full h-full object-cover rounded-lg" />
              ) : (
                <span className="text-3xl">🏢</span>
              )}
            </div>
            
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{company.name}</h1>
              <p className="text-lg text-gray-600 mb-4">{company.industry}</p>
              
              <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                <div className="flex items-center space-x-1">
                  <span>📍</span>
                  <span>{company.location}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <span>👥</span>
                  <span>{company.size || 'Size not specified'}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <span>📅</span>
                  <span>Founded {company.founded || 'N/A'}</span>
                </div>
                {company.website && (
                  <div className="flex items-center space-x-1">
                    <span>🌐</span>
                    <a href={company.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                      Website
                    </a>
                  </div>
                )}
              </div>
            </div>

            <div className="text-right">
              <div className="text-2xl font-bold text-blue-600">{jobs.length + internships.length}</div>
              <div className="text-sm text-gray-600">Open Positions</div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white rounded-lg shadow-sm border mb-6">
          <div className="border-b">
            <nav className="flex space-x-8 px-6">
              {['about', 'jobs', 'internships', 'culture'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm capitalize ${
                    activeTab === tab
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {tab}
                  {tab === 'jobs' && jobs.length > 0 && (
                    <span className="ml-2 px-2 py-1 bg-blue-100 text-blue-600 text-xs rounded-full">
                      {jobs.length}
                    </span>
                  )}
                  {tab === 'internships' && internships.length > 0 && (
                    <span className="ml-2 px-2 py-1 bg-green-100 text-green-600 text-xs rounded-full">
                      {internships.length}
                    </span>
                  )}
                </button>
              ))}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'about' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-3">About {company.name}</h3>
                  <p className="text-gray-700 leading-relaxed">
                    {company.description || 'No description available for this company.'}
                  </p>
                </div>

                {company.benefits && company.benefits.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold mb-3">Benefits & Perks</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {company.benefits.map((benefit, index) => (
                        <div key={index} className="flex items-center space-x-2">
                          <span className="text-green-500">✓</span>
                          <span className="text-gray-700">{benefit}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {company.technologies && company.technologies.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold mb-3">Technologies We Use</h3>
                    <div className="flex flex-wrap gap-2">
                      {company.technologies.map((tech, index) => (
                        <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'jobs' && (
              <div>
                <h3 className="text-lg font-semibold mb-6">Open Job Positions ({jobs.length})</h3>
                {jobs.length > 0 ? (
                  <div className="space-y-4">
                    {jobs.map((job) => (
                      <div key={job.id} className="border rounded-lg p-6 hover:shadow-sm transition-shadow">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="text-lg font-semibold text-gray-900 mb-2">{job.title}</h4>
                            <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                              <span>📍 {job.location}</span>
                              <span>💼 {job.job_type}</span>
                              <span>📊 {job.experience_level}</span>
                            </div>
                            <p className="text-gray-700 mb-4 line-clamp-2">{job.description}</p>
                            {job.skills_required && job.skills_required.length > 0 && (
                              <div className="flex flex-wrap gap-2 mb-4">
                                {job.skills_required.slice(0, 5).map((skill, index) => (
                                  <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                                    {skill}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                          <div className="ml-4">
                            <Button
                              onClick={() => handleApply(job.id, 'jobs')}
                              className="bg-blue-600 hover:bg-blue-700"
                            >
                              Apply Now
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <div className="text-4xl mb-4">💼</div>
                    <p className="text-gray-600">No job openings at the moment</p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'internships' && (
              <div>
                <h3 className="text-lg font-semibold mb-6">Open Internship Positions ({internships.length})</h3>
                {internships.length > 0 ? (
                  <div className="space-y-4">
                    {internships.map((internship) => (
                      <div key={internship.id} className="border rounded-lg p-6 hover:shadow-sm transition-shadow">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="text-lg font-semibold text-gray-900 mb-2">{internship.title}</h4>
                            <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                              <span>📍 {internship.location}</span>
                              <span>⏰ {internship.duration} months</span>
                              <span>💰 {internship.stipend ? `₹${internship.stipend}` : 'Unpaid'}</span>
                            </div>
                            <p className="text-gray-700 mb-4 line-clamp-2">{internship.description}</p>
                            {internship.skills_required && internship.skills_required.length > 0 && (
                              <div className="flex flex-wrap gap-2 mb-4">
                                {internship.skills_required.slice(0, 5).map((skill, index) => (
                                  <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                                    {skill}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                          <div className="ml-4">
                            <Button
                              onClick={() => handleApply(internship.id, 'internships')}
                              className="bg-green-600 hover:bg-green-700"
                            >
                              Apply Now
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <div className="text-4xl mb-4">🎓</div>
                    <p className="text-gray-600">No internship openings at the moment</p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'culture' && (
              <div className="space-y-6">
                <div className="text-center py-8">
                  <div className="text-4xl mb-4">🏢</div>
                  <h3 className="text-lg font-semibold mb-2">Company Culture</h3>
                  <p className="text-gray-600">Learn more about what it's like to work at {company.name}</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center p-6 bg-blue-50 rounded-lg">
                    <div className="text-3xl mb-3">🤝</div>
                    <h4 className="font-semibold mb-2">Collaborative</h4>
                    <p className="text-sm text-gray-600">We believe in teamwork and open communication</p>
                  </div>
                  
                  <div className="text-center p-6 bg-green-50 rounded-lg">
                    <div className="text-3xl mb-3">🚀</div>
                    <h4 className="font-semibold mb-2">Innovative</h4>
                    <p className="text-sm text-gray-600">Always pushing boundaries and trying new approaches</p>
                  </div>
                  
                  <div className="text-center p-6 bg-purple-50 rounded-lg">
                    <div className="text-3xl mb-3">⚖️</div>
                    <h4 className="font-semibold mb-2">Work-Life Balance</h4>
                    <p className="text-sm text-gray-600">We care about your wellbeing and personal growth</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  );
};

export default CompanyProfile;