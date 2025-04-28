import { useEffect, useState } from "react";
import { Container, Row, Col, Spinner, Alert, Form } from "react-bootstrap";
import RecommendationCard from "../components/RecommendationCard";
import ExplanationModal from "../components/ExplanationModal";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import {
  fetchRecommendations,
  saveRecommendation,
  fetchSavedRecommendations,
  deleteSavedRecommendation,
  fetchExplanation,
} from "../api/RecommendationApi";
import { getUserById } from "../api/UserApi";

interface Recommendation {
  id: number;
  name: string;
  country: string;
  avg_daily_budget: number;
  is_off_season: string;
}

const RecommendationPage = () => {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [filteredRecommendations, setFilteredRecommendations] = useState<
    Recommendation[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [explanationText, setExplanationText] = useState("");
  const [selectedDestination, setSelectedDestination] = useState("");
  const [savedDestinations, setSavedDestinations] = useState<number[]>([]);
  const [pastDestinations, setPastDestinations] = useState<string[]>([]);

  // Filters
  const [hidePastDestinations, setHidePastDestinations] = useState(false);
  const [hideSameCountry, setHideSameCountry] = useState(false);
  const [onlyOffSeason, setOnlyOffSeason] = useState(false);
  const [userCurrentCountry, setUserCurrentCountry] = useState<string>("");

  useEffect(() => {
    const load = async () => {
      try {
        const token = localStorage.getItem("session_token") || "";
        const userId = localStorage.getItem("id") || "";

        const [recs, saved, userData] = await Promise.all([
          fetchRecommendations(token, userId),
          fetchSavedRecommendations(token),
          getUserById(userId),
        ]);

        setRecommendations(recs);
        setSavedDestinations(saved.map((rec: any) => rec.destination_id));
        setUserCurrentCountry(userData.current_country?.trim() || "");

        const pastDestArray =
          userData.past_destinations &&
          typeof userData.past_destinations === "string"
            ? userData.past_destinations.split(",").map((d: string) => d.trim())
            : [];
        setPastDestinations(pastDestArray);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [
    recommendations,
    hidePastDestinations,
    hideSameCountry,
    onlyOffSeason,
    pastDestinations,
  ]);

  const applyFilters = () => {
    let recs = [...recommendations];

    if (hidePastDestinations) {
      recs = recs.filter((rec) => !pastDestinations.includes(rec.name));
    }

    if (hideSameCountry && userCurrentCountry) {
      recs = recs.filter((rec) => rec.country !== userCurrentCountry);
    }

    if (onlyOffSeason) {
      recs = recs.filter((rec) => rec.is_off_season === "Yes");
    }

    setFilteredRecommendations(recs.slice(0, 12)); // Always show up to 12
  };

  const handleSave = async (rec: Recommendation) => {
    const token = localStorage.getItem("session_token") || "";
    try {
      if (savedDestinations.includes(rec.id)) {
        await deleteSavedRecommendation(token, rec.id);
        setSavedDestinations((prev) => prev.filter((id) => id !== rec.id));
        toast.info(`Removed ${rec.name} from saved!`);
      } else {
        await saveRecommendation(token, rec.id, rec.name);
        setSavedDestinations((prev) => [...prev, rec.id]);
        toast.success(`Saved ${rec.name}! 🎉`);
      }
    } catch (err) {
      console.error("Save/Delete failed:", err);
      toast.error("Something went wrong.");
    }
  };

  const handleExplain = async (rec: Recommendation) => {
    const userId = localStorage.getItem("id") || "";
    try {
      const data = await fetchExplanation(
        localStorage.getItem("session_token") || "",
        userId,
        rec.id
      );
      setExplanationText(data.explanation || "No explanation available.");
      setSelectedDestination(rec.name);
      setShowModal(true);
    } catch (err) {
      setExplanationText("Failed to fetch explanation.");
      setSelectedDestination(rec.name);
      setShowModal(true);
    }
  };

  return (
    <Container className="mt-5 mb-5">
      <h2 className="mb-4 text-center">Your Travel Recommendations</h2>

      {/* Filters */}
      <div className="d-flex justify-content-center mb-4 gap-4 flex-wrap">
        <Form.Check
          type="switch"
          id="hide-past-switch"
          label="Hide Past Destinations"
          checked={hidePastDestinations}
          onChange={() => setHidePastDestinations(!hidePastDestinations)}
        />
        <Form.Check
          type="switch"
          id="hide-country-switch"
          label="Hide Same Country"
          checked={hideSameCountry}
          onChange={() => setHideSameCountry(!hideSameCountry)}
        />
        <Form.Check
          type="switch"
          id="off-season-switch"
          label="Show Only Off-Season"
          checked={onlyOffSeason}
          onChange={() => setOnlyOffSeason(!onlyOffSeason)}
        />
      </div>

      {loading ? (
        <div className="text-center">
          <Spinner animation="border" />
        </div>
      ) : error ? (
        <Alert variant="danger">{error}</Alert>
      ) : filteredRecommendations.length === 0 ? (
        <Alert variant="info">No recommendations match your filters.</Alert>
      ) : (
        <Row>
          {filteredRecommendations.map((rec) => (
            <Col md={4} key={rec.id}>
              <RecommendationCard
                destinationId={rec.id}
                destinationName={rec.name}
                country={rec.country}
                budget={rec.avg_daily_budget}
                isOffSeason={rec.is_off_season === "Yes"}
                onSave={() => handleSave(rec)}
                onExplain={() => handleExplain(rec)}
                isSaved={savedDestinations.includes(rec.id)}
              />
            </Col>
          ))}
        </Row>
      )}

      <ExplanationModal
        show={showModal}
        onHide={() => setShowModal(false)}
        destinationName={selectedDestination}
        explanation={explanationText}
      />

      <ToastContainer position="bottom-center" autoClose={2000} />
    </Container>
  );
};

export default RecommendationPage;
