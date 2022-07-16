import React from 'react';
import "./style.css";
import BASE_URL from "../../urls";
import axios from "axios";


class MenuItem extends React.Component {

    handleDelete = (e) => {
        const token = localStorage.getItem("user_token");
        axios({
          method: 'DELETE',
          url: BASE_URL + `/restaurants/menu/${e.target.id}/delete/`,
          headers: {
            'authorization': 'Bearer ' + token,
            'content-type': 'application/json'
          },
          data: {}
        }).then((res) => {
            console.log(`Menu item ${e.target.id} deleted`);
            document.getElementById(e.target.id).parentNode.remove();
        }).catch((err) => {
            if (err.response) {
                console.log(err.response.data);
            } else if (err.request){
                console.log(err.request);
            } else {
                console.log(err.message);
            }
        })

        return false
    }

    render() {
        return <>
            <div >
                <h4>{this.props.name}</h4> {this.props.canEdit && <i id={this.props.itemId} className="fas fa-minus-circle" onClick={e => this.handleDelete(e)}></i>} <h5>${this.props.price}</h5>
                <p> {this.props.description}</p>
            </div>
            
        </>
      
    }
}

export default MenuItem;