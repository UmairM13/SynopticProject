import { useState, useEffect } from "react";
import {
  Container,
  Row,
  Col,
  Button,
  Form,
  Card,
  ListGroup,
  Alert,
} from "react-bootstrap";
import {
  fetchPastDestinations,
  addPastDestination,
  addPastDestinationToUser,
} from "../api/UserApi";

interface PastDestination {
  id: number;
  destination_name: string;
  trip_start_date: string;
  trip_end_date: string;
  rating: number;
  notes?: string;
}

const UserProfile = () => {
  const [pastDestinations, setPastDestinations] = useState<PastDestination[]>(
    []
  );
  const [newDestination, setNewDestination] = useState({
    destination_name: "",
    trip_start_date: "",
    trip_end_date: "",
    rating: "",
    notes: "",
  });
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const userId = localStorage.getItem("id");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setNewDestination({ ...newDestination, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    setError("");
    setSuccess("");

    try {
      const newEntry = await addPastDestination(userId!, newDestination);
      setPastDestinations([...pastDestinations, newEntry]);

      setSuccess("Destination added!");
      setNewDestination({
        destination_name: "",
        trip_start_date: "",
        trip_end_date: "",
        rating: "",
        notes: "",
      });

      const newEntryForUser = await addPastDestinationToUser(
        userId!,
        newDestination.destination_name
      );
      console.log("New entry added to user:", newEntryForUser);
    } catch (err) {
      setError("An error occurred while adding your destination.");
    }
  };

  useEffect(() => {
    const loadPastDestinations = async () => {
      if (!userId) return;
      try {
        const data = await fetchPastDestinations(userId);
        setPastDestinations(data);
      } catch (e) {
        console.error("Failed to load past destinations");
      }
    };

    loadPastDestinations();
  }, [userId]);

  return (
    <Container className="mt-5">
      <h2 className="text-center mb-4">Your Profile</h2>

      <Row>
        <Col md={6}>
          <Card className="mb-4">
            <Card.Body>
              <Card.Title>Add a Past Destination</Card.Title>
              {success && <Alert variant="success">{success}</Alert>}
              {error && <Alert variant="danger">{error}</Alert>}
              <Form>
                <Form.Group className="mb-2">
                  <Form.Label>Destination Name</Form.Label>
                  <Form.Control
                    type="text"
                    name="destination_name"
                    value={newDestination.destination_name}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-2">
                  <Form.Label>Trip Start Date</Form.Label>
                  <Form.Control
                    type="date"
                    name="trip_start_date"
                    value={newDestination.trip_start_date}
                    onChange={handleChange}
                  />
                </Form.Group>

                <Form.Group className="mb-2">
                  <Form.Label>Trip End Date</Form.Label>
                  <Form.Control
                    type="date"
                    name="trip_end_date"
                    value={newDestination.trip_end_date}
                    onChange={handleChange}
                  />
                </Form.Group>

                <Form.Group className="mb-2">
                  <Form.Label>Rating (0.0 - 5.0)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    min="0"
                    max="5"
                    name="rating"
                    value={newDestination.rating}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Notes</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    name="notes"
                    value={newDestination.notes}
                    onChange={handleChange}
                  />
                </Form.Group>

                <Button className="btn-accent w-100" onClick={handleSubmit}>
                  Add Destination
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card>
            <Card.Body>
              <Card.Title>Previously Visited</Card.Title>
              <ListGroup variant="flush">
                {pastDestinations.map((dest) => (
                  <ListGroup.Item key={dest.id}>
                    <strong>{dest.destination_name}</strong> ({dest.rating}/5)
                    <br />
                    {dest.trip_start_date} – {dest.trip_end_date}
                    {dest.notes && (
                      <p className="mb-0 mt-1 text-muted">{dest.notes}</p>
                    )}
                  </ListGroup.Item>
                ))}
              </ListGroup>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default UserProfile;
