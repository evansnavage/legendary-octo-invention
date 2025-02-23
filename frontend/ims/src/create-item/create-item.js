import React, { useState } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, Form, FormGroup, Label, Input } from 'reactstrap';

function CreateItem(args) {
    const [modal, setModal] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        quantity: '',
        price: '',
        description: '',
        tags: ''
    });

    const toggle = () => setModal(!modal);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = () => {
        const filteredFormData = Object.fromEntries(
            Object.entries(formData).filter(([_, value]) => value !== '')
        );

        fetch('http://localhost:5000/create_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filteredFormData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            toggle(); // Close the modal on success
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    return (
        <div>
            <Button color="danger" onClick={toggle}>
                Create Item
            </Button>
            <Modal isOpen={modal} toggle={toggle} {...args}>
                <ModalBody>
                    <Form>
                        <FormGroup>
                            <Label for="name">Name</Label>
                            <Input type="text" name="name" id="name" value={formData.name} onChange={handleChange} />
                        </FormGroup>
                        <FormGroup>
                            <Label for="quantity">Quantity</Label>
                            <Input type="number" name="quantity" id="quantity" value={formData.quantity} onChange={handleChange} />
                        </FormGroup>
                        <FormGroup>
                            <Label for="price">Price</Label>
                            <Input type="number" name="price" id="price" value={formData.price} onChange={handleChange} />
                        </FormGroup>
                        <FormGroup>
                            <Label for="description">Description</Label>
                            <Input type="textarea" name="description" id="description" value={formData.description} onChange={handleChange} />
                        </FormGroup>
                        <FormGroup>
                            <Label for="tags">Tags</Label>
                            <Input type="text" name="tags" id="tags" value={formData.tags} onChange={handleChange} />
                        </FormGroup>
                    </Form>
                </ModalBody>
                <ModalFooter>
                    <Button color="primary" onClick={handleSubmit}>
                        Do Something
                    </Button>{' '}
                    <Button color="secondary" onClick={toggle}>
                        Cancel
                    </Button>
                </ModalFooter>
            </Modal>
        </div>
    );
}

export default CreateItem;