import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import AdminLogin from "./components/admin/AdminLogin";
import AdminDashboard from "./components/admin/AdminDashboard";
import AdminLayout from "./components/admin/AdminLayout";
import JobManagement from "./components/admin/JobManagement";
import InternshipManagement from "./components/admin/InternshipManagement";
import ArticleManagement from "./components/admin/ArticleManagement";
import RoadmapManagement from "./components/admin/RoadmapManagement";
import AIContentGenerator from "./components/admin/AIContentGenerator";
import ResumeReviewer from "./components/ResumeReviewer";
import "./App.css";
import { Toaster } from "./components/ui/toaster";

// Public routes (existing TalentD clone)
import HomePage from "./components/HomePage";

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <BrowserRouter>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<HomePage />} />
            <Route path="/resume-review" element={<ResumeReviewer />} />
            
            {/* Admin Routes */}
            <Route path="/admin/login" element={<AdminLogin />} />
            <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
            <Route path="/admin/*" element={
              <AdminLayout>
                <Routes>
                  <Route path="dashboard" element={<AdminDashboard />} />
                  <Route path="jobs" element={<JobManagement />} />
                  <Route path="internships" element={<InternshipManagement />} />
                  <Route path="articles" element={<ArticleManagement />} />
                  <Route path="roadmaps" element={<RoadmapManagement />} />
                  <Route path="ai-generator" element={<AIContentGenerator />} />
                </Routes>
              </AdminLayout>
            } />
          </Routes>
        </BrowserRouter>
        <Toaster />
      </div>
    </AuthProvider>
  );
}

export default App;