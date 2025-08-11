import React from "react";
import { Link } from "react-router-dom";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";
import { 
  FiActivity, 
  FiShield, 
  FiZap, 
  FiUsers,
  FiArrowRight,
  FiPlay
} from "react-icons/fi";

const EnhancedHeroSection = () => {
  const features = [
    {
      icon: FiActivity,
      title: "AI-Powered Detection",
      description: "Advanced machine learning algorithms for accurate tumor identification"
    },
    {
      icon: FiZap,
      title: "Instant Results",
      description: "Get comprehensive analysis results in seconds, not hours"
    },
    {
      icon: FiShield,
      title: "Secure & Private",
      description: "Your medical data is protected with enterprise-grade security"
    },
    {
      icon: FiUsers,
      title: "Expert Network",
      description: "Connect with specialized medical professionals worldwide"
    }
  ];

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0">
        <div className="absolute top-0 left-0 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute top-0 right-0 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 pt-20 pb-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Content */}
            <div className="space-y-8">
              <div className="space-y-4">
                <Badge variant="outline" className="w-fit bg-white/80 backdrop-blur-sm">
                  🧠 Advanced Medical AI
                </Badge>
                
                <h1 className="text-4xl md:text-6xl font-bold text-gray-900 leading-tight">
                  Empowering Health
                  <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                    Through Technology
                  </span>
                </h1>
                
                <p className="text-xl text-gray-600 leading-relaxed max-w-2xl">
                  Revolutionary brain tumor detection system utilizing cutting-edge AI for early, 
                  accurate diagnosis. Enhancing patient outcomes through advanced imaging analysis 
                  and informed medical decision-making.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Button 
                  asChild 
                  size="lg" 
                  variant="gradient"
                  className="group"
                >
                  <Link to="/login">
                    Get Started
                    <FiArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </Link>
                </Button>
                
                <Button 
                  variant="outline" 
                  size="lg"
                  className="group bg-white/80 backdrop-blur-sm"
                >
                  <FiPlay className="mr-2 h-4 w-4" />
                  Watch Demo
                </Button>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-6 pt-8">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">99.2%</div>
                  <div className="text-sm text-gray-600">Accuracy Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">10K+</div>
                  <div className="text-sm text-gray-600">Scans Analyzed</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">500+</div>
                  <div className="text-sm text-gray-600">Medical Partners</div>
                </div>
              </div>
            </div>

            {/* Right Column - Visual */}
            <div className="relative">
              <div className="relative z-10">
                <img
                  src="/src/assets/img/Custom/brain.svg"
                  alt="Brain Illustration"
                  className="w-full h-auto max-w-lg mx-auto drop-shadow-2xl"
                />
              </div>
              
              {/* Floating Cards */}
              <div className="absolute top-4 right-4 animate-float">
                <Card className="w-48 bg-white/90 backdrop-blur-sm">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                        <FiActivity className="h-5 w-5 text-green-600" />
                      </div>
                      <div>
                        <p className="text-sm font-medium">Scan Complete</p>
                        <p className="text-xs text-gray-500">No tumor detected</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              <div className="absolute bottom-8 left-4 animate-float animation-delay-2000">
                <Card className="w-44 bg-white/90 backdrop-blur-sm">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <FiUsers className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <p className="text-sm font-medium">Expert Review</p>
                        <p className="text-xs text-gray-500">Dr. Smith available</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="relative z-10 py-16 bg-white/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Choose Our Platform?
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Experience the future of medical diagnosis with our comprehensive tumor detection platform
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="group hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2">
                <CardContent className="p-6 text-center">
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                    <feature.icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedHeroSection;