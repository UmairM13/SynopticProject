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
}

const BudgetDateStep = ({
  budget,
  trip_start_date,
  trip_end_date,
  onContinue,
}: BudgetDateStepProps) => {
  // Calculate default dates: one month from today, and +7 days after that
  const today = new Date();
  const defaultStart = new Date(today.setMonth(today.getMonth() + 1));
  const defaultEnd = new Date(defaultStart);
  defaultEnd.setDate(defaultEnd.getDate() + 7);

  const formatDate = (date: Date) => date.toISOString().split("T")[0];

  const [localBudget, setLocalBudget] = useState(budget || "1000");
  const [tripStart, setTripStart] = useState(
    trip_start_date || formatDate(defaultStart)
  );
  const [tripEnd, setTripEnd] = useState(
    trip_end_date || formatDate(defaultEnd)
  );

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
          <Button className="btn-accent" onClick={handleSubmit}>
            Continue
          </Button>
        </div>
      </Form>
    </Container>
  );
};

export default BudgetDateStep;
