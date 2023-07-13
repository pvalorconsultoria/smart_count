import React from "react";
import { Container, Row, Col, Card } from 'react-bootstrap';

const Home = () => (
  <Row>
    <Col xs={10}>
      <Container style={{ marginTop: "20px" }}>
        <Card>
          <Card.Header>Home</Card.Header>
          <Card.Body>
            Hello World
          </Card.Body>
        </Card>
      </Container>
    </Col>
  </Row>
);

export default Home;
