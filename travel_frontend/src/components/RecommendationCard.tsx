import { Card, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

interface RecommendationCardProps {
  destinationId: number;
  destinationName: string;
  country: string;
  isOffSeason: boolean;
  budget: number;
  onSave?: () => void;
  onExplain?: () => void;
  isSaved?: boolean;
}

const RecommendationCard = ({
  destinationId,
  destinationName,
  country,
  isOffSeason,
  budget,
  onSave,
  onExplain,
  isSaved,
}: RecommendationCardProps) => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate(`/destination/${destinationId}`);
  };

  return (
    <Card
      className="mb-4 shadow-sm hover-shadow"
      onClick={handleCardClick}
      style={{ cursor: "pointer" }}
    >
      <Card.Body>
        <Card.Title>
          {destinationName}, {country}
        </Card.Title>
        <Card.Text>
          <strong>Estimated Daily Budget:</strong> £{budget.toFixed(2)} <br />
          <strong>Off-season:</strong> {isOffSeason ? "Yes" : "No"}
        </Card.Text>

        <div className="d-flex justify-content-between">
          <Button
            variant="outline-primary"
            onClick={(e) => {
              e.stopPropagation();
              onExplain?.();
            }}
          >
            Why this?
          </Button>

          {/* Save / Unsave Button */}
          <Button
            variant={isSaved ? "success" : "outline-primary"}
            onClick={(e) => {
              e.stopPropagation();
              onSave?.(); // Save OR Unsave
            }}
          >
            {isSaved ? "Saved ✓" : "Save"}
          </Button>
        </div>
      </Card.Body>
    </Card>
  );
};

export default RecommendationCard;
