import { useState, useEffect } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import SelectableCard from "../../components/SelectableCard";
import relaxedImg from "../../assets/images/holiday/relaxed.jpg";
import adventureImg from "../../assets/images/holiday/adventure.jpg";
import culturalImg from "../../assets/images/holiday/cultural.jpg";
import romanticImg from "../../assets/images/holiday/romantic.jpg";
import shoppingImg from "../../assets/images/holiday/shopping.jpg";
import luxuryImg from "../../assets/images/holiday/luxury.jpg";
import partyImg from "../../assets/images/holiday/party.jpg";
import familyImg from "../../assets/images/holiday/family.jpg";
import anyImg from "../../assets/images/holiday/any.jpg";

interface TerrainPreferencesProps {
  selected: string[];
  onContinue: (selected: string[]) => void;
}

const holidayOptions = [
  { label: "Relaxed", image: relaxedImg },
  { label: "Adventurous", image: adventureImg },
  { label: "Cultural", image: culturalImg },
  { label: "Romantic", image: romanticImg },
  { label: "Shopping", image: shoppingImg },
  { label: "Luxury", image: luxuryImg },
  { label: "Party", image: partyImg },
  { label: "Family", image: familyImg },
  { label: "Any", image: anyImg },
];
const HolidayPreferences = ({
  selected,
  onContinue,
}: TerrainPreferencesProps) => {
  const [selectedHolidays, setSelectedHolidays] = useState<string[]>(selected);

  useEffect(() => {
    setSelectedHolidays(selected);
  }, [selected]);

  const handleSelect = (label: string) => {
    setSelectedHolidays((prev) => {
      if (label === "Any") return ["Any"];
      const filtered = prev.includes("Any") ? [] : [...prev];
      return filtered.includes(label)
        ? filtered.filter((item) => item !== label)
        : [...filtered, label];
    });
  };

  const handleSubmit = () => {
    onContinue(selectedHolidays);
  };

  return (
    <Container className="mt-5">
      <h2 className="mb-4 text-center">Select Your Preferred Holiday Type</h2>
      <Row className="g-3">
        {holidayOptions.map((option, index) => (
          <Col key={index} md={4} className="mb-3">
            <SelectableCard
              label={option.label}
              image={option.image}
              isSelected={selectedHolidays.includes(option.label)}
              onSelect={() => handleSelect(option.label)}
            />
          </Col>
        ))}
      </Row>

      <div className="text-center mt-4">
        <Button
          variant="primary"
          onClick={handleSubmit}
          disabled={selectedHolidays.length === 0}
        >
          Continue
        </Button>
      </div>
    </Container>
  );
};

export default HolidayPreferences;
