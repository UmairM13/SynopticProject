// import { useEffect, useRef } from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

import Login from "./pages/login";
import Register from "./pages/Register";
import OnboardingFlow from "./pages/onboarding/OnboardingFlow";
import RecommendationPage from "./pages/RecommendationPage";
import UserProfile from "./pages/Notebook";
import AppNavbar from "./components/AppNavbar";
import Preferences from "./pages/onboarding/Preferences";
import DestinationDetailsPage from "./pages/DestinationDetails";
import HomePage from "./pages/HomePage";
import SearchPage from "./pages/SearchPage";
import AdminDashboard from "./pages/AdminDashboard";

// function InactivityLogout() {
//   const navigate = useRef<ReturnType<typeof setTimeout> | null>(null);

//   useEffect(() => {
//     const resetTimer = () => {
//       if (navigate.current) clearTimeout(navigate.current);
//       navigate.current = setTimeout(() => {
//         localStorage.removeItem("session_token");
//         window.location.href = "/login";
//       }, 30 * 60 * 1000); // 30 mins
//     };

//     const events = ["mousemove", "keydown", "click", "scroll"];
//     events.forEach((event) => window.addEventListener(event, resetTimer));
//     resetTimer();

//     return () => {
//       if (navigate.current) clearTimeout(navigate.current);
//       events.forEach((event) => window.removeEventListener(event, resetTimer));
//     };
//   }, []);

//   return null;
// }

function App() {
  const isLoggedIn = !!localStorage.getItem("session_token");
  const userEmail = localStorage.getItem("user_email");

  return (
    <Router>
      <AppNavbar />
      {/* <InactivityLogout /> */}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/onboarding" element={<OnboardingFlow />} />
        <Route path="/search" element={<SearchPage />} />

        {/* Protect pages for logged in users */}
        <Route
          path="/notebook"
          element={isLoggedIn ? <UserProfile /> : <Navigate to="/" />}
        />
        <Route
          path="/recommendations"
          element={isLoggedIn ? <RecommendationPage /> : <Navigate to="/" />}
        />
        <Route
          path="/preferences"
          element={isLoggedIn ? <Preferences /> : <Navigate to="/" />}
        />
        <Route
          path="/destination/:destinationId"
          element={
            isLoggedIn ? <DestinationDetailsPage /> : <Navigate to="/" />
          }
        />
        {/* Catch-all route for 404 */}
        <Route path="/404" element={<div>Page Not Found</div>} />
        {/* If needed, fallback route */}
        <Route path="*" element={<Navigate to="/" />} />

        <Route
          path="/admin"
          element={
            userEmail === "admin@travelmate.com" ? (
              <AdminDashboard />
            ) : (
              <Navigate to="/" />
            )
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
