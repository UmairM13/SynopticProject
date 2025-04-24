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
  localStorage.setItem("has_onboarded", data.has_onboarded);
};

export const logout = async (token: string) => {
  try {
    const response = await fetch(`${API_URL}/users/logout`, {
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

export const updateUser = async (
  userId: number,
  preferences: {
    preferred_terrain?: string;
    preferred_climate?: string;
    holiday_type?: string;
    budget?: number | null;
    trip_start_date?: string | null;
    trip_end_date?: string | null;
  }
) => {
  try {
    const response = await fetch(`${API_URL}/users/${userId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-Authorization": localStorage.getItem("session_token") || "",
      },
      body: JSON.stringify(preferences),
    });

    if (!response.ok) {
      throw new Error("Error updating user preferences");
    }
    return await response.json();
  } catch (error) {
    console.error("An error occurred while updating user preferences:", error);
    throw new Error("Error updating user preferences");
  }
};

export const fetchPastDestinations = async (userId: string) => {
  const res = await fetch(`${API_URL}/users/${userId}/past-destinations`);
  if (!res.ok) {
    throw new Error("Failed to fetch past destinations");
  }
  return await res.json();
};

export const addPastDestination = async (
  userId: string,
  newDestination: {
    destination_name: string;
    trip_start_date?: string;
    trip_end_date?: string;
    rating: string;
    notes?: string;
  }
) => {
  const res = await fetch(`${API_URL}/users/${userId}/past-destinations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newDestination),
  });

  if (!res.ok) {
    throw new Error("Failed to add past destination");
  }
  return await res.json();
};

export const addPastDestinationToUser = async (
  userId: string,
  destination_name: string
) => {
  const res = await fetch(`${API_URL}/users/${userId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "X-Authorization": localStorage.getItem("session_token") || "",
    },
    body: JSON.stringify({
      past_destinations: destination_name,
    }),
  });

  if (!res.ok) {
    throw new Error("Failed to add past destination to user");
  }
  return await res.json();
};

export const getUserById = async (userId: string) => {
  const res = await fetch(`${API_URL}/users/${userId}`, {
    method: "GET",
  });
  if (!res.ok) {
    throw new Error("Failed to fetch user data");
  }
  return await res.json();
};
