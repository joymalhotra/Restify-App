import React from 'react';

class Input extends React.Component {
    render(){
        const {placeholder, update, value} = this.props
        return <>
        <div>      
                   <input type="text"
                   placeholder={placeholder}
                   value={value}
                   onChange={event => update(event.target.value)}
                   style={{width: 700, height: 80, fontSize: '2em'}}
                   
            /></div>

            
                           

        </>
    }
}

export default Input;
