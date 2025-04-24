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

const climateOptions = [
  { label: "Tropical", image: mountainImg },
  { label: "Arid", image: desertImg },
  { label: "Temperate", image: jungleImg },
  { label: "Polar", image: beachImg },
  { label: "Mediterranean", image: urbanImg },
  { label: "Humid", image: riverImg },
  { label: "Sub-Tropical", image: coastalImg },
  { label: "Alpine", image: valleyImg },
  { label: "Any", image: anyImg },
];

const ClimatePreferences = ({
  selected,
  onContinue,
}: TerrainPreferencesProps) => {
  const [selectedClimate, setSelectedClimates] = useState<string[]>(selected);

  useEffect(() => {
    setSelectedClimates(selected);
  }, [selected]);

  const handleSelect = (label: string) => {
    setSelectedClimates((prev) => {
      if (label === "Any") return ["Any"];
      const filtered = prev.includes("Any") ? [] : [...prev];
      return filtered.includes(label)
        ? filtered.filter((item) => item !== label)
        : [...filtered, label];
    });
  };

  const handleSubmit = () => {
    onContinue(selectedClimate);
  };

  return (
    <Container className="mt-5">
      <h2 className="mb-4 text-center">Select Your Preferred Climate</h2>
      <Row className="g-3">
        {climateOptions.map((option, index) => (
          <Col key={index} md={4} className="mb-3">
            <SelectableCard
              label={option.label}
              image={option.image}
              isSelected={selectedClimate.includes(option.label)}
              onSelect={() => handleSelect(option.label)}
            />
          </Col>
        ))}
      </Row>

      <div className="text-center mt-4">
        <Button
          variant="primary"
          onClick={handleSubmit}
          disabled={selectedClimate.length === 0}
        >
          Continue
        </Button>
      </div>
    </Container>
  );
};

export default ClimatePreferences;
