import React from "react";
import { NavLink, useLocation } from "react-router-dom";
import { 
  LayoutDashboard, 
  Briefcase, 
  GraduationCap, 
  FileText, 
  Map, 
  Code2,
  BarChart3,
  Sparkles
} from "lucide-react";
import { cn } from "../../lib/utils";

const AdminSidebar = () => {
  const location = useLocation();
  
  const navigation = [
    {
      name: "Dashboard",
      href: "/admin/dashboard",
      icon: LayoutDashboard
    },
    {
      name: "Jobs",
      href: "/admin/jobs",
      icon: Briefcase
    },
    {
      name: "Internships",
      href: "/admin/internships",
      icon: GraduationCap
    },
    {
      name: "Articles",
      href: "/admin/articles",
      icon: FileText
    },
    {
      name: "Roadmaps",
      href: "/admin/roadmaps",
      icon: Map
    },
    {
      name: "DSA Corner",
      href: "/admin/dsa-corner",
      icon: Code2
    }
  ];

  return (
    <div className="w-64 bg-white border-r border-gray-200 min-h-screen">
      <nav className="p-4 space-y-2">
        {navigation.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.href;
          
          return (
            <NavLink
              key={item.name}
              to={item.href}
              className={cn(
                "flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                isActive
                  ? "bg-blue-50 text-blue-700 border border-blue-200"
                  : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
              )}
            >
              <Icon className={cn(
                "h-5 w-5",
                isActive ? "text-blue-600" : "text-gray-400"
              )} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>
      
      <div className="px-4 pt-4 mt-8 border-t border-gray-200">
        <div className="bg-blue-50 rounded-lg p-3">
          <div className="flex items-center space-x-2 mb-2">
            <Sparkles className="h-4 w-4 text-blue-600" />
            <span className="text-sm font-medium text-blue-900">AI Powered</span>
          </div>
          <p className="text-xs text-blue-700">
            Use AI to generate content automatically and analyze resumes with ATS scoring.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AdminSidebar;