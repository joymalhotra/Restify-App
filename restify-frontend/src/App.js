import logo from './logo.svg';
import './App.css';
import axios from "axios";
import Router from "./navigation/Router"

//Setup default axios properties
axios.defaults.baseURL = "http://localhost:3000/";

function App() {
  return (
        <Router />
  );
}

export default App;
