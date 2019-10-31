import Page from 'components/Page';
import React from 'react';
import {
  Card,
  CardBody,
  Col,
  Row,
  Table,
} from 'reactstrap';

const CardPage = () => {
  return (
    <Page>

      <Row key="1">
          <Col>
            <Card className="mb-3">
              <CardBody>
                <Row>
                  <Col>
                    <Card body>
                      <Table {...{ ['bordered' || 'default']: true }}>
                        <tbody>
                          <tr>
                            <td>Card Number: </td>
                            <td>Balance: </td>
                          </tr>
                        </tbody>
                      </Table>
                    </Card>
                  </Col>
                </Row>
              </CardBody>
            </Card>
          </Col>
        </Row> 
    </Page>
  );
};

export default CardPage;
