import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import SideBar from './components/SideBar';
import Header from './components/Header';
import VideoFeed from './components/VideoFeed';

function App() {
  return (
    <Container fluid>
      <Row>
        <SideBar />
        <Col sm={10}>
          <Header />
          <VideoFeed />
        </Col>
      </Row>
    </Container>
  );
}

export default App;
