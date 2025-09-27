import React from "react";

const WhyChooseSection = () => {
  const features = [
    {
      icon: "💡",
      title: "Built for Freshers",
      description: "Resources tailored specifically for tech beginners with 0-2 years experience",
      bgColor: "bg-yellow-50",
      borderColor: "border-yellow-200"
    },
    {
      icon: "⭐",
      title: "Curated Opportunities", 
      description: "Handpicked entry-level roles from companies willing to train and develop freshers",
      bgColor: "bg-blue-50",
      borderColor: "border-blue-200"
    },
    {
      icon: "🤝",
      title: "Supportive Network",
      description: "Connect with peers, mentors and hiring managers in a safe, supportive environment",
      bgColor: "bg-green-50",
      borderColor: "border-green-200"
    }
  ];
  
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-block px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium mb-4">
            Why Choose Talentd
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Designed Exclusively for Tech Freshers
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Our platform focuses specifically on the unique needs of entry-level tech talent
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className={`${feature.bgColor} ${feature.borderColor} border-2 rounded-2xl p-8 text-center hover:shadow-lg transition-shadow duration-300`}>
              <div className="text-4xl mb-6">{feature.icon}</div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">{feature.title}</h3>
              <p className="text-gray-700 leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default WhyChooseSection;