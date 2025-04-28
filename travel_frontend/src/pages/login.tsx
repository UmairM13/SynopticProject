import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/UserApi";
import { Container, Form, Button, Alert } from "react-bootstrap";
import { useAuth } from "../context/AuthContext";
import { preprocessRecommendations } from "../api/RecommendationApi";

const Login: React.FC = () => {
  const [email, setEmail] = useState<string>(""); // Changed to email for consistency
  const [password, setPassword] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const auth = useAuth();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const userData = { email, password };
      await login(userData);

      const user_id = localStorage.getItem("id");
      if (!user_id) {
        throw new Error("User ID not found in local storage");
      }

      auth.login(email, parseInt(user_id));
      await preprocessRecommendations(); // Preprocess recommendations after login
      const onboarded = localStorage.getItem("has_onboarded") === "true";
      navigate(onboarded ? "/recommendations" : "/onboarding");
    } catch (error: any) {
      setError(error.message || "Invalid credentials");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="mt-5 mb-5" style={{ maxWidth: "500px" }}>
      <h2 className="text-center mb-4">Login to Your Account</h2>
      <Form onSubmit={handleLogin}>
        {error && <Alert variant="danger">{error}</Alert>}

        <Form.Group className="mb-3" controlId="loginEmail">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="mb-4" controlId="loginPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </Form.Group>

        <div className="d-grid">
          <Button
            variant="primary"
            type="submit"
            size="lg"
            className="btn-accent"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </Button>
        </div>

        <div className="text-center mt-3">
          <span className="text-muted">
            Don't have an account?{" "}
            <a href="/register" className="fw-semibold text-decoration-none">
              Sign up here
            </a>
          </span>
        </div>
      </Form>
    </Container>
  );
};

export default Login;
