import { useParams } from "react-router-dom";
import { Container, Row, Col, Card, Spinner } from "react-bootstrap";
import { useEffect, useState } from "react";
import { getDestinationById } from "../api/DestinationApi";
import { searchFlights } from "../api/FlightsApi";
import { getUserById } from "../api/UserApi";
import airports from "../assets/airport-codes_json.json";

interface DestinationDetails {
  name: string;
  country: string;
  averageBudget: number;
  isOffSeason: boolean;
  climate: string[];
  terrain: string[];
  holidayType: string[];
  IATACode: string;
}

interface Airport {
  municipality: string;
  iso_country: string;
  iata_code: string | null;
}

// Helper to find IATA code
const findAirportByCity = (cityName: string, countryName?: string) => {
  if (!cityName) return null;

  const loweredCity = cityName.toLowerCase();
  const loweredCountry = countryName?.toLowerCase();

  const match = (airports as Airport[]).find((airport) => {
    const airportCity = airport.municipality?.toLowerCase();
    const airportCountry = airport.iso_country?.toLowerCase();
    return (
      airport.iata_code && // Only airports with IATA code
      ((airportCity && airportCity.includes(loweredCity)) ||
        (loweredCountry &&
          airportCountry &&
          airportCountry.includes(loweredCountry)))
    );
  });

  return match?.iata_code || null;
};

const DestinationDetailsPage = () => {
  const { destinationId } = useParams();
  const [details, setDetails] = useState<DestinationDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [flights, setFlights] = useState<any[]>([]);
  const [flightsLoading, setFlightsLoading] = useState(true);

  useEffect(() => {
    const fetchDetails = async () => {
      try {
        if (!destinationId) return;
        const data = await getDestinationById(Number(destinationId));

        const destinationData: DestinationDetails = {
          name: data.name,
          country: data.country,
          averageBudget: data.avg_daily_budget,
          isOffSeason: data.is_off_season,
          climate: data.climate ? [data.climate] : [],
          terrain: data.terrain
            ? data.terrain.split(",").map((item: string) => item.trim())
            : [],
          holidayType: data.holiday_type
            ? data.holiday_type.split(",").map((item: string) => item.trim())
            : [],
          IATACode: data.IATA_code || "",
        };
        setDetails(destinationData);

        await loadFlights(destinationData.IATACode);
      } catch (err) {
        console.error("Failed to load destination details", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDetails();
  }, [destinationId]);

  const loadFlights = async (destinationIATA: string) => {
    try {
      const userId = localStorage.getItem("id");
      if (!userId) throw new Error("User not logged in.");

      const userData = await getUserById(userId);

      const userCity = userData.current_city;

      //   console.log("Departure", userData.trip_start_date);
      const originIATA = findAirportByCity(userCity, userData.current_country);

      console.log(originIATA, destinationIATA);

      if (!originIATA || !destinationIATA) {
        throw new Error("Missing IATA codes for flight search.");
      }

      const data = await searchFlights(
        originIATA,
        destinationIATA,
        userData.trip_start_date
        // "2025-06"
      );

      console.log("Flights:", data);

      setFlights(data);
    } catch (error) {
      console.error(error);
    } finally {
      setFlightsLoading(false);
    }
  };

  if (loading) {
    return (
      <Container className="mt-5 text-center">
        <Spinner animation="border" />
      </Container>
    );
  }

  return (
    <Container className="mt-5">
      <Row>
        {/* Flights Column */}
        <Col md={4}>
          <Card className="p-3 mb-3 shadow-sm">
            <h5 className="mb-3">Flight Options</h5>
            {flightsLoading ? (
              <Spinner animation="border" size="sm" />
            ) : flights.length > 0 ? (
              <>
                {flights.slice(0, 4).map((flight, idx) => {
                  const firstSegment = flight.itineraries[0]?.segments[0];
                  const lastSegment =
                    flight.itineraries[0]?.segments.slice(-1)[0];
                  const airline = firstSegment?.carrierCode || "Unknown";

                  return (
                    <Card key={idx} className="mb-3 border-0 bg-light">
                      <Card.Body>
                        <div className="d-flex justify-content-between align-items-center">
                          <div className="text-center">
                            <h6>{firstSegment?.departure.iataCode}</h6>
                            <small>
                              {new Date(
                                firstSegment?.departure.at
                              ).toLocaleTimeString([], {
                                hour: "2-digit",
                                minute: "2-digit",
                              })}
                            </small>
                          </div>
                          <div>✈️</div>
                          <div className="text-center">
                            <h6>{lastSegment?.arrival.iataCode}</h6>
                            <small>
                              {new Date(
                                lastSegment?.arrival.at
                              ).toLocaleTimeString([], {
                                hour: "2-digit",
                                minute: "2-digit",
                              })}
                            </small>
                          </div>
                        </div>
                        <hr />
                        <p className="mb-1">
                          <strong>Airline:</strong> {airline}
                        </p>
                        <p className="mb-1">
                          <strong>Duration:</strong>{" "}
                          {flight.itineraries[0]?.duration
                            .replace("PT", "")
                            .toLowerCase()}
                        </p>
                        <p className="mb-0">
                          <strong>Price:</strong> £
                          {flight.price?.grandTotal || "N/A"}
                        </p>
                      </Card.Body>
                    </Card>
                  );
                })}

                {/* Button to View More Flights */}
                <div className="d-grid gap-2">
                  <a
                    href="https://www.skyscanner.net/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-primary"
                  >
                    View More Flights
                  </a>
                </div>
              </>
            ) : (
              <p>No flights found.</p>
            )}
          </Card>
        </Col>

        {/* Destination Info Column */}
        <Col md={4}>
          <Card className="p-4 shadow-sm">
            <h4 className="mb-3">
              {details?.name}, {details?.country}
            </h4>
            <p>
              <strong>Avg. Daily Budget:</strong> £{details?.averageBudget}
            </p>
            <p>
              <strong>Off-season:</strong> {details?.isOffSeason ? "Yes" : "No"}
            </p>
            <p>
              <strong>Climate:</strong> {details?.climate.join(", ")}
            </p>
            <p>
              <strong>Terrain:</strong> {details?.terrain.join(", ")}
            </p>
            <p>
              <strong>Holiday Type:</strong> {details?.holidayType.join(", ")}
            </p>
          </Card>
        </Col>

        {/* Hotels and Attractions Column */}
        <Col md={4}>
          <Card className="p-3 mb-3 shadow-sm">
            <h5>Top Hotels (Coming soon)</h5>
            <p>Search using Booking.com API...</p>
          </Card>

          <Card className="p-3 shadow-sm">
            <h5>Top Attractions (Coming soon)</h5>
            <p>Fetch from TripAdvisor API...</p>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default DestinationDetailsPage;
