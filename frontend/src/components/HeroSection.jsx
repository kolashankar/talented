import React from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card, CardContent } from "./ui/card";
import { Search } from "lucide-react";

const HeroSection = () => {
  return (
    <section className="py-20 px-4 text-white">
      <div className="max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <div className="inline-block px-4 py-2 bg-white/10 rounded-full text-sm backdrop-blur-sm">
              ✨ India's #1 Platform for Tech Freshers
            </div>
            
            <div className="space-y-6">
              <h1 className="text-5xl lg:text-6xl font-bold leading-tight">
                From <span className="text-blue-300">Campus</span> to <span className="text-purple-300">Career</span>
              </h1>
              <p className="text-xl text-blue-100 leading-relaxed">
                Join 50,000+ freshers who landed tech jobs with our entry-level 
                opportunities, proven learning paths, and supportive community.
              </p>
            </div>
            
            {/* Search Bar */}
            <div className="bg-white rounded-xl p-2 flex items-center space-x-2 shadow-2xl">
              <div className="flex-1 flex items-center space-x-2 px-4">
                <Search className="h-5 w-5 text-gray-400" />
                <Input 
                  placeholder="Search entry-level jobs..." 
                  className="border-none bg-transparent text-gray-700 placeholder-gray-400 focus:ring-0"
                />
              </div>
              <Button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold">
                Find Jobs →
              </Button>
            </div>
            
            {/* Community Info */}
            <div className="flex items-center space-x-4">
              <div className="flex -space-x-2">
                <div className="w-10 h-10 bg-blue-500 rounded-full border-2 border-white"></div>
                <div className="w-10 h-10 bg-purple-500 rounded-full border-2 border-white"></div>
                <div className="w-10 h-10 bg-green-500 rounded-full border-2 border-white"></div>
              </div>
              <div>
                <p className="font-semibold">50,000+ fresher community</p>
                <p className="text-blue-200 text-sm">All with 0-2 years experience</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4 text-sm">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                <span>Verified Jobs</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-blue-400 rounded-full"></div>
                <span>Entry-level focused</span>
              </div>
            </div>
            
            <div className="flex space-x-4">
              <Button className="bg-white/10 hover:bg-white/20 text-white border border-white/20 px-8 py-3 rounded-lg backdrop-blur-sm">
                Browse Fresher Jobs →
              </Button>
              <Button className="bg-transparent hover:bg-white/10 text-white border border-white/30 px-8 py-3 rounded-lg">
                Join Community
              </Button>
            </div>
          </div>
          
          {/* Right Stats Cards */}
          <div className="grid grid-cols-2 gap-4">
            <Card className="bg-white/10 backdrop-blur-sm border-white/20">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-blue-500 rounded-xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-white text-xl">👥</span>
                </div>
                <div className="text-3xl font-bold text-white mb-1">46,229</div>
                <div className="text-blue-200 text-sm font-medium mb-2">Active Community Members</div>
                <div className="text-blue-300 text-xs">Freshers helping freshers</div>
              </CardContent>
            </Card>
            
            <Card className="bg-white/10 backdrop-blur-sm border-white/20">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-purple-500 rounded-xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-white text-xl">📈</span>
                </div>
                <div className="text-3xl font-bold text-white mb-1">623,117</div>
                <div className="text-blue-200 text-sm font-medium mb-2">Monthly Readers</div>
                <div className="text-blue-300 text-xs">Tech career content</div>
              </CardContent>
            </Card>
            
            <Card className="bg-white/10 backdrop-blur-sm border-white/20">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-green-500 rounded-xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-white text-xl">💼</span>
                </div>
                <div className="text-3xl font-bold text-white mb-1">42,528</div>
                <div className="text-blue-200 text-sm font-medium mb-2">LinkedIn Followers</div>
                <div className="text-blue-300 text-xs">Professional network</div>
              </CardContent>
            </Card>
            
            <Card className="bg-white/10 backdrop-blur-sm border-white/20">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-orange-500 rounded-xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-white text-xl">✅</span>
                </div>
                <div className="text-3xl font-bold text-white mb-1">102,328</div>
                <div className="text-blue-200 text-sm font-medium mb-2">Registered Users</div>
                <div className="text-blue-300 text-xs">Career focused freshers</div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;