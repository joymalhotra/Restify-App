import React, {useState} from 'react';
import "./style.css";

const Slideshow = (props) => {
    const [current, setCurrent] = useState(0);
    const length = props.images.length;
    if (length <= 0){
        return null;
    }

    const nextSlide = () => {
        setCurrent(current === length - 1 ? 0: current + 1)
    };

    const prevSlide = () => {
        setCurrent(current === 0 ? length - 1: current - 1)
    };

    return (
    <>
        <div className='slider'>
            
            {props.images.map((image, index) => {

                return (
                    <div className={index === current ? 'slide active': 'slide'} key={index}>
                        {index === current && (<img src={image.image} alt ="none"/>)}
                    </div>
                )  
            })}

            <button id="left-arrow" className="btn shadow-none" type="button" onClick={prevSlide}>
                <i className="fas fa-caret-left"></i>
            </button>
            <button id="right-arrow" className="btn shadow-none" type="button" onClick={nextSlide}>
                <i className="fas fa-caret-right"></i>
            </button>
        </div>
        
    </>
    )
}

export default Slideshow;