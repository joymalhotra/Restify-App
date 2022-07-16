import BASE_URL from "../../urls"
import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Container, Button } from "react-bootstrap";
import "./style.css";
import logo from '../../assets/logo.png';
import AuthInput from '../../components/AuthInput/index'
import axios from "axios";
import { Link, Redirect } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';




function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [phone_number, setPhoneNumber] = useState("");
  const [email, setEmail] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [password2, setPassword2] = useState("");
  const [errors, setErrors] = useState({})
  const [avatar, setAvatar] = useState(null);

  const navigate = useNavigate();


  useEffect(() => {
    // must clear the previous token 
    localStorage.removeItem('user_token')
  }, []);



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
    console.log(e)
    if (e.target.files[0]) {
      setAvatar(e.target.files[0]);
    }
  };


  const handleSubmit = (e) => {
    console.log(password, username)
    let formField = new FormData()

    formField.append("username", username)
    formField.append("password", password)
    formField.append("password2", password2)
    formField.append("email", email)
    formField.append("first_name", first_name)
    formField.append("last_name", last_name)
    formField.append("avatar", avatar)
    formField.append("phone_number", phone_number)

    axios({
      method: 'Post',
      url: BASE_URL + '/accounts/register/',
      headers: {
        'content-type': 'multipart/form-data'
      },
      data: formField
    }).then((res) => {
      setUsername("")
      setPassword("")
      setEmail("")
      setErrors({})
      setPhoneNumber("")
      setPassword2("")
      setFirstName("")
      setLastName("")

      navigate("/Login");


    }).catch((err) => {
      console.log(err.response.data)
      var errors_obj = err.response.data
      setErrors(errors_obj)
    })


    e.preventDefault();
    return false
  }


  return (<>
    <Container id="main-container">
      <div className="signup-form">
        <Form autoComplete="off" onSubmit={handleSubmit}>
          <h2>Sign Up</h2>
          <p className="lead">Please fill in all the required information</p>
          <div className="form-group">
            <div className="input-group">
              <span className="input-group-addon"><i className="fa fa-user"></i></span>
              <AuthInput type="text" value={username} name="username" placeholder="Username" update={setUsername} />
            </div>

          </div>
          <div className="form-group">
            <div className="input-group">
              <span className="input-group-addon"><i className="fa fa-signature"></i></span>
              <AuthInput type="text" value={first_name} name="first_name" placeholder="First Name" update={setFirstName} />
            </div>
          </div>

          <div className="form-group">
            <div className="input-group">
              <span className="input-group-addon"><i className="fa fa-signature"></i></span>
              <AuthInput type="text" value={last_name} name="first_name" placeholder="Last Name" update={setLastName} />
            </div>
          </div>
          <div className="form-group">
            <div className="input-group">
              <span className="input-group-addon"><i className="fa fa-envelope"></i></span>
              <AuthInput type="email" value={email} name="email" placeholder="Email Address" update={setEmail} />
            </div>
          </div>
          <div className="form-group">
            <div className="input-group">
              <span className="input-group-addon">
                <i className="fa fa-phone"></i>
              </span>
              <AuthInput type="tel" value={phone_number} name="phone_number" placeholder="Phone Number(eg.+19050126789)"
                pattern="\+1[0-9]{10}" update={setPhoneNumber} />
            </div>
          </div>
          <div className="form-group">
            <div className="input-group">
              <span className="input-group-addon"><i className="fa fa-lock"></i></span>
              <AuthInput type="password" value={password} name="password" placeholder="Password" update={setPassword} />
            </div>
          </div>
          <div className="form-group">
            <div className="input-group">
              <span className="input-group-addon">
                <i className="fa fa-lock"></i>
                <i className="fa fa-check"></i>
              </span>
              <AuthInput type="password" value={password2} name="confirm_password" placeholder="Confirm Password" update={setPassword2} />
            </div>
          </div>
          <div className="form-group">
            <label> Avatar <input name="attachments" type="file" onChange={onChangeAvatar} required/> </label>
          </div>
          <p className="small text-left error"> {objToString(errors)} </p>
          <div className="form-group">

            <Button type="submit" className="btn btn-primary btn-block btn-lg">Sign Up</Button>
          </div>
          <p className="small text-center">Already have an account?<br /><Link to="/login">Click here to signin</Link></p>
          <div id="logo-container">
            <img src={logo} id="logo" alt="Restify logo" />
          </div>
        </Form>
      </div>

    </Container>

  </>
  );
}

export default Register