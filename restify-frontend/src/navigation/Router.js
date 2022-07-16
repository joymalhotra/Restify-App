import {BrowserRouter, Route, Routes} from "react-router-dom";
import Login from "../screens/LoginScreen";
import Register from "../screens/RegisterScreen";
import EditProfile from "../screens/EditProfileScreen";
import Layout from "./Layout"
import MyRestaurant from "../screens/MyRestaurantScreen";
import CreateRestaurant from "../screens/CreateRestaurantScreen";
import EditRestaurant from "../screens/EditRestaurantScreen";
import Blog from "../screens/BlogScreen"
import Restaurant from "../screens/RestaurantScreen";
import HomePage from "../screens/HomePage";



const Router = () => {
  return (
      <BrowserRouter>
          <Routes>
              <Route path="/" element={<Layout />}>

              <Route index element={<Login />} />  
              <Route path="homPage" element={<HomePage />} />
              <Route path="login" element={<Login />} />
              <Route path="register" element={<Register />} />
              <Route path="editProfile" element={<EditProfile />} />
              <Route path="myRestaurant" element={<MyRestaurant />} />
              <Route path="createRestaurant" element={<CreateRestaurant />} />
              <Route path="editRestaurant" element={<EditRestaurant />} />
              <Route path="blogs/:id" element={<Blog />} />
              <Route path="restaurant/:id" element={<Restaurant />} />
              <Route path="homePage" element={<HomePage />} />

              </Route>
          </Routes>
      </BrowserRouter>
  )
}

export default Router