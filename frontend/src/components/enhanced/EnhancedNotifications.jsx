import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";
import { LoadingSpinner } from "../ui/LoadingSpinner";
import { 
  FiBell, 
  FiCheck, 
  FiClock, 
  FiUser, 
  FiMessageSquare,
  FiCalendar,
  FiActivity
} from "react-icons/fi";

const EnhancedNotifications = ({ userRole }) => {
  const Token = localStorage.getItem("Token");
  const user = Token ? jwtDecode(Token) : null;
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        let endpoint = "";
        const userId = user?.user_id;

        switch (userRole) {
          case "Patient":
            endpoint = `http://localhost:9000/detection/doctorpatientmessagenotification/?patient_id=${userId}`;
            break;
          case "Doctor":
            endpoint = `http://localhost:9000/detection/specialistdoctornotifications/?doctor_id=${userId}`;
            break;
          case "Specialist":
            endpoint = `http://localhost:9000/detection/doctorspecialistnotifications/?specialist_id=${userId}`;
            break;
          case "Radiologist":
            endpoint = `http://localhost:9000/detection/doctorradiologistnotifications/?radiologist_id=${userId}`;
            break;
          default:
            endpoint = `http://localhost:9000/detection/notifications/?doctor_id=${userId}`;
        }

        const response = await axios.get(endpoint);
        setNotifications(response.data);
      } catch (error) {
        console.error("Error fetching notifications:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchNotifications();
  }, [userRole, user?.user_id]);

  const markAsRead = async (notificationId, endpoint) => {
    try {
      await axios.patch(`${endpoint}/${notificationId}/`, { read: true });
      setNotifications(
        notifications.map((notification) =>
          notification.id === notificationId
            ? { ...notification, read: true }
            : notification
        )
      );
    } catch (error) {
      console.error("Error marking notification as read:", error);
    }
  };

  const extractId = (message) => {
    const match = message.match(/\(ID: (\d+)\)/);
    return match ? match[1] : "";
  };

  const removeIdFromMessage = (message) => {
    return message.replace(/\(ID: \d+\)/, "").trim();
  };

  const getNotificationIcon = (message) => {
    if (message.includes("Message")) return FiMessageSquare;
    if (message.includes("Appointment")) return FiCalendar;
    if (message.includes("Recommendation")) return FiActivity;
    return FiBell;
  };

  const getNotificationLink = (notification) => {
    const message = notification.message;
    const id = extractId(message);

    if (message.startsWith("New Message")) {
      if (userRole === "Patient") return `/doctorpatientdetail/${id}`;
      if (userRole === "Doctor") return `/specialistdoctorresponsedetail/${id}`;
    }
    if (message.startsWith("New Recommendation")) {
      return `/specialistdoctorrecommendationdetail/${id}`;
    }
    if (message.startsWith("New Request")) {
      return `/doctorspecialistrequestdetail/${id}`;
    }
    if (message.startsWith("New Information")) {
      return `/radiologistdoctordetail/${id}`;
    }
    if (message.startsWith("New appointment")) {
      return `/appointments/${id}`;
    }

    return "#";
  };

  const filteredNotifications = notifications.filter(notification => {
    if (filter === "unread") return !notification.read;
    if (filter === "read") return notification.read;
    return true;
  });

  const unreadCount = notifications.filter(n => !n.read).length;

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
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <FiBell className="h-6 w-6 text-blue-600" />
          <h1 className="text-2xl font-bold text-gray-900">Notifications</h1>
          {unreadCount > 0 && (
            <Badge variant="destructive" className="rounded-full">
              {unreadCount}
            </Badge>
          )}
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant={filter === "all" ? "default" : "outline"}
            size="sm"
            onClick={() => setFilter("all")}
          >
            All
          </Button>
          <Button
            variant={filter === "unread" ? "default" : "outline"}
            size="sm"
            onClick={() => setFilter("unread")}
          >
            Unread ({unreadCount})
          </Button>
          <Button
            variant={filter === "read" ? "default" : "outline"}
            size="sm"
            onClick={() => setFilter("read")}
          >
            Read
          </Button>
        </div>
      </div>

      {/* Notifications List */}
      {filteredNotifications.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <FiBell className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No notifications found
            </h3>
            <p className="text-gray-500">
              {filter === "unread" 
                ? "You're all caught up! No unread notifications."
                : "You don't have any notifications yet."
              }
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {filteredNotifications.map((notification) => {
            const IconComponent = getNotificationIcon(notification.message);
            const link = getNotificationLink(notification);
            const cleanMessage = removeIdFromMessage(notification.message);

            return (
              <Card 
                key={notification.id} 
                className={`transition-all duration-200 hover:shadow-md ${
                  !notification.read ? "border-l-4 border-l-blue-500 bg-blue-50/30" : ""
                }`}
              >
                <CardContent className="p-4">
                  <div className="flex items-start gap-4">
                    <div className={`p-2 rounded-full ${
                      !notification.read ? "bg-blue-100" : "bg-gray-100"
                    }`}>
                      <IconComponent className={`h-4 w-4 ${
                        !notification.read ? "text-blue-600" : "text-gray-600"
                      }`} />
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          {link !== "#" ? (
                            <Link 
                              to={link}
                              className="block hover:text-blue-600 transition-colors"
                            >
                              <p className={`text-sm ${
                                !notification.read ? "font-medium text-gray-900" : "text-gray-700"
                              }`}>
                                {cleanMessage}
                              </p>
                            </Link>
                          ) : (
                            <p className={`text-sm ${
                              !notification.read ? "font-medium text-gray-900" : "text-gray-700"
                            }`}>
                              {cleanMessage}
                            </p>
                          )}
                          
                          <div className="flex items-center gap-2 mt-2">
                            <FiClock className="h-3 w-3 text-gray-400" />
                            <span className="text-xs text-gray-500">
                              {new Date(notification.created_at).toLocaleDateString()}
                            </span>
                            {!notification.read && (
                              <Badge variant="info" className="text-xs">
                                New
                              </Badge>
                            )}
                          </div>
                        </div>

                        {!notification.read && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => markAsRead(
                              notification.id, 
                              userRole === "Patient" 
                                ? "http://localhost:9000/detection/doctorpatientmessagenotification"
                                : "http://localhost:9000/detection/specialistdoctornotifications"
                            )}
                            className="shrink-0"
                          >
                            <FiCheck className="h-3 w-3 mr-1" />
                            Mark Read
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default EnhancedNotifications;