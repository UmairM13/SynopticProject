import React, { useEffect, useState } from "react";
import { Row, Col, Container, Spinner } from "react-bootstrap";
import { fetchPopularDestinations, searchDestinations } from "../api/searchApi";
import { getDestinationById } from "../api/DestinationApi";
import RecommendationCard from "../components/RecommendationCard";
import {
  saveRecommendation,
  deleteSavedRecommendation,
  fetchSavedRecommendations,
} from "../api/RecommendationApi";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

interface Destination {
  id: number;
  name: string;
  country?: string;
  avg_daily_budget?: number;
  is_off_season?: string;
  off_season_start?: string;
  off_season_end?: string;
}

const isCurrentlyOffSeason = (destination: Destination) => {
  if (!destination.off_season_start || !destination.off_season_end) {
    return false;
  }

  const currentMonth = new Date().toLocaleString("default", { month: "long" });

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  const startIndex = months.indexOf(destination.off_season_start);
  const endIndex = months.indexOf(destination.off_season_end);
  const currentIndex = months.indexOf(currentMonth);

  if (startIndex === -1 || endIndex === -1 || currentIndex === -1) {
    return false;
  }

  if (startIndex <= endIndex) {
    return currentIndex >= startIndex && currentIndex <= endIndex;
  } else {
    return currentIndex >= startIndex || currentIndex <= endIndex;
  }
};

const SearchPage = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Destination[]>([]);
  const [popularDestinations, setPopularDestinations] = useState<Destination[]>(
    []
  );
  const [loading, setLoading] = useState(true);
  const [isSearching, setIsSearching] = useState(false);
  const [savedDestinations, setSavedDestinations] = useState<number[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const initialize = async () => {
      const token = localStorage.getItem("session_token");
      if (token) {
        setIsLoggedIn(true);
        try {
          const saved = await fetchSavedRecommendations(token);
          setSavedDestinations(saved.map((rec: any) => rec.destination_id));
        } catch (err) {
          console.error("Failed to fetch saved destinations:", err);
        }
      } else {
        setIsLoggedIn(false);
      }

      await loadPopular();
    };

    initialize();
  }, []);

  const loadPopular = async () => {
    setLoading(true);
    try {
      const popularBasic = await fetchPopularDestinations();
      const fullDetailsPromises = popularBasic.map((dest: any) =>
        getDestinationById(dest.id)
      );
      const fullDetails = await Promise.all(fullDetailsPromises);

      setPopularDestinations(fullDetails);
      setResults(fullDetails);
    } catch (error) {
      console.error("Failed to load popular destinations", error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!query.trim()) {
      setIsSearching(false);
      loadPopular();
      return;
    }

    setLoading(true);
    setIsSearching(true);
    try {
      const searchBasic = await searchDestinations(query);
      const fullDetailsPromises = searchBasic.map((dest: any) =>
        getDestinationById(dest.id)
      );
      const fullDetails = await Promise.all(fullDetailsPromises);

      setResults(fullDetails);
    } catch (error) {
      console.error("Search failed", error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (destination: Destination) => {
    const token = localStorage.getItem("session_token") || "";
    if (!token) {
      toast.error("Please login to save destinations.");
      return;
    }

    try {
      if (savedDestinations.includes(destination.id)) {
        await deleteSavedRecommendation(token, destination.id);
        setSavedDestinations((prev) =>
          prev.filter((id) => id !== destination.id)
        );
        toast.info(`Removed ${destination.name} from saved!`);
      } else {
        await saveRecommendation(token, destination.id, destination.name);
        setSavedDestinations((prev) => [...prev, destination.id]);
        toast.success(`Saved ${destination.name}! 🎉`);
      }
    } catch (err) {
      console.error("Save/Delete failed:", err);
      toast.error("Something went wrong.");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-500 to-indigo-600 py-20">
        <div className="text-center max-w-3xl mx-auto px-6">
          <h1
            className="text-5xl font-extrabold mb-4"
            style={{ color: "#111827" }}
          >
            Find Your Next Adventure
          </h1>
          <p className="text-lg text-blue-100 mb-8">
            Search and explore destinations around the world 🌍
          </p>

          <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Where do you want to go?"
              className="w-full sm:w-96 p-3 rounded-xl shadow-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-white"
            />
            <button
              onClick={handleSearch}
              className="bg-white text-blue-600 font-semibold py-3 px-6 rounded-xl shadow-md hover:bg-gray-100 transition"
            >
              Search
            </button>
          </div>
        </div>
      </section>

      {/* Featured Destinations */}
      {!isSearching && (
        <section className="py-16 bg-gray-50">
          <Container>
            <h2 className="text-3xl font-bold text-gray-800 mb-10 text-center">
              🌟 Featured Destinations
            </h2>
            <Row className="g-4">
              {popularDestinations.map((destination) => (
                <Col md={4} key={destination.id}>
                  <RecommendationCard
                    destinationId={destination.id}
                    destinationName={destination.name}
                    country={destination.country ?? "Unknown"}
                    budget={destination.avg_daily_budget ?? 0}
                    isOffSeason={isCurrentlyOffSeason(destination)}
                    onSave={
                      isLoggedIn ? () => handleSave(destination) : undefined
                    }
                    isSaved={savedDestinations.includes(destination.id)}
                    hideExplainButton={true}
                  />
                </Col>
              ))}
            </Row>
          </Container>
        </section>
      )}

      {/* Search Results */}
      {isSearching && (
        <section className="py-16">
          <Container>
            <h2 className="text-3xl font-bold text-gray-800 mb-10 text-center">
              🔎 Search Results
            </h2>

            {loading ? (
              <div className="text-center">
                <Spinner animation="border" />
              </div>
            ) : results.length > 0 ? (
              <Row className="g-4">
                {results.map((destination) => (
                  <Col md={4} key={destination.id}>
                    <RecommendationCard
                      destinationId={destination.id}
                      destinationName={destination.name}
                      country={destination.country ?? "Unknown"}
                      budget={destination.avg_daily_budget ?? 0}
                      isOffSeason={isCurrentlyOffSeason(destination)}
                      onSave={
                        isLoggedIn ? () => handleSave(destination) : undefined
                      }
                      isSaved={savedDestinations.includes(destination.id)}
                      hideExplainButton={true}
                    />
                  </Col>
                ))}
              </Row>
            ) : (
              <div className="text-center">
                <p className="text-gray-400 text-lg">
                  No destinations found. Try a different search.
                </p>
              </div>
            )}
          </Container>
        </section>
      )}

      <ToastContainer position="bottom-center" autoClose={2000} />
    </div>
  );
};

export default SearchPage;
