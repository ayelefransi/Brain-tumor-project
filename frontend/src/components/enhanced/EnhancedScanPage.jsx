import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { Button } from "../ui/Button";
import { LoadingSpinner } from "../ui/LoadingSpinner";
import { Badge } from "../ui/Badge";
import { FiUpload, FiImage, FiActivity, FiDownload } from "react-icons/fi";

const EnhancedScanPage = () => {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const droppedFile = e.dataTransfer.files[0];
    handleFileSelection(droppedFile);
  };

  const handleFileSelection = (selectedFile) => {
    const allowedTypes = ["image/jpeg", "image/png"];
    if (selectedFile && allowedTypes.includes(selectedFile.type)) {
      setFile(selectedFile);
      setError(null);
      setPreviewUrl(URL.createObjectURL(selectedFile));
    } else {
      setFile(null);
      setPreviewUrl(null);
      setError("Please select a valid MRI scan image (JPEG or PNG).");
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    handleFileSelection(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select an MRI scan image to upload.");
      return;
    }

    setIsLoading(true);
    const toastId = toast.loading("Analyzing MRI scan... This may take a moment.");

    try {
      const formData = new FormData();
      formData.append("image", file);

      const response = await axios.post(
        "http://localhost:9000/detection/segement/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data);
      setFile(null);
      setPreviewUrl(null);
      setError(null);
      toast.success("Analysis completed successfully!");
    } catch (error) {
      console.error("Error uploading file:", error);
      setError("An error occurred while analyzing the scan. Please try again.");
      toast.error("Analysis failed. Please try again.");
    } finally {
      setIsLoading(false);
      toast.dismiss(toastId);
    }
  };

  const getClassificationColor = (classification) => {
    switch (classification?.toLowerCase()) {
      case 'no tumour':
        return 'success';
      case 'glioma':
        return 'destructive';
      case 'meningioma':
        return 'warning';
      case 'pituitary':
        return 'info';
      default:
        return 'secondary';
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-900">
          Brain Tumor Detection & Analysis
        </h1>
        <p className="text-gray-600">
          Upload your MRI scan for AI-powered tumor classification and segmentation
        </p>
      </div>

      {/* Upload Section */}
      <Card className="overflow-hidden">
        <CardHeader className="bg-gradient-to-r from-blue-50 to-purple-50">
          <CardTitle className="flex items-center gap-2">
            <FiUpload className="h-5 w-5" />
            Upload MRI Scan
          </CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <div
            className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
              dragActive
                ? "border-blue-500 bg-blue-50"
                : "border-gray-300 hover:border-gray-400"
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept="image/jpeg, image/png"
              onChange={handleFileChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              id="fileInput"
            />
            
            {previewUrl ? (
              <div className="space-y-4">
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="mx-auto max-w-full max-h-64 rounded-lg shadow-md"
                />
                <div className="flex items-center justify-center gap-2">
                  <FiImage className="h-4 w-4 text-green-600" />
                  <span className="text-sm text-green-600 font-medium">
                    Image ready for analysis
                  </span>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
                  <FiUpload className="h-8 w-8 text-gray-400" />
                </div>
                <div>
                  <p className="text-lg font-medium text-gray-900">
                    Drop your MRI scan here
                  </p>
                  <p className="text-sm text-gray-500">
                    or click to browse files (JPEG, PNG)
                  </p>
                </div>
              </div>
            )}
          </div>

          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          <div className="mt-6 flex justify-center">
            <Button
              onClick={handleUpload}
              disabled={!file || isLoading}
              loading={isLoading}
              className="px-8 py-3"
              variant="gradient"
            >
              {isLoading ? "Analyzing..." : "Start Analysis"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Results Section */}
      {result && (
        <div className="grid md:grid-cols-2 gap-6">
          {/* Classification Result */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FiActivity className="h-5 w-5" />
                Classification Result
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center space-y-4">
                <Badge 
                  variant={getClassificationColor(result.classification_result)}
                  className="text-lg px-4 py-2"
                >
                  {result.classification_result}
                </Badge>
                <p className="text-sm text-gray-600">
                  AI-powered classification based on MRI scan analysis
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Segmentation Result */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FiImage className="h-5 w-5" />
                Segmentation Result
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <img
                  src={`http://localhost:9000${result.segmentation_result_url}`}
                  alt="Segmentation Result"
                  className="w-full rounded-lg shadow-md"
                />
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => {
                    const link = document.createElement('a');
                    link.href = `http://localhost:9000${result.segmentation_result_url}`;
                    link.download = 'segmentation_result.png';
                    link.click();
                  }}
                >
                  <FiDownload className="mr-2 h-4 w-4" />
                  Download Result
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <Card>
          <CardContent className="p-8">
            <div className="flex flex-col items-center space-y-4">
              <LoadingSpinner size="xl" />
              <div className="text-center">
                <h3 className="text-lg font-medium text-gray-900">
                  Processing MRI Scan
                </h3>
                <p className="text-sm text-gray-500">
                  Our AI is analyzing your scan for tumor detection and segmentation...
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default EnhancedScanPage;