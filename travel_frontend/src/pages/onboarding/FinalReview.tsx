import { Container, Button, ListGroup } from "react-bootstrap";

interface FinalReviewProps {
  userData: {
    email: string;
    age: string;
    nationality: string;
    currentCity: string;
    currentCountry: string;
    preferredTerrains: string[];
    preferredClimates: string[];
    holidayType: string;
    budget: string | null;
    tripStartDate: string | null;
    tripEndDate: string | null;
  };
  onEdit: (section: string) => void;
  onSubmit: () => void;
}

const FinalReview = ({ userData, onEdit, onSubmit }: FinalReviewProps) => {
  return (
    <Container className="mt-5" style={{ maxWidth: "700px" }}>
      <h2 className="mb-4 text-center">Review Your Preferences</h2>

      <ListGroup>
        <ListGroup.Item>
          <strong>Email:</strong> {userData.email}
        </ListGroup.Item>
        <ListGroup.Item>
          <strong>Age:</strong> {userData.age}
        </ListGroup.Item>
        <ListGroup.Item>
          <strong>Nationality:</strong> {userData.nationality}
        </ListGroup.Item>
        <ListGroup.Item>
          <strong>Current Location:</strong> {userData.currentCity},{" "}
          {userData.currentCountry}
        </ListGroup.Item>
        <ListGroup.Item>
          <strong>Preferred Terrains:</strong>{" "}
          {userData.preferredTerrains.join(", ")}
        </ListGroup.Item>
        <ListGroup.Item>
          <strong>Preferred Climates:</strong>{" "}
          {userData.preferredClimates.join(", ")}
        </ListGroup.Item>
        <ListGroup.Item>
          <strong>Holiday Type:</strong> {userData.holidayType}
        </ListGroup.Item>
        <ListGroup.Item>
          <strong>Budget:</strong>{" "}
          {userData.budget ? `£${userData.budget}` : "Not Provided"}
        </ListGroup.Item>
        <ListGroup.Item>
          <strong>Travel Dates:</strong>{" "}
          {userData.tripStartDate && userData.tripEndDate
            ? `${userData.tripStartDate} to ${userData.tripEndDate}`
            : "Not Provided"}
        </ListGroup.Item>
      </ListGroup>

      <div className="d-flex justify-content-between mt-4">
        <Button variant="secondary" onClick={() => onEdit("all")}>
          Edit Details
        </Button>
        <Button className="btn-accent" onClick={onSubmit}>
          Confirm & Finish
        </Button>
      </div>
    </Container>
  );
};

export default FinalReview;
