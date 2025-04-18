import { useState } from "react";
import { Container, Form, Button, Row, Col, Alert } from "react-bootstrap";

const countries = [
  "British",
  "American",
  "Canadian",
  "German",
  "French",
  "Spanish",
  "Chinese",
  "Italian",
  "Indian",
  "Australian",
  "South African",
  "Other",
];

const Register = () => {
  const [form, setForm] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    nationality: "",
    customNationality: "",
    currentCity: "",
    currentCountry: "",
    age: "",
  });

  const [error, setError] = useState("");

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    if (parseInt(form.age) < 1) {
      setError("Age must be a positive number.");
      return;
    }

    if (form.nationality === "Other" && !form.customNationality.trim()) {
      setError("Please enter your nationality.");
      return;
    }

    setError("");

    const payload = {
      ...form,
      nationality:
        form.nationality === "Other"
          ? form.customNationality.trim()
          : form.nationality,
      email: form.email.trim(),
      currentCity: form.currentCity.trim(),
      currentCountry: form.currentCountry.trim(),
      age: parseInt(form.age, 10),
    };

    console.log("Submitted:", payload);
    // TODO: send payload to backend
  };

  return (
    <Container className="mt-5 mb-5" style={{ maxWidth: "700px" }}>
      <h2 className="mb-4 text-center">Create Your Account</h2>
      <Form onSubmit={handleSubmit}>
        {error && <Alert variant="danger">{error}</Alert>}

        <Row className="mb-3">
          <Col md={6}>
            <Form.Label>Email</Form.Label>
            <Form.Control
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
            />
          </Col>
          <Col md={6}>
            <Form.Label>Age</Form.Label>
            <Form.Control
              type="number"
              name="age"
              value={form.age}
              onChange={handleChange}
              min="1"
              required
            />
          </Col>
        </Row>

        <Row className="mb-3">
          <Col md={6}>
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              required
            />
          </Col>
          <Col md={6}>
            <Form.Label>Confirm Password</Form.Label>
            <Form.Control
              type="password"
              name="confirmPassword"
              value={form.confirmPassword}
              onChange={handleChange}
              required
            />
          </Col>
        </Row>

        <Row className="mb-3">
          <Col md={6}>
            <Form.Label id="nationality-label" htmlFor="nationality">
              Nationality
            </Form.Label>
            <Form.Select
              id="nationality"
              name="nationality"
              aria-labelledby="nationality-label"
              value={form.nationality}
              onChange={handleChange}
              required
            >
              <option value="">Select your nationality</option>
              {countries.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </Form.Select>

            {form.nationality === "Other" && (
              <>
                <Form.Label className="mt-2" htmlFor="customNationality">
                  Your Nationality
                </Form.Label>
                <Form.Control
                  id="customNationality"
                  type="text"
                  placeholder="Enter your nationality"
                  name="customNationality"
                  value={form.customNationality}
                  onChange={handleChange}
                  required
                />
              </>
            )}
          </Col>
          <Col md={6}>
            <Form.Label>Current City</Form.Label>
            <Form.Control
              type="text"
              name="currentCity"
              value={form.currentCity}
              onChange={handleChange}
            />
          </Col>
        </Row>

        <Row className="mb-4">
          <Col md={6}>
            <Form.Label>Current Country</Form.Label>
            <Form.Control
              type="text"
              name="currentCountry"
              value={form.currentCountry}
              onChange={handleChange}
            />
          </Col>
        </Row>

        <div className="d-grid">
          <Button className="btn-accent" type="submit" size="lg">
            Create Account
          </Button>
        </div>
      </Form>
    </Container>
  );
};

export default Register;
