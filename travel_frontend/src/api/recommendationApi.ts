const BASE_URL = "http://localhost:8000/travel/api";

export const fetchRecommendations = async (token: string, user_id: string) => {
  const response = await fetch(`${BASE_URL}/recommendations/${user_id}`, {
    headers: {
      "X-Authorization": token,
    },
  });

  if (!response.ok) throw new Error("Failed to fetch recommendations");

  return response.json();
};

export const saveRecommendation = async (
  token: string,
  destination_id: number,
  destination_name: string
) => {
  const response = await fetch(`${BASE_URL}/recommendations/save`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Authorization": token,
    },
    body: JSON.stringify({ destination_id, destination_name }),
  });

  if (!response.ok) throw new Error("Failed to save recommendation");
};

export const fetchExplanation = async (
  token: string,
  user_id: string,
  destination_id: number
) => {
  const response = await fetch(
    `${BASE_URL}/recommendations/explanation/${user_id}/${destination_id}`,
    {
      headers: {
        "X-Authorization": token,
      },
    }
  );

  if (!response.ok) throw new Error("Failed to fetch explanation");

  return response.json();
};

export const deleteSavedRecommendation = async (
  token: string,
  destination_id: number
) => {
  const response = await fetch(
    `${BASE_URL}/recommendations/save/${destination_id}`,
    {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-Authorization": token,
      },
      body: JSON.stringify({ destination_id }),
    }
  );

  if (!response.ok) throw new Error("Failed to delete saved recommendation");
};

export const fetchSavedRecommendations = async (token: string) => {
  const response = await fetch(`${BASE_URL}/recommendations/saved`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-Authorization": token,
    },
  });

  if (!response.ok) throw new Error("Failed to fetch saved recommendations");

  return response.json(); // should return array of saved recommendations
};

export const preprocessRecommendations = async () => {
  const response = await fetch(`${BASE_URL}/recommendations/preprocess`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) throw new Error("Failed to preprocess recommendations");

  return response.json();
};
