import React, { useState } from "react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { mockTestimonials } from "./mockData";

const TestimonialsSection = () => {
  const [currentTestimonial, setCurrentTestimonial] = useState(0);
  
  const nextTestimonial = () => {
    setCurrentTestimonial((prev) => (prev + 1) % mockTestimonials.length);
  };
  
  const prevTestimonial = () => {
    setCurrentTestimonial((prev) => (prev - 1 + mockTestimonials.length) % mockTestimonials.length);
  };
  
  return (
    <section className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-block px-4 py-2 bg-yellow-100 text-yellow-700 rounded-full text-sm font-medium mb-4">
            Fresher Success Stories
          </div>
          <h2 className="text-4xl font-bold text-gray-900">
            Hear From Our Members
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mt-4">
            These freshers landed their dream jobs through Talentd
          </p>
        </div>
        
        <div className="max-w-4xl mx-auto relative">
          <Card className="border-none shadow-2xl">
            <CardContent className="p-12 text-center">
              <div className="text-6xl text-blue-200 mb-6">“</div>
              
              <p className="text-xl text-gray-700 leading-relaxed mb-8 italic">
                {mockTestimonials[currentTestimonial].quote}
              </p>
              
              <div className="flex items-center justify-center space-x-4">
                <img 
                  src={mockTestimonials[currentTestimonial].avatar} 
                  alt={mockTestimonials[currentTestimonial].author}
                  className="w-16 h-16 rounded-full object-cover"
                />
                <div className="text-left">
                  <h4 className="text-lg font-bold text-gray-900">
                    {mockTestimonials[currentTestimonial].author}
                  </h4>
                  <p className="text-blue-600 font-medium">
                    {mockTestimonials[currentTestimonial].position}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          {/* Navigation Buttons */}
          <Button 
            onClick={prevTestimonial}
            variant="outline"
            size="icon"
            className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-4 w-12 h-12 rounded-full shadow-lg bg-white hover:bg-gray-50"
          >
            <ChevronLeft className="h-6 w-6" />
          </Button>
          
          <Button 
            onClick={nextTestimonial}
            variant="outline"
            size="icon"
            className="absolute right-0 top-1/2 transform -translate-y-1/2 translate-x-4 w-12 h-12 rounded-full shadow-lg bg-white hover:bg-gray-50"
          >
            <ChevronRight className="h-6 w-6" />
          </Button>
          
          {/* Dots indicator */}
          <div className="flex justify-center space-x-2 mt-8">
            {mockTestimonials.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentTestimonial(index)}
                className={`w-3 h-3 rounded-full transition-colors duration-200 ${
                  index === currentTestimonial ? 'bg-blue-600' : 'bg-gray-300 hover:bg-gray-400'
                }`}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;