import { Card } from "react-bootstrap";

interface SelectableCardProps {
  image: string;
  label: string;
  isSelected: boolean;
  onSelect: () => void;
}

const SelectableCard = ({
  image,
  label,
  isSelected,
  onSelect,
}: SelectableCardProps) => {
  return (
    <Card
      className={`text-center selectable-card ${isSelected ? "selected" : ""}`}
      onClick={onSelect}
      style={{
        cursor: "pointer",
        border: isSelected ? "2px solid #4B9CD3" : "1px solid #ccc",
      }}
    >
      <Card.Img
        variant="top"
        src={image}
        height="160px"
        style={{ objectFit: "cover" }}
      />
      <Card.Body>
        <Card.Text>{label}</Card.Text>
      </Card.Body>
    </Card>
  );
};

export default SelectableCard;
