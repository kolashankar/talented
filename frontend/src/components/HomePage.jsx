import React from "react";
import Header from "./Header";
import HeroSection from "./HeroSection";
import FeatureCards from "./FeatureCards";
import WhyChooseSection from "./WhyChooseSection";
import FeaturedJobs from "./FeaturedJobs";
import CommunitySection from "./CommunitySection";
import ResourcesSection from "./ResourcesSection";
import CompanyLogos from "./CompanyLogos";
import TestimonialsSection from "./TestimonialsSection";
import ArticlesSection from "./ArticlesSection";
import CTASection from "./CTASection";

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-purple-900">
      <Header />
      <HeroSection />
      <div className="bg-white">
        <FeatureCards />
        <WhyChooseSection />
        <FeaturedJobs />
        <CommunitySection />
        <ResourcesSection />
        <CompanyLogos />
        <TestimonialsSection />
        <ArticlesSection />
        <CTASection />
      </div>
    </div>
  );
};

export default HomePage;