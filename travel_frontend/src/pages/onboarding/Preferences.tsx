import { useEffect, useState } from "react";
import TerrainPreferences from "./TerrainPreferences";
import ClimatePreferences from "./ClimatePreference";
import HolidayPreferences from "./HolidayPreferences";
import BudgetDateInput from "./BudgetDateStep";
import { updateUser, getUserById } from "../../api/UserApi";
import { useNavigate } from "react-router-dom";
import { Spinner, Alert, Container } from "react-bootstrap";

interface PreferencesFormData {
  preferred_terrain: string[];
  preferred_climate: string[];
  holiday_type: string[];
  budget: string;
  trip_start_date: string;
  trip_end_date: string;
}

const Preferences = () => {
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState<PreferencesFormData>({
    preferred_terrain: [],
    preferred_climate: [],
    holiday_type: [],
    budget: "",
    trip_start_date: "",
    trip_end_date: "",
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();
  const userId = localStorage.getItem("id");

  useEffect(() => {
    const loadUserData = async () => {
      if (!userId) {
        setError("User not logged in.");
        return;
      }

      try {
        const user = await getUserById(userId);
        setFormData({
          preferred_terrain: user.preferred_terrain?.split(",") || [],
          preferred_climate: user.preferred_climate?.split(",") || [],
          holiday_type: user.holiday_type?.split(",") || [],
          budget: user.budget?.toString() || "",
          trip_start_date: user.trip_start_date || null,
          trip_end_date: user.trip_end_date || null,
        });
      } catch (err) {
        setError("Failed to load user preferences.");
      } finally {
        setLoading(false);
      }
    };

    loadUserData();
  }, [userId]);

  const nextStep = () => setStep((prev) => prev + 1);
  const updateFormData = (newData: Partial<PreferencesFormData>) => {
    setFormData((prev) => ({ ...prev, ...newData }));
  };

  const handleFinalSubmit = async () => {
    if (!userId) return;
    try {
      await updateUser(parseInt(userId), {
        preferred_terrain: formData.preferred_terrain.join(","),
        preferred_climate: formData.preferred_climate.join(","),
        holiday_type: formData.holiday_type.join(","),
        budget: parseFloat(formData.budget),
        trip_start_date: formData.trip_start_date,
        trip_end_date: formData.trip_end_date,
      });
      setSuccess("Preferences updated successfully!");
      navigate("/notebook");
    } catch (err) {
      setError("Error updating preferences.");
    }
  };

  const steps = [
    <TerrainPreferences
      key="terrain"
      selected={formData.preferred_terrain}
      onContinue={(data) => {
        updateFormData({ preferred_terrain: data });
        nextStep();
      }}
    />,
    <ClimatePreferences
      key="climate"
      selected={formData.preferred_climate}
      onContinue={(data) => {
        updateFormData({ preferred_climate: data });
        nextStep();
      }}
    />,
    <HolidayPreferences
      key="holiday"
      selected={formData.holiday_type}
      onContinue={(data) => {
        updateFormData({ holiday_type: data });
        nextStep();
      }}
    />,
    <BudgetDateInput
      key="budget-dates"
      budget={formData.budget}
      trip_start_date={formData.trip_start_date}
      trip_end_date={formData.trip_end_date}
      onContinue={(data) => {
        updateFormData(data);
        handleFinalSubmit();
      }}
      onSkip={() => handleFinalSubmit()}
    />,
  ];

  if (loading) {
    return (
      <Container className="mt-5 text-center">
        <Spinner animation="border" />
      </Container>
    );
  }

  return (
    <Container className="mt-4">
      {error && <Alert variant="danger">{error}</Alert>}
      {success && <Alert variant="success">{success}</Alert>}
      {steps[step]}
    </Container>
  );
};

export default Preferences;
