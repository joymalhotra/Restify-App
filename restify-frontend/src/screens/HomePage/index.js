import React, { useEffect, useState } from "react";
import "./style.css"
import Input from "../../components/Input/index"
import BASE_URL from "../../urls"
import axios from "axios";

// create a homepage 
function HomePage(){

    // an array of restaurants and their corresponding IDs
    const [restaurants, setRestaurants] = useState([]);
    // query inputted by the user 
    const [query, setQuery] = useState({search:''});

    // run this data anytime the search is altered 
    useEffect(() => {
        axios({
            method: 'GET',
            url: BASE_URL + `/restaurants/search/${query.search}/`,
            headers: {
                'content-type': 'application/json'
            },
            data: {}
        })
        .then(res => {
            console.log(res)
              setRestaurants(res.data)
        })
    }, [query])
        

    return (
        // anytime user inputs value, set query to that value 
        <>
        <div className="searchPage">
        <Input 
               placeholder="enter address, name of restaurant, food"
               value={query.search}
               update={(value) => setQuery({search: value})}/>
                           {/* this is where we'll show the data result */}
                
                <div className="dataResult">
                {restaurants.map(restaurant => {
            
                    return <a class="vals" href={ '/restaurant/' + restaurant[1] +'/'}> {restaurant[0]}</a>
                })}
               </div>
               </div>
        
        </>
            

    )
        
}
export default HomePage;