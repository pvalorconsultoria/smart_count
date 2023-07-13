import React from "react";
import { Row, Col, Navbar, Nav, Dropdown, Image } from 'react-bootstrap';

const Header = () => (
  <Row>
    <Col>
      <Navbar bg="light" expand="lg">
        <Navbar.Brand href="#home">Dashboard</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav>
            <Nav.Link href="#home">Home</Nav.Link>
            <Nav.Link href="#cameras">Câmeras</Nav.Link>
            <Nav.Link href="#processedBatches">Lotes Processados</Nav.Link>
          </Nav>
          <Nav style={{ marginLeft: "auto", marginRight: "100px" }}>
            <Dropdown alignRight >
              <Dropdown.Toggle variant="success" id="dropdown-basic">
                <Image src="/build/logo192.png" roundedCircle width="30" height="30" />
              </Dropdown.Toggle>
              <Dropdown.Menu style={{ marginTop: "10px" }}>
                <Dropdown.Item href="#preferences">Preferências</Dropdown.Item>
                <Dropdown.Item href="#myAccount">Minha Conta</Dropdown.Item>
                <Dropdown.Item href="#logout">Sair</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    </Col>
  </Row>
);

export default Header;
