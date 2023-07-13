import React from "react";
import { Col, ListGroup, Navbar, Image, Row } from 'react-bootstrap';
import { FaHome, FaCamera, FaFolderOpen, FaAngleRight } from 'react-icons/fa';
import './SideBar.css';

const SideBar = () => (
  <Col sm={2} className="sidebar-container bg-light">
    <Row>
      <Navbar.Brand href="#home" style={{padding: "10px"}}>
        <Image src="/build/logo_smartcount.png" alt="Logo" width="100%" height="100" className="d-inline-block align-top" />
      </Navbar.Brand>
      <ListGroup variant="flush" marginTop={{marginTop: "10px"}}>
        <ListGroup.Item action href="#home">
          <FaHome /> Home
        </ListGroup.Item>
        <ListGroup.Item action href="#cameras">
          <FaCamera /> Cameras
        </ListGroup.Item>
        <div className="list-item-container">
          <ListGroup.Item action href="#processedBatches">
            <FaFolderOpen /> Lotes Processados <FaAngleRight className="float-right"/>
          </ListGroup.Item>
          <div className="sub-menu">
            <a href="#sub1">Submenu 1</a>
            <a href="#sub2">Submenu 2</a>
          </div>
        </div>
      </ListGroup>
    </Row>
    <div className="footer-text">
      Desenvolvido por p-valor Consultoria
    </div>
  </Col>
);

export default SideBar;
