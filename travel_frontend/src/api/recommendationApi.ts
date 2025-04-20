const BASE_URL = "http://localhost:8000/travel/api";

export const fetchRecommendations = async (token: string) => {
  const response = await fetch(`${BASE_URL}/recommendations`, {
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
  destination_id: number
) => {
  const response = await fetch(
    `${BASE_URL}/recommendations/explain/${destination_id}`,
    {
      headers: {
        "X-Authorization": token,
      },
    }
  );

  if (!response.ok) throw new Error("Failed to fetch explanation");

  return response.json();
};
