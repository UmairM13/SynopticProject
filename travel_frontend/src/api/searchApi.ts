import axios from "axios";

const API_URL = "http://localhost:8000/travel/api";

export const fetchPopularDestinations = async () => {
  try {
    const response = await axios.get(`${API_URL}/search/popular-destinations`);
    return response.data;
  } catch (error) {
    console.error("Error fetching popular destinations", error);
    throw new Error("Failed to load popular destinations");
  }
};

export const searchDestinations = async (query: string) => {
  try {
    const response = await axios.get(`${API_URL}/search/search`, {
      params: { query },
    });
    return response.data.results;
  } catch (error) {
    console.error("Error searching destinations", error);
    throw new Error("Failed to search destinations");
  }
};
