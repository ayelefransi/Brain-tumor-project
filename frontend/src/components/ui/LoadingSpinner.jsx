import React from 'react';
import { cn } from '../../utils/cn';

const LoadingSpinner = ({ className, size = "default" }) => {
  const sizes = {
    sm: "h-4 w-4",
    default: "h-6 w-6",
    lg: "h-8 w-8",
    xl: "h-12 w-12"
  };

  return (
    <div className="flex items-center justify-center">
      <div
        className={cn(
          "animate-spin rounded-full border-2 border-gray-300 border-t-blue-600",
          sizes[size],
          className
        )}
      />
    </div>
  );
};

export { LoadingSpinner };