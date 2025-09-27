import React from "react";
import { Button } from "./ui/button";

const CTASection = () => {
  return (
    <section className="py-20 px-4 bg-gradient-to-r from-blue-900 via-blue-800 to-purple-900 text-white">
      <div className="max-w-4xl mx-auto text-center">
        <div className="inline-block px-4 py-2 bg-white/10 rounded-full text-sm backdrop-blur-sm mb-6">
          Start Your Tech Journey Today
        </div>
        
        <h2 className="text-4xl lg:text-5xl font-bold mb-6">
          Ready to Land Your First Tech Job?
        </h2>
        
        <p className="text-xl text-blue-100 mb-12 max-w-3xl mx-auto leading-relaxed">
          Join 50,000+ freshers who launched their tech careers with Talentd's resources, community, and opportunities.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-6 justify-center">
          <Button className="bg-white text-blue-900 hover:bg-gray-100 px-8 py-4 text-lg font-semibold rounded-lg">
            Create Free Account
          </Button>
          <Button className="bg-transparent hover:bg-white/10 text-white border-2 border-white/30 px-8 py-4 text-lg font-semibold rounded-lg">
            Browse Fresher Jobs
          </Button>
        </div>
        
        {/* Additional sign-in options */}
        <div className="mt-12 pt-8 border-t border-white/20">
          <p className="text-blue-200 mb-4">Or sign in with:</p>
          <Button className="bg-white/10 hover:bg-white/20 text-white border border-white/30 px-6 py-3 rounded-lg backdrop-blur-sm">
            Sign in with Google
          </Button>
        </div>
      </div>
    </section>
  );
};

export default CTASection;