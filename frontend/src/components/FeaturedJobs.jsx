import React from "react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { mockJobs } from "./mockData";

const FeaturedJobs = () => {
  const getTypeColor = (type) => {
    switch(type.toLowerCase()) {
      case 'internship': return 'bg-green-100 text-green-700';
      case 'fresher': return 'bg-blue-100 text-blue-700';
      case 'experienced': return 'bg-purple-100 text-purple-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };
  
  return (
    <section className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-12">
          <div>
            <div className="inline-block px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium mb-4">
              Handpicked Opportunities
            </div>
            <h2 className="text-4xl font-bold text-gray-900">Featured Fresher Jobs</h2>
          </div>
          <Button variant="outline" className="border-blue-600 text-blue-600 hover:bg-blue-50">
            View All Jobs
          </Button>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {mockJobs.map((job) => (
            <Card key={job.id} className="border-none shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer hover:-translate-y-1">
              <CardContent className="p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center overflow-hidden">
                    <img 
                      src={job.logo} 
                      alt={job.company}
                      className="w-10 h-10 object-contain"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextElementSibling.style.display = 'flex';
                      }}
                    />
                    <div className="w-10 h-10 bg-blue-500 rounded text-white text-sm font-bold flex items-center justify-center" style={{display: 'none'}}>
                      {job.company.charAt(0)}
                    </div>
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900 text-lg">{job.company}</h3>
                  </div>
                </div>
                
                <h4 className="font-semibold text-gray-800 mb-3 line-clamp-2 leading-tight">
                  {job.title}
                </h4>
                
                <div className="flex flex-wrap gap-2 mb-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${getTypeColor(job.type)}`}>
                    {job.type}
                  </span>
                  <span className="px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                    {job.location}
                  </span>
                  <span className="px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                    {job.workType}
                  </span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        
        <div className="text-center mt-12">
          <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold">
            View All Jobs
          </Button>
        </div>
      </div>
    </section>
  );
};

export default FeaturedJobs;