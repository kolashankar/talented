import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [adminUser, setAdminUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [adminToken, setAdminToken] = useState(localStorage.getItem("admin_token"));

  // Set up axios interceptors for tokens
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else if (adminToken) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${adminToken}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token, adminToken]);

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      let userValid = false;
      let adminValid = false;
      
      // Check user authentication
      if (token) {
        try {
          const response = await axios.get(`${API}/user-auth/me`);
          setUser(response.data);
          userValid = true;
        } catch (error) {
          console.error("User auth check failed:", error);
          localStorage.removeItem("token");
          setToken(null);
          setUser(null);
        }
      }
      
      // Check admin authentication
      if (adminToken) {
        try {
          const response = await axios.get(`${API}/auth/me`);
          setAdminUser(response.data);
          adminValid = true;
        } catch (error) {
          console.error("Admin auth check failed:", error);
          localStorage.removeItem("admin_token");
          setAdminToken(null);
          setAdminUser(null);
        }
      }
      
      setLoading(false);
    };

    // Only run once on component mount
    checkAuth();
  }, []); // Remove dependencies to prevent infinite loop

  // Separate useEffect for token changes that only sets axios headers
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else if (adminToken) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${adminToken}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token, adminToken]);

  // Google Login for users
  const login = () => {
    // This would typically open Google OAuth popup
    // For now, we'll simulate the OAuth flow
    window.location.href = `https://accounts.google.com/o/oauth2/auth?client_id=${process.env.REACT_APP_GOOGLE_CLIENT_ID}&redirect_uri=${encodeURIComponent(window.location.origin + '/auth/callback')}&scope=openid%20email%20profile&response_type=code`;
  };

  const handleGoogleCallback = async (code) => {
    try {
      // This would exchange the code for tokens
      // For demo purposes, we'll simulate successful login
      const mockUserData = {
        email: "user@example.com",
        name: "Demo User",
        google_id: "mock_google_id",
        profile_picture: null
      };

      const response = await axios.post(`${API}/user-auth/google-login`, mockUserData);
      const { access_token, user: userData } = response.data;
      
      localStorage.setItem("token", access_token);
      setToken(access_token);
      setUser(userData);
      
      return { success: true };
    } catch (error) {
      console.error("Google login error:", error);
      return { 
        success: false, 
        error: error.response?.data?.detail || "Login failed"
      };
    }
  };

  // Admin Login
  const adminLogin = async (username, password) => {
    try {
      const response = await axios.post(`${API}/auth/login`, {
        username,
        password
      });

      const { access_token, user: userData } = response.data;
      
      localStorage.setItem("admin_token", access_token);
      setAdminToken(access_token);
      setAdminUser(userData);
      
      return { success: true };
    } catch (error) {
      console.error("Admin login error:", error);
      return { 
        success: false, 
        error: error.response?.data?.detail || "Login failed"
      };
    }
  };

  const logoutUser = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  const logoutAdmin = () => {
    localStorage.removeItem("admin_token");
    setAdminToken(null);
    setAdminUser(null);
  };

  const logout = () => {
    logoutUser();
    logoutAdmin();
    delete axios.defaults.headers.common['Authorization'];
  };

  const value = {
    // User auth
    user,
    login,
    logoutUser,
    handleGoogleCallback,
    
    // Admin auth
    adminUser,
    adminLogin,
    logoutAdmin,
    
    // General
    logout,
    loading,
    isAuthenticated: !!user,
    isAdminAuthenticated: !!adminUser
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export { AuthContext };