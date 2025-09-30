import React from "react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";

const FeatureCards = () => {
  const features = [
    {
      icon: "🚀",
      iconBg: "bg-purple-500",
      title: "Career Launch",
      description: "Entry-level tech jobs",
      cta: "Explore Now"
    },
    {
      icon: "📚",
      iconBg: "bg-blue-500",
      title: "Learning Hub",
      description: "Fresher-focused resources",
      cta: "Explore Now"
    },
    {
      icon: "👥",
      iconBg: "bg-green-500",
      title: "Community",
      description: "50,000+ tech freshers",
      cta: "Explore Now"
    },
    {
      icon: "🗺️",
      iconBg: "bg-orange-500",
      title: "Tech Roadmaps",
      description: "Guided career paths",
      cta: "Explore Now"
    }
  ];
  
  return (
    <section className="py-16 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="border-none shadow-lg hover:shadow-xl transition-shadow duration-300 cursor-pointer">
              <CardContent className="p-8 text-center">
                <div className={`w-16 h-16 ${feature.iconBg} rounded-2xl mx-auto mb-6 flex items-center justify-center`}>
                  <span className="text-white text-2xl">{feature.icon}</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600 mb-6">{feature.description}</p>
                <Button variant="link" className="text-blue-600 hover:text-blue-700 p-0 h-auto font-semibold">
                  {feature.cta}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeatureCards;