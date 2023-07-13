import React from "react";
import { Container, Row, Col, Card } from 'react-bootstrap';

const VideoFeed = () => (
  <Row>
    <Col xs={6}>
      <Container style={{ marginTop: "20px" }}>
        <Card>
          <Card.Header>Video Feed</Card.Header>
          <Card.Body>
            <img src="/video_feed" alt="Video Feed" style={{ maxHeight: "80vh", width: "auto", height: "auto" }}/>
          </Card.Body>
        </Card>
      </Container>
    </Col>
  </Row>
);

export default VideoFeed;
