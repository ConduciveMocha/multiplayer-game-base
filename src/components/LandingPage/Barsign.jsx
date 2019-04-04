import React from 'react';
import {Link} from 'react-router-dom';
import './Barsign.css'
 const Barsign = (props) => {
    return(
        <div className="barsign-container">
            <div className="neon-text-container">
                <p className="neon-text-b">
                    B
                </p>
                <p className="neon-text-a">
                    A
                </p>
                <p className="neon-text-r">
                    R
                </p>
            </div>
            <p className="sim-text">Simulator</p>
            <div className="redirect-buttons">
                <Link to='/login'>
                    <button className="redirect-login">Login</button>
                </Link>
                <Link to='/register'>
                    <button className="redirect-register">Create Account</button>
                </Link>
            </div>
            
        </div>
    )
}
export default Barsign;