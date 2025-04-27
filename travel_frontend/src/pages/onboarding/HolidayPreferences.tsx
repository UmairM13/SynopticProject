import { useState, useEffect } from "react";
import { Container, Row, Col, Button, Modal } from "react-bootstrap";
import SelectableCard from "../../components/SelectableCard";
import relaxedImg from "../../assets/images/holiday/relaxed.jpg";
import adventureImg from "../../assets/images/holiday/adventure.jpg";
import culturalImg from "../../assets/images/holiday/culture.jpg";
import romanticImg from "../../assets/images/holiday/romantic.jpg";
import shoppingImg from "../../assets/images/holiday/shopping.jpg";
import luxuryImg from "../../assets/images/holiday/luxury.jpg";
import partyImg from "../../assets/images/holiday/party.jpg";
import familyImg from "../../assets/images/holiday/family.jpg";
import anyImg from "../../assets/images/holiday/any.jpg";

interface HolidayPreferencesProps {
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
}: HolidayPreferencesProps) => {
  const [selectedHolidays, setSelectedHolidays] = useState<string[]>(selected);
  const [showInfoModal, setShowInfoModal] = useState(false);

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
      <div className="d-flex justify-content-center align-items-center mb-4 position-relative">
        <h2 className="text-center">Select Your Preferred Holiday Type</h2>
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

      {/* Info Modal */}
      <Modal
        show={showInfoModal}
        onHide={() => setShowInfoModal(false)}
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>Holiday Preferences Info</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>
            Picking your preferred holiday type helps us tailor your trip
            experience!
          </p>
          <ul>
            <li>
              <strong>Relaxed</strong> — e.g., Santorini (Greece), Maldives
            </li>
            <li>
              <strong>Adventurous</strong> — e.g., Queenstown (New Zealand),
              Costa Rica
            </li>
            <li>
              <strong>Cultural</strong> — e.g., Kyoto (Japan), Rome (Italy)
            </li>
            <li>
              <strong>Romantic</strong> — e.g., Paris (France), Venice (Italy)
            </li>
            <li>
              <strong>Shopping</strong> — e.g., Milan (Italy), Dubai (UAE)
            </li>
            <li>
              <strong>Luxury</strong> — e.g., Bora Bora, Monaco
            </li>
            <li>
              <strong>Party</strong> — e.g., Ibiza (Spain), Cancun (Mexico)
            </li>
            <li>
              <strong>Family</strong> — e.g., Orlando (USA), Gold Coast
              (Australia)
            </li>
            <li>
              <strong>Any</strong> — I'm open to any type of holiday!
            </li>
          </ul>
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default HolidayPreferences;
