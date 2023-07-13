import React from "react";
import { Col, ListGroup, Navbar, Image } from 'react-bootstrap';
import { FaHome, FaCamera, FaFolderOpen } from 'react-icons/fa';

const SideBar = () => (
  <Col sm={2} bg="light" className="text-light">
    <Navbar.Brand href="#home">
      <Image src="/build/logo_smartcount.jpeg" alt="Logo" width="100%" height="100" className="d-inline-block align-top" />
    </Navbar.Brand>
    <ListGroup variant="flush">
      <ListGroup.Item action href="#home">
        <FaHome /> Home
      </ListGroup.Item>
      <ListGroup.Item action href="#cameras">
        <FaCamera /> Câmeras
      </ListGroup.Item>
      <ListGroup.Item action href="#processedBatches">
        <FaFolderOpen /> Lotes Processados
      </ListGroup.Item>
    </ListGroup>
  </Col>
);

export default SideBar;
