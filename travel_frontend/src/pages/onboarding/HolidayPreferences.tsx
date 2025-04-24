import { useState, useEffect } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import SelectableCard from "../../components/SelectableCard";
import mountainImg from "../../assets/images/mountain.jpg";
import desertImg from "../../assets/images/desert.jpg";
import jungleImg from "../../assets/images/jungle.jpg";
import beachImg from "../../assets/images/beach.jpg";
import urbanImg from "../../assets/images/urban.jpg";
import riverImg from "../../assets/images/river.jpg";
import coastalImg from "../../assets/images/coastal.jpg";
import valleyImg from "../../assets/images/valley.jpg";
import anyImg from "../../assets/images/any.jpg";

interface TerrainPreferencesProps {
  selected: string[];
  onContinue: (selected: string[]) => void;
}

const holidayOptions = [
  { label: "Relaxed", image: mountainImg },
  { label: "Adventurous", image: desertImg },
  { label: "Cultural", image: jungleImg },
  { label: "Romantic", image: beachImg },
  { label: "Shopping", image: urbanImg },
  { label: "Luxury", image: riverImg },
  { label: "Party", image: coastalImg },
  { label: "Family", image: valleyImg },
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
