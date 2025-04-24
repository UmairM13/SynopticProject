import {
  Navbar,
  Nav,
  Container,
  Form,
  FormControl,
  Button,
  NavDropdown,
} from "react-bootstrap";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const AppNavbar = () => {
  const { isLoggedIn, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };
  return (
    <Navbar bg="light" expand="lg" className="shadow-sm">
      <Container>
        <Navbar.Brand as={RouterLink as any} to="/recommendations">
          🌍 TravelMate
        </Navbar.Brand>

        <Navbar.Toggle aria-controls="main-navbar" />
        <Navbar.Collapse id="main-navbar">
          <Nav className="me-auto">
            <Nav.Link as={RouterLink as any} to="/recommendations">
              Recommendations
            </Nav.Link>
            <Nav.Link as={RouterLink as any} to="/search">
              Search
            </Nav.Link>
          </Nav>

          <Form className="d-flex me-3" onSubmit={(e) => e.preventDefault()}>
            <FormControl
              type="search"
              placeholder="Search destinations..."
              className="me-2"
              aria-label="Search"
            />
            <Button variant="outline-primary" disabled>
              Search
            </Button>
          </Form>

          {isLoggedIn ? (
            <Nav>
              <NavDropdown title="Account" id="account-dropdown" align="end">
                <NavDropdown.Item as={RouterLink as any} to="/notebook">
                  Notebook
                </NavDropdown.Item>
                <NavDropdown.Item as={RouterLink as any} to="/preferences">
                  Preferences
                </NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item onClick={handleLogout}>
                  Logout
                </NavDropdown.Item>
              </NavDropdown>
            </Nav>
          ) : (
            <Button
              as={RouterLink as any}
              to="/login"
              variant="outline-primary"
            >
              Login / Signup
            </Button>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;
