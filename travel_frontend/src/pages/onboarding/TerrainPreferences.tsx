import { useState, useEffect } from "react";
import { Container, Row, Col, Button, Modal } from "react-bootstrap";
import SelectableCard from "../../components/SelectableCard";
import mountainImg from "../../assets/images/terrain/mountain.jpg";
import desertImg from "../../assets/images/terrain/desert.jpg";
import jungleImg from "../../assets/images/terrain/jungle.jpg";
import beachImg from "../../assets/images/terrain/beach.jpg";
import urbanImg from "../../assets/images/terrain/urban.jpg";
import riverImg from "../../assets/images/terrain/river.jpg";
import coastalImg from "../../assets/images/terrain/coastal.jpg";
import valleyImg from "../../assets/images/terrain/valley.jpg";
import anyImg from "../../assets/images/terrain/any.jpg";

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
  const [showInfoModal, setShowInfoModal] = useState(false);

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
      <div className="d-flex justify-content-center align-items-center mb-4 position-relative">
        <h2 className="text-center">Select Your Preferred Terrain</h2>
        <Button
          variant="outline-secondary"
          size="sm"
          className="ms-2 position-absolute"
          style={{ top: 0, right: 0 }}
          onClick={() => setShowInfoModal(true)}
        >
          i
        </Button>
      </div>

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

      {/* Info Modal */}
      <Modal
        show={showInfoModal}
        onHide={() => setShowInfoModal(false)}
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>Terrain Preferences Info</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>
            Selecting your preferred terrains helps us match you with
            destinations that fit your ideal landscapes!
          </p>
          <ul>
            <li>
              <strong>Mountain</strong> — e.g., Zermatt (Switzerland), Aspen
              (USA)
            </li>
            <li>
              <strong>Desert</strong> — e.g., Dubai (UAE), Marrakech (Morocco)
            </li>
            <li>
              <strong>Jungle</strong> — e.g., Manaus (Brazil), Siem Reap
              (Cambodia)
            </li>
            <li>
              <strong>Beach</strong> — e.g., Bali (Indonesia), Cancun (Mexico)
            </li>
            <li>
              <strong>Urban</strong> — e.g., New York City (USA), Tokyo (Japan)
            </li>
            <li>
              <strong>River</strong> — e.g., Victoria Falls (Zimbabwe), Porto
              (Portugal)
            </li>
            <li>
              <strong>Coastal</strong> — e.g., Amalfi Coast (Italy), Cape Town
              (South Africa)
            </li>
            <li>
              <strong>Valley</strong> — e.g., Napa Valley (USA), Lauterbrunnen
              (Switzerland)
            </li>
            <li>
              <strong>Any</strong> — I'm open to any kind of terrain!
            </li>
          </ul>
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default TerrainPreferences;
