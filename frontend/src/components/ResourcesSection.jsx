import React from "react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { mockResources } from "./mockData";

const ResourcesSection = () => {
  return (
    <section className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-block px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-medium mb-4">
            Fresher Resources
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Everything You Need to Succeed
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Tools and resources designed specifically for tech beginners
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockResources.map((resource, index) => (
            <Card key={index} className="border-none shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer hover:-translate-y-1">
              <CardContent className="p-8 text-center">
                <div className={`w-16 h-16 ${resource.bgColor} rounded-2xl mx-auto mb-6 flex items-center justify-center`}>
                  <span className="text-white text-2xl">{resource.icon}</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{resource.title}</h3>
                <p className="text-gray-600 mb-6">{resource.description}</p>
                <Button variant="link" className="text-blue-600 hover:text-blue-700 p-0 h-auto font-semibold">
                  Learn more
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ResourcesSection;