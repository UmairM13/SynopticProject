import { useEffect, useState } from "react";
import { Container, Row, Col, Spinner, Alert } from "react-bootstrap";
import {
  fetchTopDestinations,
  fetchUserStats,
  fetchRecommendationActivity,
} from "../api/AdminApi";
import { Bar, Line } from "react-chartjs-2";
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
} from "chart.js";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

// Types
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
}

interface RecommendationActivity {
  year: number;
  month: number;
  count: number;
}

const AdminDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [topDestinations, setTopDestinations] = useState<TopDestination[]>([]);
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [activity, setActivity] = useState<RecommendationActivity[]>([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [topDest, stats, activityData] = await Promise.all([
          fetchTopDestinations(),
          fetchUserStats(),
          fetchRecommendationActivity(),
        ]);
        setTopDestinations(topDest);
        setUserStats(stats);
        setActivity(activityData);
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
          {/* Top Destinations Chart */}
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
                legend: {
                  position: "top" as const,
                },
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
              </>
            )}
          </div>
        </Col>
      </Row>

      <Row>
        <Col>
          {/* Recommendation Activity Over Time */}
          <Line
            data={{
              labels: activity.map((a) => `${a.month}/${a.year}`),
              datasets: [
                {
                  label: "Recommendations",
                  data: activity.map((a) => a.count),
                  fill: false,
                  borderColor: "rgba(99, 102, 241, 0.8)",
                  tension: 0.3,
                },
              ],
            }}
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: "top" as const,
                },
                title: {
                  display: true,
                  text: "Monthly Recommendation Activity",
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
