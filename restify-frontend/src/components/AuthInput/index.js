import React from 'react';
import "./style.css";


class AuthInput extends React.Component {
    render(){
        const {placeholder, name, value, type, update, pattern, readOnly} = this.props
        return <>
            <input className="form-control" type={type} name={name} pattern={pattern} placeholder={placeholder}
                value={value} onChange={event => update(event.target.value)}
                required readOnly={readOnly}/>
        </>
    }
}

export default AuthInput;
