import axios from "axios";

const API_URL = "http://localhost:8000/travel/api";

export const signup = async (userData: {
  email: string;
  password: string;
  age: number;
  nationality: string;
  current_city: string;
  current_country: string;
}) => {
  try {
    const response = await axios.post(`${API_URL}/users`, userData);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 400) {
      throw new Error("User already exists");
    }
    throw new Error("Error signing up");
  }
};

export const login = async (userData: { email: string; password: string }) => {
  const response = await fetch(`${API_URL}/users/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    throw new Error("Error logging in");
  }
  const data = await response.json();
  localStorage.setItem("id", data.id);
  localStorage.setItem("session_token", data.session_token);
};

export const logout = async (token: string) => {
  try {
    const response = await fetch(`${API_URL}/logout`, {
      method: "POST",
      headers: {
        "X-Authorization": token,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error logging out");
    }

    // Read the response as text
    const data = await response.text();

    console.log(data); // This will output "Logout successful"
  } catch (error) {
    console.error("An error occurred while logging out:", error);
    throw new Error("Error logging out");
  }
};
