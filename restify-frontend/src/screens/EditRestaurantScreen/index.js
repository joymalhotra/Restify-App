import BASE_URL from "../../urls"
import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Container, Button } from "react-bootstrap";
import "./style.css";
import AuthInput from '../../components/AuthInput/index'
import axios from "axios";
import { useNavigate } from 'react-router-dom';

function EditRestaurant(){
    
    const [restaurantId, setRestaurantId] = useState(0);
    const [name, setName] = useState("");
    const [address, setAddress] = useState("");
    const [postalCode, setPostalCode] = useState("");
    const [website, setWebsite] = useState("");
    const [phone, setPhone] = useState("");
    const [description, setDescription] = useState("");
    const [logo, setLogo] = useState(undefined);
    const [imgData, setImgData] = useState(null);

    const navigate = useNavigate();

    function fetchRestaurantInfo() {
        const token = localStorage.getItem("user_token");
        axios({

            method: 'GET',
            url: BASE_URL + '/restaurants/my-restaurant/',
            headers: {
                'authorization': 'Bearer ' + token,
                'content-type': 'application/json'
            },
            data: {}

        }).then((res) => {
            setRestaurantId(res.data["id"])
            setName(res.data["name"])
            setAddress(res.data["address"])
            setPostalCode(res.data["postal_code"])
            setWebsite(res.data["website"])
            setPhone(res.data["phone_number"])
            setDescription(res.data["description"])
            setLogo(res.data["logo"])
        }).catch((err) => {
            if (err.response) {
                console.log(err.response.data);
            } else if (err.request){
                console.log(err.request);
            } else {
                console.log(err.message);
            }
        });
        return 
    }


    const handleSubmit = (e) => {
        const token = localStorage.getItem("user_token");
        let formField = new FormData()
        formField.append("name", name)
        formField.append("address", address)
        formField.append("postal_code", postalCode)
        formField.append("website", website)
        formField.append("phone_number", phone)
        formField.append("description", description)
        formField.append("logo", logo)

        axios({
          method: 'PUT',
          url: BASE_URL + '/restaurants/edit/',
          headers: {
            'authorization': 'Bearer ' + token,
            'content-type': 'multipart/form-data',
          },
          data: formField
        }).then((res) => {
            
            navigate("/myRestaurant");
    
        }).catch((err) => {
            if (err.response) {
                console.log(err.response.data);
            } else if (err.request){
                console.log(err.request);
            } else {
                console.log(err.message);
            }
        })
    
        e.preventDefault();
        return false
    }

    const onChangeLogo = (e) => {
        if (e.target.files[0]) {
            setLogo(e.target.files[0]);
            const reader = new FileReader();
            reader.addEventListener("load", () => {
                setImgData(reader.result);
            });
            reader.readAsDataURL(e.target.files[0]);
        }
    };

    useEffect(() => {
        fetchRestaurantInfo();
        document.title = "Edit Restaurant"
    }, []);

    return <>
        <Container className="container-xl px-4 mt-4">
            <hr className="mt-0 mb-4" />
            <div className="row">
                <div className="col-xl-4">
                <div className="card mb-4 mb-xl-0">
                    <div className="card-header">Restaurant Logo</div>
                    <div className="card-body text-center">
                      {imgData ? (
                      <div>
                        <img id="logo" src={imgData} alt="" />
                      </div>
                    ) : (
                      <div>
                        <img id="logo" src={logo} alt=""/>
                      </div>
                    )}  
                    
                    <div className="small font-italic text-muted mb-4">JPG or PNG no larger than 5 MB</div>
                    <label><input type="file" accept="image/png" onChange={onChangeLogo} required /> </label>

                    </div>
                </div>
                </div>
                <div className="col-xl-8">
                <div className="card mb-4">
                    <div className="card-header">Restaurant Information</div>
                    <div className="card-body">
                    <Form autoComplete="off" onSubmit={handleSubmit}>

                        <div className="mb-3">
                        <label className="small mb-1" >Restaurant Name</label>
                        <AuthInput type="text" placeholder="Name" name="name" value={name} update={setName} />
                        </div>
                        <div className="row gx-3 mb-3">

                        <div className="col-md-6">
                            <label className="small mb-1" >Address </label>
                            <AuthInput type="text" placeholder="Address" name="address" value={address} update={setAddress} />
                        </div>

                        <div className="col-md-6">
                            <label className="small mb-1" >Postal Code</label>
                            <AuthInput type="text" placeholder="Postal Code" name="postal_code" value={postalCode} update={setPostalCode} />
                        </div>
                        </div>
                        <div className="row gx-3 mb-3">

                        <div className="col-md-6">
                            <label className="small mb-1" >Website</label>
                            <AuthInput type="url" placeholder="Enter your website url" name="email" value={website} update={setWebsite} />
                        </div>

                        <div className="col-md-6">
                            <label className="small mb-1" >Phone number</label>
                            <AuthInput type="tel" placeholder="Enter your phone number" name="phone_number"value={phone} update={setPhone} />
                        </div>
                        </div>
                        <div className="row gx-3 mb-3">

                        <div className="mb-3">
                            <label className="small mb-1" >Description</label>
                            <textarea className="form-control" placeholder="Describe your restaurant!" name="description" value={description} onChange={e => setDescription(e.target.value)} rows="10"></textarea>
                        </div>
                        </div>

                        <button className="btn" type="submit">Save changes</button>
            
                    </Form >
                    </div>
                </div>
                </div>
            </div>
        </Container>

    
    </>
}

export default EditRestaurant;