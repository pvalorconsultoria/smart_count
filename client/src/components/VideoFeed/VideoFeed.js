import React from "react";
import { Container, Row, Col, Card } from 'react-bootstrap';

const VideoFeed = () => (
  <Row>
    <Col>
      <Container style={{ marginTop: "20px" }}>
        <Card style={{ width: "40%", height: "40%" }}>
          <Card.Header>Video Feed</Card.Header>
          <Card.Body>
            <img src="/video_feed" alt="Video Feed" style={{ width: "100%", height: "100%" }}/>
          </Card.Body>
        </Card>
      </Container>
    </Col>
  </Row>
);

export default VideoFeed;
