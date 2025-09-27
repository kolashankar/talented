import React from "react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { mockArticles } from "./mockData";

const ArticlesSection = () => {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-12">
          <div>
            <div className="inline-block px-4 py-2 bg-orange-100 text-orange-700 rounded-full text-sm font-medium mb-4">
              Learning Resources
            </div>
            <h2 className="text-4xl font-bold text-gray-900">Latest Articles for Freshers</h2>
          </div>
          <Button variant="outline" className="border-orange-600 text-orange-600 hover:bg-orange-50">
            View All Articles
          </Button>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          {mockArticles.map((article) => (
            <Card key={article.id} className="border-none shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer hover:-translate-y-1 overflow-hidden">
              <div className="aspect-video relative overflow-hidden">
                <img 
                  src={article.image} 
                  alt={article.title}
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute top-4 left-4">
                  <span className="bg-white text-blue-600 px-3 py-1 rounded-full text-sm font-medium">
                    {article.category}
                  </span>
                </div>
              </div>
              <CardContent className="p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-3 line-clamp-2 leading-tight">
                  {article.title}
                </h3>
                <p className="text-gray-600 mb-4 line-clamp-3 leading-relaxed">
                  {article.excerpt}
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">{article.date}</span>
                  <Button variant="link" className="text-blue-600 hover:text-blue-700 p-0 h-auto font-semibold">
                    Read Article
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ArticlesSection;