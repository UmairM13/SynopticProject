import { Modal, Button } from "react-bootstrap";

interface ExplanationModalProps {
  show: boolean;
  onHide: () => void;
  destinationName: string;
  explanation: string;
}

const ExplanationModal = ({
  show,
  onHide,
  destinationName,
  explanation,
}: ExplanationModalProps) => {
  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>Why {destinationName}?</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p>{explanation}</p>
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
