import { useState } from "react";
import TerrainPreferences from "./TerrainPreferences";
import ClimatePreferences from "./ClimatePreference";
import HolidayPreferences from "./HolidayPreferences";
import BudgetDateInput from "./BudgetDateStep";
import FinalReview from "./FinalReview";
import { updateUser } from "../../api/UserApi";
import { useNavigate } from "react-router-dom";

// You can adjust this to include email, age, etc. from context if needed
interface OnboardingFormData {
  preferred_terrain: string[];
  preferred_climate: string[];
  holiday_type: string[];
  budget: string;
  trip_start_date: string;
  trip_end_date: string;
}

const OnboardingFlow = () => {
  const [step, setStep] = useState(0);

  const [formData, setFormData] = useState<OnboardingFormData>({
    preferred_terrain: [],
    preferred_climate: [],
    holiday_type: [],
    budget: "",
    trip_start_date: "",
    trip_end_date: "",
  });

  const navigate = useNavigate();

  const nextStep = () => setStep((prev) => prev + 1);
  //   const prevStep = () => setStep((prev) => prev - 1);

  const updateFormData = (newData: Partial<OnboardingFormData>) => {
    setFormData((prev) => ({ ...prev, ...newData }));
  };

  const handleFinalSubmit = async () => {
    console.log("Submitting final onboarding data:", formData);
    // TODO: Send to backend via API call
    try {
      const userId = localStorage.getItem("id");
      if (!userId) throw new Error("User ID not found in local storage");

      const payload = {
        preferred_terrain: formData.preferred_terrain.join(", "),
        preferred_climate: formData.preferred_climate.join(", "),
        holiday_type: formData.holiday_type.join(", "),
        budget: formData.budget ? parseFloat(formData.budget) : null,
        trip_start_date: formData.trip_start_date || null,
        trip_end_date: formData.trip_end_date || null,
        has_onboarded: true,
      };

      await updateUser(parseInt(userId), payload);
      localStorage.setItem("has_onboarded", "true");
      console.log("User preferences updated successfully");

      navigate("/notebook");
    } catch (error) {
      console.error("Error updating user preferences:", error);
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
        nextStep();
      }}
      onSkip={nextStep}
    />,
    <FinalReview
      key="review"
      userData={{
        email: "placeholder@email.com", // Replace with actual user data
        age: "25",
        nationality: "British",
        currentCity: "London",
        currentCountry: "UK",
        preferredTerrains: formData.preferred_terrain,
        preferredClimates: formData.preferred_climate,
        holidayType: formData.holiday_type[0] || "N/A",
        budget: formData.budget || null,
        tripStartDate: formData.trip_start_date || null,
        tripEndDate: formData.trip_end_date || null,
      }}
      onEdit={() => setStep(0)}
      onSubmit={handleFinalSubmit}
    />,
  ];

  return <>{steps[step]}</>;
};

export default OnboardingFlow;
