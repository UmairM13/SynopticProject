import { Container, Row, Col, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate("/register");
  };

  return (
    <div
      style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}
    >
      {/* Hero Section */}
      <div
        style={{
          background:
            "linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          color: "white",
          padding: "100px 20px",
          textAlign: "center",
        }}
      >
        <h1 className="mb-3">Discover Your Perfect Escape</h1>
        <p className="mb-4">
          Travel smarter, save more, and explore destinations at their best —
          all tailored just for you.
        </p>
        <Button size="lg" variant="primary" onClick={handleGetStarted}>
          Get Started
        </Button>
      </div>

      {/* Features Section */}
      <Container className="text-center mt-5 mb-5">
        <Row className="g-4">
          <Col md={4}>
            <h4>Personalized Destinations</h4>
            <p>
              Recommendations based on your travel style, preferences, and
              budget.
            </p>
          </Col>
          <Col md={4}>
            <h4>Off-Season Focus</h4>
            <p>
              Find hidden gems when they're most affordable and less crowded.
            </p>
          </Col>
          <Col md={4}>
            <h4>Save and Plan</h4>
            <p>
              Save your favorite destinations and plan future adventures easily.
            </p>
          </Col>
        </Row>
      </Container>

      {/* Footer */}
      <footer className="text-center text-muted mt-auto py-3">
        © 2025 TravelMate &mdash; Travel Smarter. Travel Better.
      </footer>
    </div>
  );
};

export default HomePage;
