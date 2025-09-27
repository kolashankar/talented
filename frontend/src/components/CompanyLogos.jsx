import React from "react";
import { mockCompanyLogos } from "./mockData";

const CompanyLogos = () => {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-block px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm font-medium mb-4">
            Success Stories
          </div>
          <h2 className="text-4xl font-bold text-gray-900">
            Our Members Work At
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mt-4">
            Talentd freshers have secured positions at these top tech companies
          </p>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-6">
          {mockCompanyLogos.map((company, index) => (
            <div key={index} className="bg-white rounded-xl p-6 flex items-center justify-center hover:shadow-lg transition-shadow duration-300">
              <img 
                src={company.logo} 
                alt={company.name}
                className="h-12 w-auto object-contain grayscale hover:grayscale-0 transition-all duration-300"
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextElementSibling.style.display = 'flex';
                }}
              />
              <div className="h-12 bg-gray-200 rounded text-gray-600 text-sm font-bold flex items-center justify-center px-2" style={{display: 'none'}}>
                {company.name}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default CompanyLogos;