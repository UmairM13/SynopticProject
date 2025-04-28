import { useState } from "react";
import { Container, Form, Button, Row, Col, Alert } from "react-bootstrap";
import { signup } from "../api/UserApi";
import { useNavigate } from "react-router-dom";
import Select from "react-select";
import { countryOptions } from "../assets/countries"; // your country list

const nationalities = [
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
    customCurrentCountry: "",
    age: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const navigate = useNavigate();

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

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

    if (form.currentCountry === "Other" && !form.customCurrentCountry.trim()) {
      setError("Please enter your country.");
      return;
    }

    const payload = {
      email: form.email.trim(),
      password: form.password.trim(),
      age: parseInt(form.age, 10),
      nationality:
        form.nationality === "Other"
          ? form.customNationality.trim()
          : form.nationality,
      current_city: form.currentCity.trim(),
      current_country:
        form.currentCountry === "Other"
          ? form.customCurrentCountry.trim()
          : form.currentCountry,

      // Temporary fields for onboarding
      preferred_climate: "Any",
      preferred_terrain: "Unknown",
      past_destinations: "",
      budget: 1000,
      holiday_type: "Relaxed",
      trip_start_date: null,
      trip_end_date: null,
    };

    try {
      setLoading(true);
      await signup(payload);
      setSuccess("Account created successfully!");
      setTimeout(() => {
        navigate("/login");
      }, 1500);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Error signing up.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="mt-5 mb-5" style={{ maxWidth: "700px" }}>
      <h2 className="mb-4 text-center">Create Your Account</h2>
      <Form onSubmit={handleSubmit}>
        {error && <Alert variant="danger">{error}</Alert>}
        {success && <Alert variant="success">{success}</Alert>}

        {/* Email + Age */}
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

        {/* Password + Confirm Password */}
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

        {/* Nationality + Current City */}
        <Row className="mb-3">
          <Col md={6}>
            <Form.Label>Nationality</Form.Label>
            <Form.Select
              name="nationality"
              value={form.nationality}
              onChange={handleChange}
              required
              style={{ color: form.nationality ? "#212529" : "#6c757d" }}
            >
              <option value="">Select your nationality...</option>
              {nationalities.map((nat) => (
                <option key={nat} value={nat}>
                  {nat}
                </option>
              ))}
            </Form.Select>

            {form.nationality === "Other" && (
              <Form.Control
                className="mt-2"
                type="text"
                name="customNationality"
                placeholder="Enter your nationality"
                value={form.customNationality}
                onChange={handleChange}
                required
              />
            )}
          </Col>

          <Col md={6}>
            <Form.Label>Current City</Form.Label>
            <Form.Control
              type="text"
              name="currentCity"
              value={form.currentCity}
              onChange={handleChange}
              required
            />
          </Col>
        </Row>

        {/* Current Country */}
        <Row className="mb-4">
          <Col md={12}>
            <Form.Label>Current Country</Form.Label>
            <Select
              options={[...countryOptions, { label: "Other", value: "Other" }]}
              value={
                countryOptions.find((c) => c.value === form.currentCountry) ||
                null
              }
              onChange={(selected) =>
                setForm({
                  ...form,
                  currentCountry: selected?.value || "",
                  customCurrentCountry: "",
                })
              }
              placeholder="Select your country..."
              isSearchable
              styles={{
                control: (provided, state) => ({
                  ...provided,
                  backgroundColor: "#fff",
                  borderColor: "#ced4da",
                  minHeight: "38px",
                  height: "38px",
                  boxShadow: state.isFocused
                    ? "0 0 0 0.2rem rgba(0,123,255,.25)"
                    : "none",
                  "&:hover": {
                    borderColor: "#86b7fe",
                  },
                }),
                valueContainer: (provided) => ({
                  ...provided,
                  height: "38px",
                  padding: "0 8px",
                }),
                input: (provided) => ({
                  ...provided,
                  margin: "0px",
                }),
                indicatorSeparator: () => ({
                  display: "none",
                }),
                indicatorsContainer: (provided) => ({
                  ...provided,
                  height: "38px",
                }),
                menu: (provided) => ({
                  ...provided,
                  zIndex: 9999,
                }),
              }}
            />

            {form.currentCountry === "Other" && (
              <Form.Control
                className="mt-2"
                type="text"
                placeholder="Enter your country"
                value={form.customCurrentCountry}
                onChange={(e) =>
                  setForm({ ...form, customCurrentCountry: e.target.value })
                }
                required
              />
            )}
          </Col>
        </Row>

        {/* Submit Button */}
        <div className="d-grid">
          <Button
            className="btn-accent"
            type="submit"
            size="lg"
            disabled={loading}
          >
            {loading ? "Creating..." : "Create Account"}
          </Button>
        </div>
      </Form>
    </Container>
  );
};

export default Register;
