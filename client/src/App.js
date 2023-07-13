import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

function App() {
  return (
    <Container fluid>
      <Row>
        {/* Left Bar */}
        <Col sm={2} className="bg-dark text-light">
          {/* Place your left bar content here */}
        </Col>

        {/* Main Content */}
        <Col sm={10}>
          {/* Header */}
          <Row>
            <Col>
              {/* Place your header content here */}
            </Col>
          </Row>

          {/* Video Feed */}
          <Row>
            <Col>
              {/* Place your video feed component here */}
              <img src="/video_feed" alt="Video Feed" />
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
