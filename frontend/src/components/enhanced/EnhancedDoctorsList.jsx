import React, { useState, useEffect } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";
import { Input } from "../ui/Input";
import { LoadingSpinner } from "../ui/LoadingSpinner";
import { 
  FiSearch, 
  FiPhone, 
  FiMapPin, 
  FiUser, 
  FiCalendar,
  FiFilter
} from "react-icons/fi";

const EnhancedDoctorsList = () => {
  const [doctors, setDoctors] = useState([]);
  const [filteredDoctors, setFilteredDoctors] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCity, setSelectedCity] = useState("");
  const [loading, setLoading] = useState(true);
  const [expandedBios, setExpandedBios] = useState({});

  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const response = await axios.get(
          "http://localhost:9000/detection/customers/doctors/"
        );
        setDoctors(response.data);
        setFilteredDoctors(response.data);
      } catch (error) {
        console.error("Error fetching doctors:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDoctors();
  }, []);

  useEffect(() => {
    let filtered = doctors;

    if (searchTerm) {
      filtered = filtered.filter(
        (doctor) =>
          doctor.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          doctor.last_name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (selectedCity) {
      filtered = filtered.filter(
        (doctor) => doctor.city.toLowerCase() === selectedCity.toLowerCase()
      );
    }

    setFilteredDoctors(filtered);
  }, [searchTerm, selectedCity, doctors]);

  const toggleBio = (doctorId) => {
    setExpandedBios((prev) => ({
      ...prev,
      [doctorId]: !prev[doctorId],
    }));
  };

  const renderBio = (bio, doctorId) => {
    const isExpanded = expandedBios[doctorId];
    const words = bio?.split(" ") || [];
    const shouldShowToggle = words.length > 25;
    
    return (
      <div className="space-y-2">
        <p className="text-sm text-gray-600">
          {isExpanded ? bio : words.slice(0, 25).join(" ") + (shouldShowToggle ? "..." : "")}
        </p>
        {shouldShowToggle && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => toggleBio(doctorId)}
            className="text-blue-600 hover:text-blue-700 p-0 h-auto"
          >
            {isExpanded ? "Show Less" : "Read More"}
          </Button>
        )}
      </div>
    );
  };

  const uniqueCities = [...new Set(doctors.map(doctor => doctor.city))];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <LoadingSpinner size="xl" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-900">Find Your Doctor</h1>
        <p className="text-gray-600">
          Connect with experienced medical professionals for your healthcare needs
        </p>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-6">
          <div className="grid md:grid-cols-3 gap-4">
            <div className="relative">
              <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                placeholder="Search doctors by name..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <div className="relative">
              <FiFilter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <select
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
                className="w-full h-10 pl-10 pr-3 border border-input bg-background rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <option value="">All Cities</option>
                {uniqueCities.map((city) => (
                  <option key={city} value={city}>
                    {city}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-center gap-2">
              <Badge variant="outline">
                {filteredDoctors.length} doctor{filteredDoctors.length !== 1 ? 's' : ''} found
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Doctors Grid */}
      {filteredDoctors.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <FiUser className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No doctors found</h3>
            <p className="text-gray-500">Try adjusting your search criteria</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDoctors.map((doctor) => (
            <Card key={doctor.id} className="group hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
              <CardHeader className="text-center pb-4">
                <div className="relative mx-auto">
                  <img
                    src={`http://localhost:9000${doctor.image}`}
                    alt={`Dr. ${doctor.first_name} ${doctor.last_name}`}
                    className="w-20 h-20 rounded-full object-cover border-4 border-white shadow-lg"
                  />
                  <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-green-500 rounded-full border-2 border-white"></div>
                </div>
                <CardTitle className="text-lg">
                  Dr. {doctor.first_name} {doctor.last_name}
                </CardTitle>
                <Badge variant="secondary" className="w-fit mx-auto">
                  {doctor.role}
                </Badge>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <FiPhone className="h-4 w-4" />
                    <span>{doctor.phone}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <FiMapPin className="h-4 w-4" />
                    <span>{doctor.city}</span>
                  </div>
                </div>

                {doctor.bio && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">About</h4>
                    {renderBio(doctor.bio, doctor.id)}
                  </div>
                )}

                <div className="pt-4 border-t">
                  <Button 
                    className="w-full"
                    variant="gradient"
                  >
                    <FiCalendar className="mr-2 h-4 w-4" />
                    Book Appointment
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default EnhancedDoctorsList;