import BASE_URL from "../../urls"
import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Container, Button } from "react-bootstrap";
import "./style.css";
import logo from '../../assets/logo.png';
import AuthInput from '../../components/AuthInput/index'
import axios from "axios";
import { useNavigate } from 'react-router-dom';



function EditProfile() {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [phone_number, setPhoneNumber] = useState("");
  const [email, setEmail] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [avatar, setAvatar] = useState("");
  const [avatarBlob, setAvatarBlob] = useState("")

  const [errors, setErrors] = useState({})
  const [token, setToken] = useState("")

  const navigate = useNavigate();


  function objToString(obj) {
    var str = '';
    for (var p in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, p)) {
        str += p.toUpperCase() + ': ' + obj[p];
      }
    }
    return str;
  }

  const onChangeAvatar = (e) => {
    if (e.target.files[0]) {
      setAvatar(e.target.files[0]);
    }
  };
  const handleSubmit = (e) => {

    let formField = new FormData()

    formField.append("username", username)
    formField.append("password", password)
    formField.append("email", email)
    formField.append("first_name", first_name)
    formField.append("last_name", last_name)
    formField.append("avatar", avatar)
    formField.append("phone_number", phone_number)

    // first have to verfify that the password entered is correct

    axios({
      method: 'Post',
      url: BASE_URL + '/accounts/login/',
      headers: {
        'content-type': 'application/json'
      },
      data: {
        username: username,
        password: password
      }
    }).then((res) => {
      axios({
        method: 'Put',
        url: BASE_URL + '/accounts/editProfile/',
        headers: {
          'authorization': 'Bearer ' + token,
          'content-type': 'multipart/form-data'
        },
        data: formField
      }).then((res) => {
        fetchProfileInfo()
        setErrors({})
        setPassword("")

      }).catch((err) => {
        var errors_obj = err.response.data
        setErrors(errors_obj)
      })

    }).catch((err) => {
      var errors_obj = err.response.data
      setErrors(errors_obj)      
      setPassword("")
    })




    e.preventDefault();
    return false
  }



  function fetchProfileInfo() {
    if (!localStorage.getItem("user_token")) {
      console.log("no token")
      navigate("/Login");

    }
    const token = localStorage.getItem("user_token");
    setToken(token)

    axios({
      method: 'Get',
      url: BASE_URL + '/accounts/profile/',
      headers: {
        'authorization': 'Bearer ' + token,
        'content-type': 'application/json'
      },
      data: {
      }
    }).then((res) => {
      setUsername(res.data["username"])
      setEmail(res.data["email"])
      setPhoneNumber(res.data["user_profile"]["phone_number"])
      setFirstName(res.data["first_name"])
      setLastName(res.data["last_name"])

      axios({
        method: 'Get',
        url: res.data.user_profile.avatar,
        headers: {
          'authorization': 'Bearer ' + token,
        },
        data: {
        },
        responseType: 'blob'
      }).then((res) => {
        setAvatarBlob(URL.createObjectURL(res.data))
        setAvatar(new File([res.data], "avatar.png", { type: "image/png" }))


      }).catch((err) => {
        console.log(err)
        navigate("/Login");

      })



    }).catch((err) => {
      if (err.resonse) {
        var errors_obj = err.response.data
        setErrors(errors_obj)
      }
      else {
        // the only possible error is 401 in which case we should send user to login page
        navigate("/Login");
      }

    })

    return
  }


  useEffect(() => {
    fetchProfileInfo()
  }, []);


  return (<>
    <Container className="container-xl px-4 mt-4">
      <hr className="mt-0 mb-4" />
      <div className="row">
        <div className="col-xl-4">
          <div className="card mb-4 mb-xl-0">
            <div className="card-header">Avatar</div>
            <div className="card-body text-center">
              <div >
                <img id="avatar" className="rounded-circle mb-2"
                  src={avatarBlob} alt="" />
              </div>
              <div className="small font-italic text-muted mb-4">JPG or PNG no larger than 5 MB</div>
              <label> Avatar <input name="attachments" type="file" accept="image/png" onChange={onChangeAvatar} required /> </label>
            </div>
          </div>
        </div>
        <div className="col-xl-8">
          <div className="card mb-4">
            <div className="card-header">Profile Information</div>
            <div className="card-body">
              <Form autoComplete="off" onSubmit={handleSubmit}>

                <div className="mb-3">
                  <label className="small mb-1" >Username</label>
                  <AuthInput type="text" placeholder="Username" name="username" value={username} update={setUsername} readOnly />
                </div>
                <div className="row gx-3 mb-3">

                  <div className="col-md-6">
                    <label className="small mb-1" >First name</label>
                    <AuthInput type="text" placeholder="First name" name="firstname" value={first_name} update={setFirstName} required />
                  </div>

                  <div className="col-md-6">
                    <label className="small mb-1" >Last name</label>
                    <AuthInput type="text" placeholder="Last name" name="lastname" value={last_name} update={setLastName} required />
                  </div>
                </div>
                <div className="row gx-3 mb-3">

                  <div className="col-md-6">
                    <label className="small mb-1" >Email</label>
                    <AuthInput type="email" placeholder="Enter your email" name="email" value={email} update={setEmail} required />
                  </div>

                  <div className="col-md-6">
                    <label className="small mb-1" >Phone number</label>
                    <AuthInput type="tel" placeholder="Enter your phone number" name="phonenumber"
                      value={phone_number} update={setPhoneNumber} pattern="\+1[0-9]{10}" required />
                  </div>
                </div>
                <div className="row gx-3 mb-3">

                  <div className="col-ml-6">
                    <label className="small mb-1" >Password</label>
                    <AuthInput type="password" placeholder="Enter password to save changes" name="password" value={password} update={setPassword} required />
                  </div>
                </div>

                <button className="btn" type="submit">Save changes</button>
                <p className="small text-left error"> {objToString(errors)} </p>

              </Form >
            </div>
          </div>
        </div>
      </div>
    </Container>

  </>
  );

}

export default EditProfile