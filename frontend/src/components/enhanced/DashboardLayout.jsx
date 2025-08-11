import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useUserRole, useAuth } from '../../context/AuthContext';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { 
  FiMenu, 
  FiX, 
  FiBell, 
  FiUser, 
  FiActivity, 
  FiUpload, 
  FiMessageSquare,
  FiCalendar,
  FiFileText,
  FiUsers,
  FiSettings,
  FiLogOut,
  FiHome
} from 'react-icons/fi';

const DashboardLayout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { userRole } = useUserRole();
  const { isLogged } = useAuth();
  const location = useLocation();

  const navigation = {
    Patient: [
      { name: 'Dashboard', href: '/doctors', icon: FiHome },
      { name: 'Doctors', href: '/doctors', icon: FiUsers },
      { name: 'Notifications', href: '/doctorpatientnotifications', icon: FiBell },
      { name: 'Recommendations', href: '/viewrecommendation', icon: FiFileText },
      { name: 'Schedule', href: '/schedule', icon: FiCalendar },
    ],
    Doctor: [
      { name: 'Dashboard', href: '/scan', icon: FiHome },
      { name: 'Scan', href: '/scan', icon: FiActivity },
      { name: 'Notifications', href: '/alldoctornotification', icon: FiBell },
      { name: 'Messages', href: '/alldoctormessage', icon: FiMessageSquare },
      { name: 'Upload', href: '/alldoctorupload', icon: FiUpload },
      { name: 'Medical Records', href: '/alldoctorrecord', icon: FiFileText },
      { name: 'Patients', href: '/patients', icon: FiUsers },
    ],
    Specialist: [
      { name: 'Dashboard', href: '/scan', icon: FiHome },
      { name: 'Scan', href: '/scan', icon: FiActivity },
      { name: 'Notifications', href: '/doctorspecialistnotification', icon: FiBell },
      { name: 'Responses', href: '/allspecialistresponse', icon: FiMessageSquare },
      { name: 'Appointments', href: '/appointement-list', icon: FiCalendar },
    ],
    Radiologist: [
      { name: 'Dashboard', href: '/scan', icon: FiHome },
      { name: 'Scan', href: '/scan', icon: FiActivity },
      { name: 'Notifications', href: '/doctorradiologistnotification', icon: FiBell },
      { name: 'Upload to Doctor', href: '/postradiotodoctor', icon: FiUpload },
    ]
  };

  const currentNav = navigation[userRole] || navigation.Patient;

  if (!isLogged) {
    return children;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-xl transform transition-transform duration-300 ease-in-out lg:translate-x-0 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex items-center justify-between h-16 px-6 border-b">
          <Link to="/" className="text-xl font-bold text-gray-900">
            TUMOR TRACK
          </Link>
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            onClick={() => setSidebarOpen(false)}
          >
            <FiX className="h-5 w-5" />
          </Button>
        </div>

        <nav className="mt-6 px-3">
          <div className="space-y-1">
            {currentNav.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    "flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200",
                    isActive
                      ? "bg-blue-50 text-blue-700 border-r-2 border-blue-700"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  )}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon className={cn("mr-3 h-5 w-5", isActive ? "text-blue-700" : "text-gray-400")} />
                  {item.name}
                </Link>
              );
            })}
          </div>

          <div className="mt-8 pt-6 border-t">
            <div className="space-y-1">
              <Link
                to="/profile"
                className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 rounded-lg hover:bg-gray-50 hover:text-gray-900 transition-all duration-200"
                onClick={() => setSidebarOpen(false)}
              >
                <FiUser className="mr-3 h-5 w-5 text-gray-400" />
                Profile
              </Link>
              <Link
                to="/contact"
                className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 rounded-lg hover:bg-gray-50 hover:text-gray-900 transition-all duration-200"
                onClick={() => setSidebarOpen(false)}
              >
                <FiSettings className="mr-3 h-5 w-5 text-gray-400" />
                Contact
              </Link>
            </div>
          </div>
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-4 border-t">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <FiUser className="h-4 w-4 text-white" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">User</p>
                <Badge variant="outline" className="text-xs">
                  {userRole}
                </Badge>
              </div>
            </div>
            <Button variant="ghost" size="icon">
              <FiLogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <div className="sticky top-0 z-40 bg-white border-b shadow-sm">
          <div className="flex items-center justify-between h-16 px-4 sm:px-6">
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <FiMenu className="h-5 w-5" />
            </Button>

            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="icon" className="relative">
                <FiBell className="h-5 w-5" />
                <Badge className="absolute -top-1 -right-1 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs">
                  3
                </Badge>
              </Button>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="p-4 sm:p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;