import { useEffect, useState } from "react";
import { Container, Row, Col, Spinner, Alert } from "react-bootstrap";
import {
  fetchTopDestinations,
  fetchUserStats,
  fetchRecommendationActivity,
  fetchPreferencesDistribution,
  fetchPastDestinationsByNationality,
  fetchPastDestinationsByAge,
  fetchOffSeasonRate,
  fetchOffSeasonMonthly,
} from "../api/AdminApi"; // <-- we'll add these small fetchers
import { Bar, Pie, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";

// Register Chart.js modules
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

// Interfaces
interface TopDestination {
  destination_name: string;
  count: number;
}

interface UserStats {
  total_users: number;
  avg_age: number;
  avg_budget: number;
  top_climate: string;
  top_terrain: string;
  top_holiday_type: string;
  top_nationalities: { country: string; count: number }[];
  total_recommendations: string;
}

interface RecommendationActivity {
  year: number;
  month: number;
  count: number;
}

interface PreferenceDistribution {
  climates: { climate: string; count: number }[];
  terrains: { terrain: string; count: number }[];
}

interface PastDestinationRecord {
  nationality?: string;
  age?: number;
  destination: string;
  count: number;
}

interface OffSeasonRate {
  off_season_recommendations: number;
  peak_season_recommendations: number;
  off_season_ratio: string;
}

interface OffSeasonMonthly {
  month: string;
  off_season_destinations: number;
}

const AdminDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [topDestinations, setTopDestinations] = useState<TopDestination[]>([]);
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [activity, setActivity] = useState<RecommendationActivity[]>([]);
  const [preferences, setPreferences] = useState<PreferenceDistribution | null>(
    null
  );
  const [pastByNationality, setPastByNationality] = useState<
    PastDestinationRecord[]
  >([]);
  const [pastByAge, setPastByAge] = useState<PastDestinationRecord[]>([]);
  const [offSeasonRate, setOffSeasonRate] = useState<OffSeasonRate | null>(
    null
  );
  const [offSeasonMonthly, setOffSeasonMonthly] = useState<OffSeasonMonthly[]>(
    []
  );

  useEffect(() => {
    const loadData = async () => {
      try {
        const [
          topDest,
          stats,
          activityData,
          prefDist,
          pastNat,
          pastAge,
          seasonRate,
          seasonMonthly,
        ] = await Promise.all([
          fetchTopDestinations(),
          fetchUserStats(),
          fetchRecommendationActivity(),
          fetchPreferencesDistribution(),
          fetchPastDestinationsByNationality(),
          fetchPastDestinationsByAge(),
          fetchOffSeasonRate(),
          fetchOffSeasonMonthly(),
        ]);

        setTopDestinations(topDest);
        setUserStats(stats);
        setActivity(activityData);
        setPreferences(prefDist);
        setPastByNationality(pastNat);
        setPastByAge(pastAge);
        setOffSeasonRate(seasonRate);
        setOffSeasonMonthly(seasonMonthly);
      } catch (err) {
        console.error(err);
        setError("Failed to load admin data.");
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="text-center my-5">
        <Spinner animation="border" />
      </div>
    );
  }

  if (error) {
    return (
      <Container className="py-5">
        <Alert variant="danger" className="text-center">
          {error}
        </Alert>
      </Container>
    );
  }

  return (
    <Container className="py-5">
      <h2 className="text-center mb-5">📊 Admin Dashboard</h2>

      <Row className="mb-5">
        <Col md={6}>
          {/* Top Destinations */}
          <Bar
            data={{
              labels: topDestinations.map((d) => d.destination_name),
              datasets: [
                {
                  label: "Number of Saves",
                  data: topDestinations.map((d) => d.count),
                  backgroundColor: "rgba(59, 130, 246, 0.5)",
                },
              ],
            }}
            options={{
              responsive: true,
              plugins: {
                title: {
                  display: true,
                  text: "Top Saved Destinations",
                },
              },
            }}
          />
        </Col>

        <Col md={6}>
          {/* User Stats */}
          <div className="p-4 shadow rounded bg-light">
            <h5>User Stats</h5>
            {userStats && (
              <>
                <p>
                  <strong>Total Users:</strong> {userStats.total_users}
                </p>
                <p>
                  <strong>Avg Age:</strong> {Math.round(userStats.avg_age)}
                </p>
                <p>
                  <strong>Avg Budget:</strong> £
                  {Math.round(userStats.avg_budget)}
                </p>
                <p>
                  <strong>Top Climate:</strong> {userStats.top_climate || "N/A"}
                </p>
                <p>
                  <strong>Top Terrain:</strong> {userStats.top_terrain || "N/A"}
                </p>
                <p>
                  <strong>Top Holiday Type:</strong>{" "}
                  {userStats.top_holiday_type || "N/A"}
                </p>
                <p>
                  <strong>Top Nationalities:</strong>{" "}
                  {userStats.top_nationalities
                    .map((n) => `${n.country} (${n.count})`)
                    .join(", ")}
                </p>
                <p>
                  <strong>Top Recommendations:</strong>{" "}
                  {userStats.total_recommendations || "N/A"}
                </p>
              </>
            )}
          </div>
        </Col>
      </Row>

      <Row className="mb-5">
        <Col>
          {/* Monthly Recommendation Activity */}
          <Line
            data={{
              labels: activity.map((a) => `${a.month}/${a.year}`),
              datasets: [
                {
                  label: "Recommendations",
                  data: activity.map((a) => a.count),
                  fill: false,
                  borderColor: "rgba(99, 102, 241, 0.8)",
                  tension: 0.4,
                },
              ],
            }}
            options={{
              responsive: true,
              plugins: {
                title: {
                  display: true,
                  text: "Monthly Recommendation Activity",
                },
              },
            }}
          />
        </Col>
      </Row>

      <Row className="mb-5">
        <Col md={6}>
          {/* Climate Preferences */}
          {preferences && (
            <Pie
              data={{
                labels: preferences.climates.map((c) => c.climate),
                datasets: [
                  {
                    label: "Climate Preferences",
                    data: preferences.climates.map((c) => c.count),
                    backgroundColor: [
                      "rgba(255, 99, 132, 0.6)",
                      "rgba(54, 162, 235, 0.6)",
                      "rgba(255, 206, 86, 0.6)",
                      "rgba(75, 192, 192, 0.6)",
                      "rgba(153, 102, 255, 0.6)",
                    ],
                  },
                ],
              }}
              options={{
                plugins: {
                  title: {
                    display: true,
                    text: "Preferred Climates",
                  },
                },
              }}
            />
          )}
        </Col>

        <Col md={6}>
          {/* Terrain Preferences */}
          {preferences && (
            <Pie
              data={{
                labels: preferences.terrains.map((t) => t.terrain),
                datasets: [
                  {
                    label: "Terrain Preferences",
                    data: preferences.terrains.map((t) => t.count),
                    backgroundColor: [
                      "rgba(255, 159, 64, 0.6)",
                      "rgba(255, 99, 132, 0.6)",
                      "rgba(153, 102, 255, 0.6)",
                      "rgba(75, 192, 192, 0.6)",
                    ],
                  },
                ],
              }}
              options={{
                plugins: {
                  title: {
                    display: true,
                    text: "Preferred Terrains",
                  },
                },
              }}
            />
          )}
        </Col>
      </Row>

      <Row className="mb-5">
        <Col md={6}>
          {/* Past Destinations by Nationality */}
          <Bar
            data={{
              labels: pastByNationality.map(
                (r) => `${r.nationality}: ${r.destination}`
              ),
              datasets: [
                {
                  label: "Past Destinations (by Nationality)",
                  data: pastByNationality.map((r) => r.count),
                  backgroundColor: "rgba(54, 162, 235, 0.5)",
                },
              ],
            }}
            options={{
              plugins: {
                title: {
                  display: true,
                  text: "Top Past Destinations by Nationality",
                },
              },
            }}
          />
        </Col>

        <Col md={6}>
          {/* Past Destinations by Age */}
          <Bar
            data={{
              labels: pastByAge.map((r) => `${r.age}: ${r.destination}`),
              datasets: [
                {
                  label: "Past Destinations (by Age)",
                  data: pastByAge.map((r) => r.count),
                  backgroundColor: "rgba(255, 206, 86, 0.5)",
                },
              ],
            }}
            options={{
              plugins: {
                title: {
                  display: true,
                  text: "Top Past Destinations by Age",
                },
              },
            }}
          />
        </Col>
      </Row>

      <Row className="mb-5">
        <Col md={6}>
          {/* Off Season Rate */}
          {offSeasonRate && (
            <Pie
              data={{
                labels: ["Off-Season", "Peak-Season"],
                datasets: [
                  {
                    label: "Off-Season vs Peak-Season",
                    data: [
                      offSeasonRate.off_season_recommendations,
                      offSeasonRate.peak_season_recommendations,
                    ],
                    backgroundColor: [
                      "rgba(75, 192, 192, 0.6)",
                      "rgba(255, 99, 132, 0.6)",
                    ],
                  },
                ],
              }}
              options={{
                plugins: {
                  title: {
                    display: true,
                    text: `Off-Season Rate (${offSeasonRate.off_season_ratio})`,
                  },
                },
              }}
            />
          )}
        </Col>

        <Col md={6}>
          {/* Monthly Off-Season Availability */}
          <Line
            data={{
              labels: offSeasonMonthly.map((m) => m.month),
              datasets: [
                {
                  label: "Off-Season Destinations",
                  data: offSeasonMonthly.map((m) => m.off_season_destinations),
                  fill: true,
                  backgroundColor: "rgba(153, 102, 255, 0.2)",
                  borderColor: "rgba(153, 102, 255, 1)",
                },
              ],
            }}
            options={{
              plugins: {
                title: {
                  display: true,
                  text: "Monthly Off-Season Destination Availability",
                },
              },
            }}
          />
        </Col>
      </Row>
    </Container>
  );
};

export default AdminDashboard;
