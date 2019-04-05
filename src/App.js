import React, { Component } from 'react';

import {BrowserRouter as Router, Route} from 'react-router-dom';


import Barsign from './components/LandingPage/Barsign'
import LoginScreen from './components/LoginScreen'
import RegistrationScreen from './components/RegistrationScreen'
import GamePage from './components/GamePage/GamePage'
import Messenger from './components/Messenger'
import store from './store'
import {Provider} from 'react-redux'
import './App.css';

class App extends Component {
  render() {
    return ( 
      
      <Provider store={store}>
      {/* <Router>
        
        <div className="App">
          <Route exact path='/' component={Barsign} />
          <Route path='/login' component={LoginScreen}/>
          <Route path='/register' component={RegistrationScreen} />
          <Route path='/game' component={GamePage}/>
        </div>

      </Router> */}
       <Messenger messageThreads={[]}/> 
      </Provider>

      
    );
  }
}



export default (App);
    