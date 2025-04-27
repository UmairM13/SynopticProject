import { useState, useEffect } from "react";
import { Container, Row, Col, Button, Modal } from "react-bootstrap";
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

interface ClimatePreferencesProps {
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
}: ClimatePreferencesProps) => {
  const [selectedClimate, setSelectedClimates] = useState<string[]>(selected);
  const [showInfoModal, setShowInfoModal] = useState(false);

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
      <div className="d-flex justify-content-center align-items-center mb-4 position-relative">
        <h2 className="text-center">Select Your Preferred Climate</h2>
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

      {/* Info Modal */}
      <Modal
        show={showInfoModal}
        onHide={() => setShowInfoModal(false)}
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>Climate Preferences Info</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>
            Selecting your preferred climates helps us recommend destinations
            where you'll feel most comfortable!
          </p>
          <ul>
            <li>
              <strong>Tropical</strong> — e.g., Bali (Indonesia), Honolulu (USA)
            </li>
            <li>
              <strong>Arid</strong> — e.g., Cairo (Egypt), Phoenix (USA)
            </li>
            <li>
              <strong>Temperate</strong> — e.g., Paris (France), Vancouver
              (Canada)
            </li>
            <li>
              <strong>Polar</strong> — e.g., Reykjavik (Iceland), Tromsø
              (Norway)
            </li>
            <li>
              <strong>Mediterranean</strong> — e.g., Barcelona (Spain), Athens
              (Greece)
            </li>
            <li>
              <strong>Humid</strong> — e.g., Singapore, New Orleans (USA)
            </li>
            <li>
              <strong>Sub-Tropical</strong> — e.g., Algiers (Algeria), Brisbane
              (Australia)
            </li>
            <li>
              <strong>Alpine</strong> — e.g., Chamonix (France), Queenstown (New
              Zealand)
            </li>
            <li>
              <strong>Any</strong> — I'm open to any kind of climate!
            </li>
          </ul>
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default ClimatePreferences;
