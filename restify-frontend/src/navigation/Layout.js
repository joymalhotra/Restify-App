import { Link, Outlet } from "react-router-dom";
import { Navbar, Container, Nav, NavDropdown } from "react-bootstrap"
import "./style.css";
import logo from '../assets/logo.png';


const Layout = () => {
  return <>
    <nav className="navbar navbar-light navbar-expand-lg">
    <Navbar.Brand>
      <img className="navbar-brand logo" src={logo} width="20" />
    </Navbar.Brand>



      <div className="collapse navbar-collapse" id="navbarSupportedContent">

        <ul className="navbar-nav mr-auto">
    
          <li className="nav-item active">
            <a className="nav-link" href="/homePage">Home <span className="sr-only">(current)</span></a>
          </li>
          <li className="nav-item active">

          <Link className="dropdown-item" to="/myRestaurant">My Restaurant</Link>
          </li>

          <li className="nav-item active">
            <a className="nav-link" href="/login">Feed <span className="sr-only">(current)</span></a>
          </li>

        </ul>
        <ul className="navbar-nav ml-auto">
          <li className="nav-item dropdown">
            <a className="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown"
              aria-haspopup="true" aria-expanded="false">
              <i className="fa fa-bell"></i>
            </a>
            <div className="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
              {/* <a className="dropdown-item" href="../Blog/blog.html"> <i className="fa-solid fa-user avatar"></i>Elon Tusk commented on your Blog Post</a>
              <div className="dropdown-divider"></div>
              <a className="dropdown-item" href="../Blog/blog.html"> <i className="fa-solid fa-user avatar"></i>Elon Tusk commented on your Blog Post</a>
              <div className="dropdown-divider"></div>
              <a className="dropdown-item" href="../Blog/blog.html"> <i className="fa-solid fa-user avatar"></i>Elon Tusk commented on your Blog Post</a> */}
            </div>
          </li>

          <li className="nav-item dropdown">
            <a className="nav-link dropdown-toggle" id="navbarDropdown" role="button" data-toggle="dropdown"
              aria-haspopup="true" aria-expanded="false">
              <i className="fa fa-user"></i>
            </a>
            <div className="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
              <Link className="dropdown-item" to="/login">Logout</Link>
              <div className="dropdown-divider"></div>
              <Link className="dropdown-item" to="/editProfile">Edit Profile</Link>
              <div className="dropdown-divider"></div>
              <Link className="dropdown-item" to="/editRestaurant">Edit Restaurant</Link>
            </div>
          </li>

        </ul>

      </div>
    </nav>

    <Outlet />
  </>
}

export default Layout