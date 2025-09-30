import React from "react";
import { Card, CardContent } from "./ui/card";
import { mockCommunityPlatforms } from "./mockData";

const CommunitySection = () => {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-block px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm font-medium mb-4">
            Join 50,000+ Tech Freshers
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Connect With Our Community
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Networking is crucial for freshers. Join our platforms to connect with peers and mentors.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {mockCommunityPlatforms.map((platform, index) => (
            <Card key={index} className={`${platform.bgColor} ${platform.borderColor} border-2 hover:shadow-lg transition-shadow duration-300 cursor-pointer`}>
              <CardContent className="p-8 text-center">
                <div className={`text-4xl mb-4`}>{platform.icon}</div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">{platform.name}</h3>
                <p className={`text-sm ${platform.iconColor} font-medium`}>{platform.members}</p>
                <div className="mt-4">
                  <span className={`inline-block w-6 h-6 ${platform.iconColor.replace('text-', 'bg-')} rounded-full flex items-center justify-center`}>
                    <span className="text-white text-xs">→</span>
                  </span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default CommunitySection;