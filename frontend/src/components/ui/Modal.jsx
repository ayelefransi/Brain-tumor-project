import React, { useEffect } from 'react';
import { cn } from '../../utils/cn';

const Modal = ({ isOpen, onClose, children, className }) => {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div 
        className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />
      <div 
        className={cn(
          "relative z-50 w-full max-w-lg mx-4 bg-white rounded-xl shadow-2xl transform transition-all duration-300 scale-100",
          className
        )}
      >
        {children}
      </div>
    </div>
  );
};

const ModalHeader = ({ children, className }) => (
  <div className={cn("flex items-center justify-between p-6 border-b", className)}>
    {children}
  </div>
);

const ModalContent = ({ children, className }) => (
  <div className={cn("p-6", className)}>
    {children}
  </div>
);

const ModalFooter = ({ children, className }) => (
  <div className={cn("flex items-center justify-end gap-3 p-6 border-t bg-gray-50 rounded-b-xl", className)}>
    {children}
  </div>
);

export { Modal, ModalHeader, ModalContent, ModalFooter };