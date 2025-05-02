import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

// Already existing
export const fetchTopDestinations = async () => {
  const res = await axios.get(`${API_URL}/analytics//top-destinations`);
  return res.data;
};

export const fetchUserStats = async () => {
  const res = await axios.get(`${API_URL}/analytics//user-stats`);
  return res.data;
};

export const fetchRecommendationActivity = async () => {
  const res = await axios.get(`${API_URL}/analytics//recommendation-activity`);
  return res.data;
};

// New fetchers for full dashboard 🔥
export const fetchPreferencesDistribution = async () => {
  const res = await axios.get(`${API_URL}/analytics//preferences-distribution`);
  return res.data;
};

export const fetchPastDestinationsByNationality = async () => {
  const res = await axios.get(
    `${API_URL}/analytics//past-destinations-by-nationality`
  );
  return res.data;
};

export const fetchPastDestinationsByAge = async () => {
  const res = await axios.get(`${API_URL}/analytics//past-destinations-by-age`);
  return res.data;
};

export const fetchOffSeasonRate = async () => {
  const res = await axios.get(`${API_URL}/analytics//off-season-rate`);
  return res.data;
};

export const fetchOffSeasonMonthly = async () => {
  const res = await axios.get(`${API_URL}/analytics//off-season-monthly`);
  return res.data;
};
