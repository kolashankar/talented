import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';

const StaticPage = () => {
  const { slug } = useParams();
  const [page, setPage] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPage();
  }, [slug]);

  const fetchPage = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/pages/${slug}`);
      
      if (response.ok) {
        const data = await response.json();
        setPage(data);
      } else if (response.status === 404) {
        setError('Page not found');
      } else {
        setError('Failed to load page');
      }
    } catch (err) {
      setError('Failed to load page');
      console.error('Error fetching page:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading page...</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="text-center">
            <div className="text-6xl mb-4">😔</div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">{error}</h1>
            <p className="text-gray-600">The page you're looking for could not be found.</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-sm border p-8">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{page.title}</h1>
            {page.last_updated && (
              <p className="text-sm text-gray-500">
                Last updated: {new Date(page.last_updated).toLocaleDateString()}
              </p>
            )}
          </div>
          
          <div className="prose max-w-none">
            <div 
              dangerouslySetInnerHTML={{ __html: page.content }} 
              className="text-gray-700 leading-relaxed"
            />
          </div>
          
          {page.contact_info && (
            <div className="mt-8 p-6 bg-blue-50 rounded-lg border border-blue-200">
              <h3 className="text-lg font-semibold text-blue-900 mb-3">Need Help?</h3>
              <div className="space-y-2">
                {page.contact_info.email && (
                  <p className="text-blue-800">
                    📧 Email: <a href={`mailto:${page.contact_info.email}`} className="underline">{page.contact_info.email}</a>
                  </p>
                )}
                {page.contact_info.phone && (
                  <p className="text-blue-800">
                    📞 Phone: <a href={`tel:${page.contact_info.phone}`} className="underline">{page.contact_info.phone}</a>
                  </p>
                )}
                {page.contact_info.support_url && (
                  <p className="text-blue-800">
                    🔗 Support: <a href={page.contact_info.support_url} className="underline" target="_blank" rel="noopener noreferrer">Get Help</a>
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
      
      <Footer />
    </div>
  );
};

export default StaticPage;