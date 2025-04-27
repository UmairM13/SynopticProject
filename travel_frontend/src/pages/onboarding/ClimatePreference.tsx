import { useState, useEffect } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import SelectableCard from "../../components/SelectableCard";
import tropicalImg from "../../assets/images/climate/tropical.jpg";
import aridImg from "../../assets/images/climate/arid.jpg";
import temperateImg from "../../assets/images/climate/temperate.jpg";
import polarImg from "../../assets/images/climate/polar.jpg";
import mediterraneanImg from "../../assets/images/climate/mediterranean.jpg";
import humidImg from "../../assets/images/climate/humid.jpg";
import subTropicalImg from "../../assets/images/climate/subtropical.jpg";
import alpineImg from "../../assets/images/climate/alpine.jpg";
import anyImg from "../../assets/images/climate/any.jpg";

interface TerrainPreferencesProps {
  selected: string[];
  onContinue: (selected: string[]) => void;
}

const climateOptions = [
  { label: "Tropical", image: tropicalImg },
  { label: "Arid", image: aridImg },
  { label: "Temperate", image: temperateImg },
  { label: "Polar", image: polarImg },
  { label: "Mediterranean", image: mediterraneanImg },
  { label: "Humid", image: humidImg },
  { label: "Sub-Tropical", image: subTropicalImg },
  { label: "Alpine", image: alpineImg },
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
