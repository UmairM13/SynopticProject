import axios from "axios";

const API_URL = "http://localhost:8000/travel/api/analytics";

// Already existing
export const fetchTopDestinations = async () => {
  const res = await axios.get(`${API_URL}/top-destinations`);
  return res.data;
};

export const fetchUserStats = async () => {
  const res = await axios.get(`${API_URL}/user-stats`);
  return res.data;
};

export const fetchRecommendationActivity = async () => {
  const res = await axios.get(`${API_URL}/recommendation-activity`);
  return res.data;
};

// New fetchers for full dashboard 🔥
export const fetchPreferencesDistribution = async () => {
  const res = await axios.get(`${API_URL}/preferences-distribution`);
  return res.data;
};

export const fetchPastDestinationsByNationality = async () => {
  const res = await axios.get(`${API_URL}/past-destinations-by-nationality`);
  return res.data;
};

export const fetchPastDestinationsByAge = async () => {
  const res = await axios.get(`${API_URL}/past-destinations-by-age`);
  return res.data;
};

export const fetchOffSeasonRate = async () => {
  const res = await axios.get(`${API_URL}/off-season-rate`);
  return res.data;
};

export const fetchOffSeasonMonthly = async () => {
  const res = await axios.get(`${API_URL}/off-season-monthly`);
  return res.data;
};
