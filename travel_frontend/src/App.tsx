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
  return (
    <Router>
      <AppNavbar />
      {/* <InactivityLogout /> */}
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/onboarding" element={<OnboardingFlow />} />
        <Route path="/notebook" element={<UserProfile />} />
        <Route path="/recommendations" element={<RecommendationPage />} />
        <Route path="/preferences" element={<Preferences />} />
        <Route
          path="/destination/:destinationId"
          element={<DestinationDetailsPage />}
        />
        {/* Catch-all route for 404 */}
        <Route path="/404" element={<div>Page Not Found</div>} />
        {/* If needed, fallback route */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
