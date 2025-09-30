import React from "react";
import { Button } from "./ui/button";

const Header = () => {
  return (
    <>
      {/* Top Navigation Bar */}
      <div className="bg-blue-900 py-2 px-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between text-sm">
          <div className="flex items-center space-x-6 text-white">
            <a href="#" className="hover:text-blue-200 transition-colors">Jobs Tracker</a>
            <a href="/resume-review" className="hover:text-blue-200 transition-colors">Resume Review</a>
            <a href="/portfolio-builder" className="hover:text-blue-200 transition-colors">Portfolio Builder</a>
            <a href="#" className="hover:text-blue-200 transition-colors">Income Tax Calculator</a>
            <a href="#" className="hover:text-blue-200 transition-colors">DRDO Internships</a>
          </div>
          <Button className="bg-green-500 hover:bg-green-600 text-white px-4 py-1 text-sm rounded-full">
            Join WhatsApp Community
          </Button>
        </div>
      </div>
      
      {/* Main Navigation */}
      <header className="bg-gradient-to-r from-blue-900 to-blue-800 py-4 px-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-8">
            {/* Logo */}
            <a href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
                <span className="text-blue-900 font-bold text-lg">✱</span>
              </div>
              <span className="text-white text-xl font-bold">Talentd</span>
            </a>
            
            {/* Navigation Links */}
            <nav className="hidden md:flex items-center space-x-6 text-white">
              <a href="/jobs" className="hover:text-blue-200 transition-colors flex items-center space-x-1">
                <span>📋</span>
                <span>Jobs</span>
              </a>
              <a href="/jobs" className="hover:text-blue-200 transition-colors flex items-center space-x-1">
                <span>⭐</span>
                <span>Fresher Jobs</span>
              </a>
              <a href="/internships" className="hover:text-blue-200 transition-colors flex items-center space-x-1">
                <span>📚</span>
                <span>Internships</span>
              </a>
              <a href="/roadmaps" className="hover:text-blue-200 transition-colors flex items-center space-x-1">
                <span>🗺️</span>
                <span>Roadmaps</span>
              </a>
              <a href="/articles" className="hover:text-blue-200 transition-colors flex items-center space-x-1">
                <span>📖</span>
                <span>Articles</span>
              </a>
              <a href="/dsa-corner" className="hover:text-blue-200 transition-colors flex items-center space-x-1">
                <span>⚡</span>
                <span>DSA Corner</span>
              </a>
            </nav>
          </div>
          
          {/* Auth Buttons */}
          <div className="flex items-center space-x-3">
            <a href="/login">
              <Button variant="ghost" className="text-white hover:bg-blue-700">
                Login
              </Button>
            </a>
            <a href="/register">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg">
                Register
              </Button>
            </a>
          </div>
        </div>
      </header>
    </>
  );
};

export default Header;