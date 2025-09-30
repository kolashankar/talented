import React, { useState, useEffect } from 'react';
import { publicApi } from '../services/api';
import { Button } from './ui/button';
import { Input } from './ui/input';
import Header from './Header';

const Internships = () => {
  const [internships, setInternships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [locationFilter, setLocationFilter] = useState('');
  const [durationFilter, setDurationFilter] = useState('');

  useEffect(() => {
    fetchInternships();
  }, [searchTerm, locationFilter, durationFilter]);

  const fetchInternships = async () => {
    try {
      setLoading(true);
      const params = {};
      if (searchTerm) params.search = searchTerm;
      if (locationFilter) params.location = locationFilter;
      if (durationFilter) params.duration = parseInt(durationFilter);
      
      const data = await publicApi.getInternships(params);
      setInternships(data);
    } catch (err) {
      setError('Failed to fetch internships');
      console.error('Error fetching internships:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatStipend = (stipend) => {
    if (!stipend) return 'Unpaid';
    return stipend.includes('₹') ? stipend : `₹${stipend}`;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">📚 Internships</h1>
          <p className="text-gray-600">Start your career with valuable internship opportunities</p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Input
              placeholder="Search internships..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full"
            />
            <Input
              placeholder="Location"
              value={locationFilter}
              onChange={(e) => setLocationFilter(e.target.value)}
              className="w-full"
            />
            <select
              value={durationFilter}
              onChange={(e) => setDurationFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Durations</option>
              <option value="1">1 Month</option>
              <option value="2">2 Months</option>
              <option value="3">3 Months</option>
              <option value="6">6 Months</option>
              <option value="12">12 Months</option>
            </select>
          </div>
        </div>

        {/* Internships Grid */}
        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading internships...</p>
          </div>
        ) : error ? (
          <div className="text-center py-8">
            <p className="text-red-600">{error}</p>
          </div>
        ) : internships.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-600">No internships found matching your criteria</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {internships.map((internship) => (
              <div key={internship.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6 border">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">{internship.title}</h3>
                    <p className="text-blue-600 font-medium">{internship.company}</p>
                  </div>
                  <div className="text-sm text-gray-500">
                    {internship.views} views
                  </div>
                </div>
                
                <div className="space-y-2 mb-4">
                  <div className="flex items-center text-sm text-gray-600">
                    <span className="mr-1">📍</span>
                    {internship.location}
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <span className="mr-1">💰</span>
                    {formatStipend(internship.stipend)}
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <span className="mr-1">⏱️</span>
                    {internship.duration_months} months
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <span className="mr-1">📅</span>
                    Start: {formatDate(internship.start_date)}
                  </div>
                </div>

                {internship.skills_required && internship.skills_required.length > 0 && (
                  <div className="mb-4">
                    <div className="flex flex-wrap gap-1">
                      {internship.skills_required.slice(0, 3).map((skill, index) => (
                        <span key={index} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                          {skill}
                        </span>
                      ))}
                      {internship.skills_required.length > 3 && (
                        <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                          +{internship.skills_required.length - 3} more
                        </span>
                      )}
                    </div>
                  </div>
                )}

                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-500">
                    Posted {formatDate(internship.created_at)}
                  </span>
                  <Button size="sm" className="bg-green-600 hover:bg-green-700">
                    Apply Now
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

export default Internships;