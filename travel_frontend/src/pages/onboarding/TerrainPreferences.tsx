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

const terrainOptions = [
  { label: "Mountain", image: mountainImg },
  { label: "Desert", image: desertImg },
  { label: "Jungle", image: jungleImg },
  { label: "Beach", image: beachImg },
  { label: "Urban", image: urbanImg },
  { label: "River", image: riverImg },
  { label: "Coastal", image: coastalImg },
  { label: "Valley", image: valleyImg },
  { label: "Any", image: anyImg },
];

const TerrainPreferences = ({
  selected,
  onContinue,
}: TerrainPreferencesProps) => {
  const [selectedTerrains, setSelectedTerrains] = useState<string[]>(selected);

  useEffect(() => {
    setSelectedTerrains(selected);
  }, [selected]);

  const handleSelect = (label: string) => {
    setSelectedTerrains((prev) => {
      if (label === "Any") return ["Any"];
      const filtered = prev.includes("Any") ? [] : [...prev];
      return filtered.includes(label)
        ? filtered.filter((item) => item !== label)
        : [...filtered, label];
    });
  };

  const handleSubmit = () => {
    onContinue(selectedTerrains);
  };

  return (
    <Container className="mt-5">
      <h2 className="mb-4 text-center">Select Your Preferred Terrain</h2>
      <Row className="g-3">
        {terrainOptions.map((option, index) => (
          <Col key={index} md={4} className="mb-3">
            <SelectableCard
              label={option.label}
              image={option.image}
              isSelected={selectedTerrains.includes(option.label)}
              onSelect={() => handleSelect(option.label)}
            />
          </Col>
        ))}
      </Row>

      <div className="text-center mt-4">
        <Button
          variant="primary"
          onClick={handleSubmit}
          disabled={selectedTerrains.length === 0}
        >
          Continue
        </Button>
      </div>
    </Container>
  );
};

export default TerrainPreferences;
