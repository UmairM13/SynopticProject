import { Card, Button } from "react-bootstrap";

interface RecommendationCardProps {
  destinationName: string;
  country: string;
  isOffSeason: boolean;
  budget: number;
  onSave?: () => void;
  onExplain?: () => void;
}

const RecommendationCard = ({
  destinationName,
  country,
  isOffSeason,
  budget,
  onSave,
  onExplain,
}: RecommendationCardProps) => {
  return (
    <Card className="mb-4 shadow-sm">
      <Card.Body>
        <Card.Title>{destinationName}</Card.Title>
        <Card.Subtitle className="mb-2 text-muted">{country}</Card.Subtitle>
        <Card.Text>
          <strong>Budget:</strong> £{budget} <br />
          <strong>Off-season:</strong> {isOffSeason ? "Yes" : "No"}
        </Card.Text>
        <div className="d-flex justify-content-between">
          <Button variant="outline-primary" onClick={onExplain}>
            Why this?
          </Button>
          <Button variant="success" onClick={onSave}>
            Save
          </Button>
        </div>
      </Card.Body>
    </Card>
  );
};

export default RecommendationCard;
