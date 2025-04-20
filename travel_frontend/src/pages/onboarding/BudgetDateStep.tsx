import { useState } from "react";
import { Container, Row, Col, Form, Button } from "react-bootstrap";

interface BudgetDateStepProps {
  budget: string;
  trip_start_date: string;
  trip_end_date: string;
  onContinue: (data: {
    budget: string;
    trip_start_date: string;
    trip_end_date: string;
  }) => void;
  onSkip: () => void;
}

const BudgetDateStep = ({
  budget,
  trip_start_date,
  trip_end_date,
  onContinue,
  onSkip,
}: BudgetDateStepProps) => {
  const [localBudget, setLocalBudget] = useState(budget || "");
  const [tripStart, setTripStart] = useState(trip_start_date || "");
  const [tripEnd, setTripEnd] = useState(trip_end_date || "");

  const handleSubmit = () => {
    onContinue({
      budget: localBudget,
      trip_start_date: tripStart,
      trip_end_date: tripEnd,
    });
  };

  return (
    <Container className="mt-5" style={{ maxWidth: "600px" }}>
      <h2 className="mb-4 text-center">Your Travel Budget & Dates</h2>

      <Form>
        <Form.Group className="mb-3">
          <Form.Label>Estimated Total Budget (£)</Form.Label>
          <Form.Control
            type="number"
            placeholder="e.g. 1500"
            value={localBudget}
            onChange={(e) => setLocalBudget(e.target.value)}
            min="0"
          />
        </Form.Group>

        <Row>
          <Col>
            <Form.Group className="mb-3">
              <Form.Label>Trip Start Date</Form.Label>
              <Form.Control
                type="date"
                value={tripStart}
                onChange={(e) => setTripStart(e.target.value)}
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group className="mb-3">
              <Form.Label>Trip End Date</Form.Label>
              <Form.Control
                type="date"
                value={tripEnd}
                onChange={(e) => setTripEnd(e.target.value)}
              />
            </Form.Group>
          </Col>
        </Row>

        <div className="d-flex justify-content-between mt-4">
          <Button variant="secondary" onClick={onSkip}>
            Skip for now
          </Button>
          <Button className="btn-accent" onClick={handleSubmit}>
            Continue
          </Button>
        </div>
      </Form>
    </Container>
  );
};

export default BudgetDateStep;
