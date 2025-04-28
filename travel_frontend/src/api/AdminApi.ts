import axios from "axios";

const API_URL = "http://localhost:8000/travel/api";

export const fetchTopDestinations = async () => {
  const res = await axios.get(`${API_URL}/analytics/top-destinations`);
  return res.data;
};

export const fetchUserStats = async () => {
  const res = await axios.get(`${API_URL}/analytics/user-stats`);
  return res.data;
};

export const fetchRecommendationActivity = async () => {
  const res = await axios.get(`${API_URL}/analytics/recommendation-activity`);
  return res.data;
};
