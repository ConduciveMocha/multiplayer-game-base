import React, { Component } from 'react';
import {Provider} from 'react-redux';
import GameScreen from './components/GameScreen'
import DebugLoader from './components/DebugLoader'

import store from './store'

import './App.css';


class App extends Component {
  render() {
    return ( <Provider store={store}>
      <DebugLoader />
      <GameScreen width={600} height={450}/>}
      </Provider>
    );
  }
}

export default App;
