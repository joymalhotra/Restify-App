import BASE_URL from "../../urls"
import React, { useState, useEffect} from "react";
import Form from "react-bootstrap/Form";
import { Container, Button } from "react-bootstrap";
import "./style.css";
import logo from '../../assets/logo.png';
import AuthInput from '../../components/AuthInput/index'
import axios from "axios";
import { Link, Redirect } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';



function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("")

  useEffect(() => {
    // must clear the previous token in 
    localStorage.removeItem('user_token')

  }, []);


  const storeToken = (value) => {
    try {
      localStorage.setItem('user_token', value)
    } catch (e) {
      // saving error
    }
  }



  const handleSubmit = (e) => {
    // console.log(password, username)

    if (!username || !password) {
      setError("USERNAME AND PASSWORD CAN'T BE BLANK")
    }

    else {
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
        console.log(res.data.access)
        storeToken(res.data.access)
        setError("") // no error
        setUsername("")
        setPassword("")
        navigate("/homPage")
      }).catch((err) => {
        setError("INCORRECT USERNAME OR PASSWORD")
        setUsername("")
        setPassword("")
      })

    }

    e.preventDefault();
    return false
  }


  return (<>
    <Container id="main-container">
      <div className="signup-form">
        <Form autoComplete="off" onSubmit={handleSubmit}>
          <h2>Sign In</h2>
          <p className="lead">Please fill in all the required information to access the website</p>
          <div className="form-group">
            <div className="input-group">
              <span className="input-group-addon"><i className="fa fa-user"></i></span>
              <AuthInput type="text" name="username" placeholder="Enter Username or Email"
                value={username} update={setUsername}
              />
            </div>
          </div>

          <div className="form-group">
            <div className="input-group">
              <span className="input-group-addon"><i className="fa fa-lock"></i></span>
              <AuthInput type="password" name="password" placeholder="Enter Password"
                value={password} update={setPassword}
              />
            </div>
          </div>

          <p className="small text-left error"> {error} </p>

          <div className="form-group">

            <Button type="submit" className="btn btn-primary btn-block btn-lg" id="signin">
              Sign In
            </Button>
          </div>
          <p className="small text-center">Don't have an account?<br /> <Link id ="loginLink" to="/register">Click here to signup</Link>
          </p>
          <div id="logo-container">
            <img src={logo} id="logo" alt="Restify logo" />
          </div>
        </Form>
      </div>
    </Container>
  </>

  );
}

export default Login