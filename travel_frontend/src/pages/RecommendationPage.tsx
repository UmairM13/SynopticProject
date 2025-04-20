import { useEffect, useState } from "react";
import { Container, Row, Col, Spinner, Alert } from "react-bootstrap";
import RecommendationCard from "../components/RecommendationCard";
import ExplanationModal from "../components/ExplanationModal";

import {
  fetchRecommendations,
  saveRecommendation,
  fetchExplanation,
} from "../api/recommendationApi";

interface Recommendation {
  id: number;
  destination_name: string;
  country: string;
  avg_daily_budget: number;
  is_off_season: string;
}

const RecommendationPage = () => {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [explanationText, setExplanationText] = useState("");
  const [selectedDestination, setSelectedDestination] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const token = localStorage.getItem("token") || "";
        const data = await fetchRecommendations(token);
        setRecommendations(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const handleSave = async (rec: Recommendation) => {
    try {
      await saveRecommendation(
        localStorage.getItem("token") || "",
        rec.id,
        rec.destination_name
      );
      alert("Saved!");
    } catch (err) {
      console.error("Save failed:", err);
    }
  };

  const handleExplain = async (rec: Recommendation) => {
    try {
      const data = await fetchExplanation(
        localStorage.getItem("token") || "",
        rec.id
      );
      setExplanationText(data.explanation || "No explanation available.");
      setSelectedDestination(rec.destination_name);
      setShowModal(true);
    } catch (err) {
      setExplanationText("Failed to fetch explanation.");
      setSelectedDestination(rec.destination_name);
      setShowModal(true);
    }
  };
  return (
    <Container className="mt-5 mb-5">
      <h2 className="mb-4 text-center">Your Travel Recommendations</h2>

      {loading ? (
        <div className="text-center">
          <Spinner animation="border" />
        </div>
      ) : error ? (
        <Alert variant="danger">{error}</Alert>
      ) : recommendations.length === 0 ? (
        <Alert variant="info">No recommendations found.</Alert>
      ) : (
        <Row>
          {recommendations.map((rec) => (
            <Col md={4} key={rec.id}>
              <RecommendationCard
                destinationName={rec.destination_name}
                country={rec.country}
                budget={rec.avg_daily_budget}
                isOffSeason={rec.is_off_season === "Yes"}
                onSave={() => handleSave(rec)}
                onExplain={() => handleExplain(rec)}
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
    </Container>
  );
};

export default RecommendationPage;
