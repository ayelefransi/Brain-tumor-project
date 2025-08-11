import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { jwtDecode } from "jwt-decode";
import { useLocation } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { Button } from "../ui/Button";
import { Input } from "../ui/Input";
import { Badge } from "../ui/Badge";
import { 
  FiUser, 
  FiActivity, 
  FiHeart, 
  FiDroplet,
  FiWeight,
  FiFileText,
  FiSave
} from "react-icons/fi";

const EnhancedMedicalRecordForm = () => {
  const location = useLocation();
  const { customerIDK } = location.state;
  const Token = localStorage.getItem("Token");
  const user = Token ? jwtDecode(Token) : null;
  const doctorId = user?.user_id;

  const [formData, setFormData] = useState({
    weight: "",
    systolic_blood_pressure: "",
    diastolic_blood_pressure: "",
    blood_sugar_level: "",
    heart_rate: "",
    cholesterol_level: "",
    doctor_notes: "",
    doctor: doctorId,
    patient: customerIDK,
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    const toastId = toast.loading("Saving medical record...");

    try {
      const response = await axios.post(
        "http://localhost:9000/detection/medicalrecords/",
        formData
      );
      console.log("Data submitted successfully:", response.data);
      toast.success("Medical record saved successfully!");
      
      // Reset form
      setFormData({
        weight: "",
        systolic_blood_pressure: "",
        diastolic_blood_pressure: "",
        blood_sugar_level: "",
        heart_rate: "",
        cholesterol_level: "",
        doctor_notes: "",
        doctor: doctorId,
        patient: customerIDK,
      });
    } catch (error) {
      console.error("Error submitting data:", error);
      toast.error("Failed to save medical record. Please try again.");
    } finally {
      setIsLoading(false);
      toast.dismiss(toastId);
    }
  };

  const formSections = [
    {
      title: "Vital Signs",
      icon: FiActivity,
      fields: [
        { name: "weight", label: "Weight (kg)", icon: FiWeight, type: "number", step: "0.1" },
        { name: "heart_rate", label: "Heart Rate (bpm)", icon: FiHeart, type: "number" },
      ]
    },
    {
      title: "Blood Pressure",
      icon: FiDroplet,
      fields: [
        { name: "systolic_blood_pressure", label: "Systolic (mmHg)", type: "number" },
        { name: "diastolic_blood_pressure", label: "Diastolic (mmHg)", type: "number" },
      ]
    },
    {
      title: "Laboratory Results",
      icon: FiActivity,
      fields: [
        { name: "blood_sugar_level", label: "Blood Sugar (mg/dL)", type: "number", step: "0.1" },
        { name: "cholesterol_level", label: "Cholesterol (mg/dL)", type: "number", step: "0.1" },
      ]
    }
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-900">Medical Record</h1>
        <p className="text-gray-600">
          Complete patient medical information and vital signs
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Form Sections */}
        {formSections.map((section, index) => (
          <Card key={index} className="overflow-hidden">
            <CardHeader className="bg-gradient-to-r from-blue-50 to-purple-50">
              <CardTitle className="flex items-center gap-2">
                <section.icon className="h-5 w-5 text-blue-600" />
                {section.title}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="grid md:grid-cols-2 gap-4">
                {section.fields.map((field) => (
                  <div key={field.name} className="space-y-2">
                    <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
                      {field.icon && <field.icon className="h-4 w-4" />}
                      {field.label}
                    </label>
                    <Input
                      type={field.type}
                      name={field.name}
                      value={formData[field.name]}
                      onChange={handleChange}
                      step={field.step}
                      placeholder={`Enter ${field.label.toLowerCase()}`}
                      className="transition-all duration-200 focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}

        {/* Doctor Notes */}
        <Card>
          <CardHeader className="bg-gradient-to-r from-blue-50 to-purple-50">
            <CardTitle className="flex items-center gap-2">
              <FiFileText className="h-5 w-5 text-blue-600" />
              Clinical Notes
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">
                Diagnosis & Treatment Plan
              </label>
              <textarea
                name="doctor_notes"
                value={formData.doctor_notes}
                onChange={handleChange}
                rows={6}
                placeholder="Enter detailed diagnosis, treatment plan, and clinical observations..."
                className="w-full px-3 py-2 border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
              />
            </div>
          </CardContent>
        </Card>

        {/* Submit Button */}
        <Card>
          <CardContent className="p-6">
            <div className="flex justify-center">
              <Button
                type="submit"
                loading={isLoading}
                size="lg"
                variant="gradient"
                className="px-12"
              >
                <FiSave className="mr-2 h-4 w-4" />
                {isLoading ? "Saving..." : "Save Medical Record"}
              </Button>
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  );
};

export default EnhancedMedicalRecordForm;