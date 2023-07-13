import React from "react";
import { Col, ListGroup, Navbar, Image, Row } from 'react-bootstrap';
import { FaHome, FaCamera, FaFolderOpen, FaAngleRight } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import './SideBar.css';

const SideBar = () => (
  <Col sm={2} className="sidebar-container bg-light">
    <Row>
      <Navbar.Brand as={Link} to="home" style={{padding: "10px"}}>
        <Image src="/build/logo_smartcount.png" alt="Logo" width="100%" height="100" className="d-inline-block align-top" />
      </Navbar.Brand>
      <ListGroup variant="flush" marginTop={{marginTop: "10px"}}>
        <ListGroup.Item action as={Link} to="home">
          <FaHome /> Home
        </ListGroup.Item>
        <ListGroup.Item action as={Link} to="cameras">
          <FaCamera /> Cameras
        </ListGroup.Item>
        <div className="list-item-container">
          <ListGroup.Item action as={Link} to="processedBatches">
            <FaFolderOpen /> Lotes Processados <FaAngleRight className="float-right"/>
          </ListGroup.Item>
          <div className="sub-menu">
            <Link to="sub1">Submenu 1</Link>
            <Link to="sub2">Submenu 2</Link>
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
