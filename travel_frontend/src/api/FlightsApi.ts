import axios from "axios";

const AMADEUS_API_URL =
  "https://test.api.amadeus.com/v2/shopping/flight-offers";

const CLIENT_ID = import.meta.env.VITE_CLIENT_ID; // Replace with your actual API Key
const CLIENT_SECRET = import.meta.env.VITE_CLIENT_SECRET; // Replace with your actual API Secret

// Function to obtain access token
const getAccessToken = async () => {
  const formData = new URLSearchParams();
  formData.append("grant_type", "client_credentials");
  formData.append("client_id", CLIENT_ID);
  formData.append("client_secret", CLIENT_SECRET);

  const response = await axios.post(
    "https://test.api.amadeus.com/v1/security/oauth2/token",
    formData.toString(),
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );
  return response.data.access_token;
};

export const searchFlights = async (
  origin: string,
  destination: string,
  tripStartDate: string
  // tripEndDate: string | null = null
) => {
  try {
    const token = await getAccessToken();
    const response = await axios.get(AMADEUS_API_URL, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: {
        originLocationCode: origin,
        destinationLocationCode: destination,
        departureDate: tripStartDate,
        adults: 1,
        max: 20,
        currencyCode: "GBP",
      },
    });
    return response.data.data;
  } catch (error) {
    console.error("Error fetching flights:", error);
    throw error;
  }
};
