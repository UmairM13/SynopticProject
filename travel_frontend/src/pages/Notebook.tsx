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
  Modal,
  Dropdown,
} from "react-bootstrap";
import {
  fetchPastDestinations,
  addPastDestination,
  addPastDestinationToUser,
  updatePastDestination,
  deletePastDestination,
} from "../api/UserApi";
import {
  fetchSavedRecommendations,
  deleteSavedRecommendation,
} from "../api/RecommendationApi";

interface PastDestination {
  id: number;
  destination_name: string;
  trip_start_date: string | null;
  trip_end_date: string | null;
  rating: string;
  notes?: string | null;
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
  const [editDestination, setEditDestination] =
    useState<PastDestination | null>(null);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [savedRecommendations, setSavedRecommendations] = useState<any[]>([]);
  const [showAllSaved, setShowAllSaved] = useState(false);
  const [showAllPast, setShowAllPast] = useState(false);

  const userId = localStorage.getItem("id");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setNewDestination({ ...newDestination, [e.target.name]: e.target.value });
  };

  const handleModalChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    if (!editDestination) return;
    setEditDestination({ ...editDestination, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    setError("");
    setSuccess("");

    const cleaned = {
      destination_name: newDestination.destination_name,
      trip_start_date: newDestination.trip_start_date.trim() || null,
      trip_end_date: newDestination.trip_end_date.trim() || null,
      rating: newDestination.rating,
      notes: newDestination.notes.trim() || null,
    };

    try {
      const newEntry = await addPastDestination(userId!, cleaned);
      setPastDestinations([...pastDestinations, newEntry]);
      setSuccess("Destination added!");
      setNewDestination({
        destination_name: "",
        trip_start_date: "",
        trip_end_date: "",
        rating: "",
        notes: "",
      });
      await addPastDestinationToUser(userId!, cleaned.destination_name);
    } catch {
      setError("An error occurred while adding your destination.");
    }
  };

  const handleEdit = (destination: PastDestination) => {
    setEditDestination(destination);
    setShowModal(true);
  };

  const handleUpdate = async () => {
    if (!editDestination || !userId) return;
    try {
      const payload = {
        destination_name: editDestination.destination_name,
        trip_start_date: editDestination.trip_start_date?.trim() || null,
        trip_end_date: editDestination.trip_end_date?.trim() || null,
        rating: editDestination.rating,
        notes: editDestination.notes?.trim() || null,
      };

      await updatePastDestination(userId, editDestination.id, payload);
      setPastDestinations((prev) =>
        prev.map((d) =>
          d.id === editDestination.id ? { ...d, ...payload } : d
        )
      );
      await addPastDestinationToUser(userId, payload.destination_name);
      setShowModal(false);
      setSuccess("Destination updated!");
    } catch {
      setError("Failed to update destination.");
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deletePastDestination(userId!, id);
      setPastDestinations(pastDestinations.filter((dest) => dest.id !== id));
      setSuccess("Destination deleted!");
    } catch {
      setError("An error occurred while deleting the destination.");
    }
  };

  useEffect(() => {
    const loadData = async () => {
      if (!userId) return;
      try {
        const past = await fetchPastDestinations(userId);
        setPastDestinations(past);

        const saved = await fetchSavedRecommendations(
          localStorage.getItem("session_token") || ""
        );
        setSavedRecommendations(saved);
      } catch {
        console.error("Failed to load profile data");
      }
    };
    loadData();
  }, [userId]);

  return (
    <Container className="mt-5">
      <h2 className="text-center mb-4">Your Profile</h2>
      <Row>
        <Col md={6}>
          {/* Saved Recommendations */}
          <Card className="mb-4 fade-in">
            <Card.Body>
              <Card.Title>Saved Recommendations</Card.Title>
              <ListGroup variant="flush">
                {savedRecommendations.length === 0 ? (
                  <ListGroup.Item className="text-muted">
                    No saved recommendations.
                  </ListGroup.Item>
                ) : (
                  (showAllSaved
                    ? savedRecommendations
                    : savedRecommendations.slice(0, 5)
                  ).map((rec) => (
                    <ListGroup.Item
                      key={rec.destination_id}
                      className="d-flex justify-content-between align-items-start"
                    >
                      <div
                        style={{ cursor: "pointer" }}
                        onClick={() =>
                          (window.location.href = `/destination/${rec.destination_id}`)
                        }
                      >
                        <strong>{rec.destination}</strong>
                        <br />
                        <small className="text-muted">
                          Saved on{" "}
                          {new Date(rec.timestamp).toLocaleDateString()}
                        </small>
                      </div>
                      <Button
                        variant="outline-danger"
                        size="sm"
                        onClick={async (e) => {
                          e.stopPropagation();
                          try {
                            await deleteSavedRecommendation(
                              localStorage.getItem("session_token") || "",
                              rec.destination_id
                            );
                            setSavedRecommendations((prev) =>
                              prev.filter(
                                (r) => r.destination_id !== rec.destination_id
                              )
                            );
                          } catch (err) {
                            console.error(
                              "Failed to unsave recommendation",
                              err
                            );
                          }
                        }}
                      >
                        Unsave
                      </Button>
                    </ListGroup.Item>
                  ))
                )}
              </ListGroup>
              {savedRecommendations.length > 5 && (
                <Button
                  variant="link"
                  className="mt-2 p-0"
                  onClick={() => setShowAllSaved(!showAllSaved)}
                >
                  {showAllSaved ? "Show Less" : "Show More"}
                </Button>
              )}
            </Card.Body>
          </Card>

          {/* Past Destinations */}
          <Card className="fade-in">
            <Card.Body>
              <Card.Title>Previously Visited</Card.Title>
              <ListGroup variant="flush">
                {(showAllPast
                  ? [...pastDestinations]
                  : [...pastDestinations].slice(0, 5)
                )
                  .sort((a, b) => {
                    const dateA = a.trip_end_date || a.trip_start_date;
                    const dateB = b.trip_end_date || b.trip_start_date;
                    if (!dateA && !dateB) return 0;
                    if (!dateA) return 1;
                    if (!dateB) return -1;
                    return (
                      new Date(dateB).getTime() - new Date(dateA).getTime()
                    );
                  })
                  .map((dest) => (
                    <ListGroup.Item
                      key={dest.id}
                      className="d-flex justify-content-between align-items-start"
                    >
                      <div>
                        <strong>{dest.destination_name}</strong> ({dest.rating}
                        /5)
                        <br />
                        {dest.trip_start_date} – {dest.trip_end_date}
                        {dest.notes && (
                          <p className="mb-0 mt-1 text-muted">{dest.notes}</p>
                        )}
                      </div>
                      <Dropdown align="end">
                        <Dropdown.Toggle
                          variant="light"
                          size="sm"
                          className="border-0"
                        >
                          <i className="bi bi-three-dots-vertical"></i>
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                          <Dropdown.Item onClick={() => handleEdit(dest)}>
                            Edit
                          </Dropdown.Item>
                          <Dropdown.Item
                            onClick={() => handleDelete(dest.id)}
                            className="text-danger"
                          >
                            Delete
                          </Dropdown.Item>
                        </Dropdown.Menu>
                      </Dropdown>
                    </ListGroup.Item>
                  ))}
              </ListGroup>
              {pastDestinations.length > 5 && (
                <Button
                  variant="link"
                  className="mt-2 p-0"
                  onClick={() => setShowAllPast(!showAllPast)}
                >
                  {showAllPast ? "Show Less" : "Show More"}
                </Button>
              )}
            </Card.Body>
          </Card>
        </Col>

        {/* Form to Add Destination */}
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
                  <Form.Label>Rating</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    name="rating"
                    value={newDestination.rating}
                    onChange={handleChange}
                  />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Notes</Form.Label>
                  <Form.Control
                    as="textarea"
                    name="notes"
                    rows={3}
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
      </Row>

      {/* Edit Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Edit Destination</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {editDestination && (
            <Form>
              <Form.Group className="mb-2">
                <Form.Label>Destination Name</Form.Label>
                <Form.Control
                  type="text"
                  name="destination_name"
                  value={editDestination.destination_name}
                  onChange={handleModalChange}
                />
              </Form.Group>
              <Form.Group className="mb-2">
                <Form.Label>Trip Start Date</Form.Label>
                <Form.Control
                  type="date"
                  name="trip_start_date"
                  value={editDestination.trip_start_date || ""}
                  onChange={handleModalChange}
                />
              </Form.Group>
              <Form.Group className="mb-2">
                <Form.Label>Trip End Date</Form.Label>
                <Form.Control
                  type="date"
                  name="trip_end_date"
                  value={editDestination.trip_end_date || ""}
                  onChange={handleModalChange}
                />
              </Form.Group>
              <Form.Group className="mb-2">
                <Form.Label>Rating</Form.Label>
                <Form.Control
                  type="number"
                  name="rating"
                  step="0.1"
                  min="0"
                  max="5"
                  value={editDestination.rating}
                  onChange={handleModalChange}
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Notes</Form.Label>
                <Form.Control
                  as="textarea"
                  name="notes"
                  rows={3}
                  value={editDestination.notes || ""}
                  onChange={handleModalChange}
                />
              </Form.Group>
              <Button onClick={handleUpdate} className="w-100">
                Save Changes
              </Button>
            </Form>
          )}
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default UserProfile;
