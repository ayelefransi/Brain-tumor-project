import React, { useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import loginService from "../../Services/login.service";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { Button } from "../ui/Button";
import { Input } from "../ui/Input";
import { FiEye, FiEyeOff, FiMail, FiLock, FiArrowRight } from "react-icons/fi";

const EnhancedLoginForm = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    if (errors[name]) {
      setErrors({ ...errors, [name]: "" });
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^\S+@\S+\.\S+$/.test(formData.email)) {
      newErrors.email = "Invalid email format";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 4) {
      newErrors.password = "Password must be at least 4 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    const toastId = toast.loading("Signing in...");

    try {
      const response = await loginService.logIn(formData);
      const { access, user_role } = response.data;

      localStorage.setItem("Token", access);

      const redirectPaths = {
        Patient: "/doctors",
        Doctor: "/scan",
        Receptionist: "/add-patient",
        Radiologist: "/scan",
        Specialist: "/scan",
      };

      toast.success("Login successful!");
      window.location.replace(redirectPaths[user_role] || "/");
    } catch (error) {
      console.error("Login error:", error);
      toast.error("Invalid credentials. Please try again.");
    } finally {
      setLoading(false);
      toast.dismiss(toastId);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl grid lg:grid-cols-2 gap-8 items-center">
        {/* Left Side - Branding */}
        <div className="hidden lg:block space-y-6">
          <div className="space-y-4">
            <h1 className="text-4xl font-bold text-gray-900">
              Welcome Back!
            </h1>
            <p className="text-xl text-gray-600">
              Access your tumor detection results, medical history, and 
              personalized health recommendations.
            </p>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <FiArrowRight className="h-4 w-4 text-blue-600" />
              </div>
              <span className="text-gray-700">Secure medical data access</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <FiArrowRight className="h-4 w-4 text-green-600" />
              </div>
              <span className="text-gray-700">AI-powered health insights</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                <FiArrowRight className="h-4 w-4 text-purple-600" />
              </div>
              <span className="text-gray-700">Expert medical consultations</span>
            </div>
          </div>
        </div>

        {/* Right Side - Login Form */}
        <Card className="w-full max-w-md mx-auto shadow-2xl">
          <CardHeader className="text-center space-y-2">
            <CardTitle className="text-2xl font-bold">Sign In</CardTitle>
            <p className="text-gray-600">Enter your credentials to continue</p>
          </CardHeader>
          
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Email Field */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">
                  Email Address
                </label>
                <div className="relative">
                  <FiMail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Enter your email"
                    className={`pl-10 ${errors.email ? "border-red-500" : ""}`}
                  />
                </div>
                {errors.email && (
                  <p className="text-sm text-red-600">{errors.email}</p>
                )}
              </div>

              {/* Password Field */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">
                  Password
                </label>
                <div className="relative">
                  <FiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    type={showPassword ? "text" : "password"}
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Enter your password"
                    className={`pl-10 pr-10 ${errors.password ? "border-red-500" : ""}`}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? <FiEyeOff className="h-4 w-4" /> : <FiEye className="h-4 w-4" />}
                  </button>
                </div>
                {errors.password && (
                  <p className="text-sm text-red-600">{errors.password}</p>
                )}
              </div>

              {/* Submit Button */}
              <Button
                type="submit"
                loading={loading}
                className="w-full"
                variant="gradient"
                size="lg"
              >
                Sign In
                <FiArrowRight className="ml-2 h-4 w-4" />
              </Button>

              {/* Links */}
              <div className="text-center space-y-2">
                <Link 
                  to="/forgot" 
                  className="text-sm text-blue-600 hover:text-blue-700 transition-colors"
                >
                  Forgot your password?
                </Link>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default EnhancedLoginForm;