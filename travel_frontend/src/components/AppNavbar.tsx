import {
  Navbar,
  Nav,
  Container,
  Form,
  FormControl,
  Button,
  NavDropdown,
  ListGroup,
} from "react-bootstrap";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useEffect, useRef, useState } from "react";
import { searchDestinations } from "../api/searchApi";

interface SearchResult {
  id: number;
  name: string;
  country?: string;
}

const AppNavbar = () => {
  const { isLoggedIn, logout, userEmail } = useAuth(); // ✅ also get userEmail here
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setShowDropdown(false);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  const handleSearchChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);

    if (query.trim().length === 0) {
      setSearchResults([]);
      setShowDropdown(false);
      return;
    }

    try {
      const results = await searchDestinations(query);
      setSearchResults(results.slice(0, 5)); // Limit to 5 results
      setShowDropdown(true);
    } catch (error) {
      console.error("Search failed", error);
      setSearchResults([]);
      setShowDropdown(false);
    }
  };

  const handleResultClick = (id: number) => {
    setSearchQuery("");
    setShowDropdown(false);
    navigate(`/destination/${id}`);
  };

  return (
    <Navbar bg="light" expand="lg" className="shadow-sm position-relative">
      <Container>
        <Navbar.Brand as={RouterLink as any} to="/">
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

          <Form
            className="d-flex me-3 position-relative"
            onSubmit={(e) => e.preventDefault()}
            ref={dropdownRef}
          >
            <FormControl
              type="search"
              placeholder="Search destinations..."
              className="me-2"
              aria-label="Search"
              value={searchQuery}
              onChange={handleSearchChange}
            />
            {/* <Button variant="outline-primary" disabled>
              Search
            </Button> */}

            {showDropdown && searchResults.length > 0 && (
              <div
                className="position-absolute bg-white shadow rounded mt-2 w-100 z-10"
                style={{ top: "100%", left: 0 }}
              >
                <ListGroup>
                  {searchResults.map((result) => (
                    <ListGroup.Item
                      action
                      key={result.id}
                      onClick={() => handleResultClick(result.id)}
                    >
                      {result.name}{" "}
                      {result.country ? `(${result.country})` : ""}
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              </div>
            )}
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
                {/* Admin dashboard link inside Nav */}
                {isLoggedIn && userEmail === "admin@travelmate.com" && (
                  <NavDropdown.Item as={RouterLink as any} to="/admin">
                    Admin Dashboard
                  </NavDropdown.Item>
                )}
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
