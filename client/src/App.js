import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import SideBar from './components/SideBar';
import Header from './components/Header';
import Home from './components/Home';
import ProcessedBatches from './components/ProcessedBatches/ProcessedBatches';

function App() {
  return (
    <Router>
      <Container fluid>
        <Row>
          <SideBar />
          <Col sm={10} style={{paddingLeft: "0px"}}>
            <Header />
            <Routes>
              <Route path="processedBatches" element={<ProcessedBatches/> } />
              <Route path="home" element={<Home />} />
              <Route path="/" element={<Navigate to="home" replace />} />
            </Routes>
          </Col>
        </Row>
      </Container>
    </Router>
  );
}

export default App;
