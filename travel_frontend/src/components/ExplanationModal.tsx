import { JSX } from "react";
import { Modal, Button } from "react-bootstrap";

interface ExplanationModalProps {
  show: boolean;
  onHide: () => void;
  destinationName: string;
  explanation: any;
}

const ExplanationModal = ({
  show,
  onHide,
  destinationName,
  explanation,
}: ExplanationModalProps) => {
  const renderValue = (value: any, key?: string): JSX.Element | string => {
    // Special case for similar_destinations
    if (key === "similar_destinations" && Array.isArray(value)) {
      return (
        <ul>
          {value.map((item: any, idx: number) => (
            <li key={idx}>
              <strong>{item.name}</strong> (Similarity: {item.similarity_score})
            </li>
          ))}
        </ul>
      );
    }

    if (Array.isArray(value)) {
      return value.join(", ");
    } else if (typeof value === "object" && value !== null) {
      return (
        <ul>
          {Object.entries(value).map(([k, v]) => (
            <li key={k}>
              <strong>{k}:</strong> {renderValue(v, k)}
            </li>
          ))}
        </ul>
      );
    } else {
      return String(value);
    }
  };

  return (
    <Modal show={show} onHide={onHide} centered size="lg">
      <Modal.Header closeButton>
        <Modal.Title>Why {destinationName}?</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {explanation.match_summary && (
          <>
            <h5 className="mb-2">Match Summary:</h5>
            <p>{explanation.match_summary.join(", ")}</p>
          </>
        )}

        {explanation.details && (
          <>
            <h5 className="mt-4">Details:</h5>
            <ul>
              {Object.entries(explanation.details).map(([key, value]) => (
                <li key={key}>
                  <strong>{key}:</strong> {renderValue(value, key)}
                </li>
              ))}
            </ul>
          </>
        )}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ExplanationModal;
