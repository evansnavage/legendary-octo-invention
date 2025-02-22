import React from 'react';
import { Form, FormGroup, Input, Label, Button, Card, CardBody } from 'reactstrap';
import './Login.css';
import 'bootstrap/dist/css/bootstrap.css';

function Login() {
    return (
        <>
            <div className="logo-text text-center mt-5 pt-5">LOGIN</div>

            <div className="login-container">
                <Card className="login-card">
                    <CardBody>
                        <div className="login-form">
                            <Form>
                                <FormGroup>
                                    <Label for="exampleEmail">
                                        Email
                                    </Label>
                                    <Input
                                        id="exampleEmail"
                                        name="email"
                                        // placeholder="Email"
                                        type="email"
                                    />
                                </FormGroup>

                                {' '}
                                <FormGroup>
                                    <Label for="examplePassword">
                                        Password
                                    </Label>
                                    <Input
                                        id="examplePassword"
                                        name="password"
                                        // placeholder="Password"
                                        type="password"
                                    />
                                </FormGroup>
                                {' '}
                                <Button className='button'>
                                    Submit
                                </Button>
                            </Form>
                        </div>
                    </CardBody>
                </Card>
            </div>
        </>
    );
}

export default Login;