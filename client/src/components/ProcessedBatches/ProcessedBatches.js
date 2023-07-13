import React, { useEffect, useState } from "react";
import { Container, Row, Col, Card, Table, Button, Modal } from 'react-bootstrap';
import axios from 'axios';
import { BsEye, BsTrash, BsArrowRepeat } from "react-icons/bs";
import VideoFeed from '../VideoFeed';

const ProcessedBatches = () => {
  const [data, setData] = useState([]);
  const [showModal, setShowModal] = useState(false); // State to control the modal
  const [currentItem, setCurrentItem] = useState(null); // Store current item

  useEffect(() => {
    axios.get('/api/processedBatches')
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error(`Error fetching data: ${error}`);
      });
  }, []);

  const handleReprocess = (item) => {
    axios.post('/api/processVideo', item) // Make a POST request
      .then((response) => {
        setCurrentItem(item);
        setShowModal(true); // Open the modal
      })
      .catch((error) => {
        console.error(`Error reprocessing data: ${error}`);
      });
  };

  return (
    <Row>
      <Col xs={10}>
        <Container style={{ marginTop: "20px" }}>
          <Card>
            <Card.Header>Lotes Processados</Card.Header>
            <Card.Body>
              <Table striped bordered hover>
                <thead>
                  <tr>
                    <th>Data de Processamento</th>
                    <th>Camera</th>
                    <th>Produto</th>
                    <th>Linha de Produção</th>
                    <th>Planta</th>
                    <th>Quantidade</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((item, index) => (
                    <tr key={index}>
                      <td>{item.dataDeProcessamento}</td>
                      <td>{item.camera}</td>
                      <td>{item.produto}</td>
                      <td>{item.linhaDeProducao}</td>
                      <td>{item.planta}</td>
                      <td>{item.quantidadeContada}</td>
                      <td>
                        <Button variant="outline-primary" size="sm" onClick={() => handleReprocess(item)}>
                          <BsArrowRepeat /> 
                        </Button>{' '}
                        <Button variant="outline-success" size="sm">
                          <BsEye /> 
                        </Button>{' '}
                        <Button variant="outline-danger" size="sm">
                          <BsTrash /> 
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Container>
        <Modal show={showModal} onHide={() => setShowModal(false)}>
          <Modal.Header closeButton>
            <Modal.Title>Reprocessing Video</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <VideoFeed item={currentItem} />
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
      </Col>
    </Row>
  );
};

export default ProcessedBatches;
