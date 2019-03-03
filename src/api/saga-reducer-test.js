import {ImageAsset} from '../game/game-object';
import testsprite from  '../assets/player-sprites/sprite1_front.png';
import testbg from '../assets/backgrounds/test_background.jpg';
import Footprint from '../game/footprint';
const bgFootprint = new Footprint({x:20,y:15});
const objs = [
    
   new ImageAsset(testsprite),
   new ImageAsset(testbg)
]

export default objs;