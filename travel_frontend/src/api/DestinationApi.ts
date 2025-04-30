import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const getDestinations = async () => {
  try {
    const response = await axios.get(`${API_URL}/destinations`);
    return response.data;
  } catch (error) {
    throw new Error("Error fetching destinations");
  }
};

export const getDestinationById = async (id: number) => {
  try {
    const response = await axios.get(`${API_URL}/destinations/${id}`);
    return response.data;
  } catch (error) {
    throw new Error("Error fetching destination by ID");
  }
};
