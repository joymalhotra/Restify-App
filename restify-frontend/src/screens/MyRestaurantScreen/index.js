import { useState,useEffect } from "react";
import BASE_URL from "../../urls";
import axios from "axios";
import "./style.css";
import { Button, Form } from "react-bootstrap";
import AuthInput from '../../components/AuthInput/index'
import Popup from "../../components/Popup";
import MenuItem from "../../components/MenuItem";
import Slideshow from "../../components/Slideshow";
import { useNavigate } from 'react-router-dom';

function MyRestaurant() {
    
    const [restaurantId, setRestaurantId] = useState(0);
    const [name, setName] = useState("");
    const [address, setAddress] = useState("");
    const [postalCode, setPostalCode] = useState("");
    const [website, setWebsite] = useState("");
    const [phone, setPhone] = useState("");
    const [description, setDescription] = useState("");
    const [logo, setLogo] = useState(undefined);
    const [menuPopup, setMenuPopup] = useState(false);
    const [imagePopup, setImagePopup] = useState(false);
    const [itemName, setItemName] = useState("");
    const [itemPrice, setItemPrice] = useState("");
    const [itemDescription, setItemDescription] = useState("");
    const [followCount, setFollowCount] = useState(0);
    const [likeCount, setLikeCount] = useState(0);
    const [menu, setMenu] = useState([]);
    const [image, setImage] = useState(undefined);
    const [images, setImages] = useState([]);
    const [followStatus, setFollowStatus] = useState(false);
    const [likeStatus, setLikeStatus] = useState(false);

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

    function fetchFollowCount() {
        axios({
            method: 'GET',
            url: BASE_URL + `/restaurants/numberfollowers/${restaurantId}/`,
            headers: {
                'content-type': 'application/json'
            },
            data: {}
        }).then((res) => {
            setFollowCount(res.data["Number Followers"])
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

    function fetchLikeCount() {
        axios({
            method: 'GET',
            url: BASE_URL + `/restaurants/numberlikes/${restaurantId}/`,
            headers: {
                'content-type': 'application/json'
            },
            data: {}
        }).then((res) => {
            setLikeCount(res.data["Number Liked"])
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

    function fetchMenu() {
        const token = localStorage.getItem("user_token");
        axios({
            method: 'GET',
            url: BASE_URL + `/restaurants/${restaurantId}/menu/view/`,
            headers: {
                'authorization': 'Bearer ' + token,
                'content-type': 'application/json'
            },
            data: {}
        }).then((res) => {
            setMenu(res.data);
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

    function fetchImages() {
        axios({
            method: 'GET',
            url: BASE_URL + `/restaurants/${restaurantId}/image/all/`,
            headers: {
                'content-type': 'application/json'
            },
            data: {}
        }).then((res) => {
            setImages(res.data);
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

    function fetchFollowStatus() {
        const token = localStorage.getItem("user_token");
        axios({
            method: 'GET',
            url: BASE_URL + `/restaurants/followed/${restaurantId}/`,
            headers: {
                'authorization': 'Bearer ' + token,
                'content-type': 'application/json'
            },
            data: {}
        }).then((res) => {
            setFollowStatus(res.data["Restaurant Followed"] === 'True')
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

    function fetchLikeStatus() {
        const token = localStorage.getItem("user_token");
        axios({
            method: 'GET',
            url: BASE_URL + `/restaurants/liked/${restaurantId}/`,
            headers: {
                'authorization': 'Bearer ' + token,
                'content-type': 'application/json'
            },
            data: {}
        }).then((res) => {
            setLikeStatus(res.data["Restaurant Liked"] === 'True')
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

    const handleMenuSubmit = (e) => {
        const token = localStorage.getItem("user_token");
        axios({
          method: 'POST',
          url: BASE_URL + '/restaurants/menu/add/',
          headers: {
            'authorization': 'Bearer ' + token,
            'content-type': 'application/json'
          },
          data: {
            name: itemName,
            price: itemPrice,
            description: itemDescription,
          }
        }).then((res) => {
            console.log("Menu item created");
            setMenuPopup(false);
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


    const handleImageSubmit = (e) => {
        const token = localStorage.getItem("user_token");
        let formField = new FormData();
        formField.append("image", image);
        axios({
          method: 'POST',
          url: BASE_URL + '/restaurants/image/add/',
          headers: {
            'authorization': 'Bearer ' + token,
            'content-type': 'multipart/form-data'
          },
          data: formField
        }).then((res) => {
            console.log("Image added");
            setImagePopup(false);
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

    const handleFollow = (e) => {
        const token = localStorage.getItem("user_token");
        axios({
          method: 'POST',
          url: BASE_URL + '/restaurants/follow/',
          headers: {
            'authorization': 'Bearer ' + token,
            'content-type': 'application/json'
          },
          data: {
            restaurant: restaurantId
          }
        }).then((res) => {
            setFollowStatus(true);
            console.log("Restaurant Followed");
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

    const handleLike = (e) => {
        const token = localStorage.getItem("user_token");
        axios({
          method: 'POST',
          url: BASE_URL + '/restaurants/like/',
          headers: {
            'authorization': 'Bearer ' + token,
            'content-type': 'application/json'
          },
          data: {
            restaurant: restaurantId
          }
        }).then((res) => {
            setLikeStatus(true)
            console.log("Restaurant Liked");
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

    const handleUnfollow = (e) => {
        const token = localStorage.getItem("user_token");
        axios({
          method: 'DELETE',
          url: BASE_URL + `/restaurants/${restaurantId}/unfollow/`,
          headers: {
            'authorization': 'Bearer ' + token,
            'content-type': 'application/json'
          },
          data: {
            restaurant: restaurantId
          }
        }).then((res) => {
            setFollowStatus(false);
            console.log("Restaurant Unfollowed");
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

    const handleUnlike = (e) => {
        const token = localStorage.getItem("user_token");
        axios({
          method: 'DELETE',
          url: BASE_URL + `/restaurants/${restaurantId}/unlike/`,
          headers: {
            'authorization': 'Bearer ' + token,
            'content-type': 'application/json'
          },
          data: {
            restaurant: restaurantId
          }
        }).then((res) => {
            setLikeStatus(false);
            console.log("Restaurant Unliked");
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

    const onChangeImage = (e) => {
        if (e.target.files[0]) {
            setImage(e.target.files[0]);
        }
    }

    useEffect(() => {
        fetchRestaurantInfo();
    }, []);

    useEffect(() => {
        fetchFollowCount();
        fetchLikeCount();
        fetchFollowStatus();
        fetchLikeStatus();
    }, [restaurantId, followStatus, likeStatus]);

    useEffect(() => {
        fetchMenu();
        fetchImages();
    }, [restaurantId, menuPopup, imagePopup]);

    if (!restaurantId){
        return (<>
            <div className="header">
                <h1> Create a restaurant.</h1>
                <button className="btn shadow-none" onClick={navigate("/createRestaurant")}>
                    Create a restaurant
                </button>
            </div>
        </>)
    }

    return (<>
        <div className="header">
          <img id="res-logo" src={logo} alt="" />
          <h1>
            {name}
          </h1>

          {followStatus ? (
          <button className="btn shadow-none" type="button" onClick={handleUnfollow}>
            <i className="fas fa-heart"></i> Following
          </button>) : (
          <button className="btn shadow-none" type="button" onClick={handleFollow}>
            <i className="far fa-heart"></i> Follow
          </button>
          )}
          
          {likeStatus ? (
          <button className="btn shadow-none" type="button" onClick={handleUnlike}>
            <i className="fas fa-thumbs-up"></i> Liked
          </button>) : (
          <button className="btn shadow-none" type="button" onClick={handleLike}>
            <i className="far fa-thumbs-up"></i> Like
          </button>
          )}

        </div>
        
        <div className="flex-container">
        
            <div className="left-column">
                <div className="general">
                    <h7> <i className="fas fa-map-marker-alt"></i> {address}, {postalCode}</h7> <br/> 
                    <i className="fas fa-globe-americas"></i> <a href={website}>
                       {website}
                    </a> <br/> 
                    <h7> <i className="fas fa-phone-alt"></i> {phone}</h7> <br/> 
                    <h7> <i className="fas fa-heart"></i> {followCount} people follow this</h7> <br/> 
                    <h7> <i className="fas fa-thumbs-up"></i> {likeCount} people like this</h7>
                </div>
              

                <hr/>
                <div id="description">
                    <h2> From the Business </h2>
                    <p>{description}</p>
                    
                </div><hr/>
                
                <div id="menu">
                    
                  <h2>Menu</h2>
                  
                  {menu.map((item) => {
                    return <MenuItem key={item.id} itemId={item.id} name={item.name} price={item.price} description={item.description} canEdit={true}/>
                  })}

                  <button className="btn shadow-none" type="button" onClick={() => setMenuPopup(true)}>
                    <i className="fas fa-plus"></i> Add Menu Item
                  </button>

                  <Popup trigger={menuPopup} setTrigger={setMenuPopup}>
                    <h3>Add a menu item</h3>
                    <Form autoComplete="off" onSubmit={handleMenuSubmit}>
                    <label className="small mb-1" >Name</label>
                    <AuthInput type="text" placeholder="Name" name="item-name" update={setItemName} />
                    <label className="small mb-1" >Price</label>
                    <AuthInput type="text" placeholder="Price" name="item-price" update={setItemPrice} />
                    <label className="small mb-1" >Description</label>
                    <AuthInput type="text" placeholder="Describe your product!" name="item-description" update={setItemDescription} />
                    <br/>
                    <button className="btn shadow-none" > Add</button>
                    </Form> 
                    
                  </Popup>

                </div><hr/>
                
                <div id="blog">
                  <a href="../UpdateBlogs/blogs.html" className="btn btn-lg">
                    <i className="fas fa-rss"></i> Blog posts
                  </a>
                </div><hr/>
                
            </div>

            <div className="right-column">
                
                <Slideshow images={images}></Slideshow>
                  <br/><br/>
                <button id="image-btn" className="btn shadow-none" type="button" onClick={() => setImagePopup(true)}>
                    <i className="fas fa-plus"></i> Add Image
                  </button>

                  <Popup trigger={imagePopup} setTrigger={setImagePopup}>
                    <h3>Add an image</h3>
                    <Form autoComplete="off" onSubmit={handleImageSubmit}>
                    <label className="small mb-1" >Image</label>
                    <input type="file" name="image" className="form-control" onChange={onChangeImage} required/>
                    <br/>
                    <button className="btn shadow-none"> Add</button>
                    </Form> 
                    
                  </Popup>
            </div>
        </div>
          
    </>);
}

export default MyRestaurant;