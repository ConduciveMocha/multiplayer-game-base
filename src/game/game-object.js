import Footprint from './footprint';
import { throws } from 'assert';
import LoadStates from '../constants/LoadStates'
export const MoveEnum = {
    UP:{x:0, y:-1},
    DOWN: {x:0, y:1},
    LEFT: {x:-1, y:0},
    RIGHT: {x:1, y:0}
}






export class GameAsset {
    constructor(assetUrl, assetType, id=0){
        this.assetUrl = assetUrl;
        this.assetType = assetType;
        this.asset = null;
        this.assetUrl = assetUrl;
        this.id = id;
        this.gameObjectIds = []
        this.loadState=LoadStates.LOADING;
        this.error = '';
    }
    completed = (error='') => {this.loadState = error ? LoadStates.FAILED : LoadStates.SUCCESSFUL; this.error=error}
    setID = (newId) => {this.id=newId};

}


export class ImageAsset extends GameAsset {
    constructor(imageUrl,imageDim={}, id=0) {
        super(imageUrl, 'img',id=id);
        this.imageDim = imageDim;
        this.asset = new Image()
        this.asset.src = this.assetUrl;
        
    }

    initialize(cb) {
        this.asset.onload = cb;
    }
    completed = (error='') => {
        this.error = error;
        this.loadState = this.error ? LoadStates.FAILED : LoadStates.SUCCESSFUL;
    }
}





export  class GameObject {
    
    constructor(fp, pos,assetIds,id=0) {
        this.footprint = fp;
        this.pos = pos;
        this.assetIds = assetIds;
        this.id = id
    }

    move(direction) {
        let newPos = {x:this.pos.x+direction.x, y:this.pos.y + direction.y}
        
        // Add Boundary Check here

        //

        this.pos = newPos;
    }

    away(direction) {
        let newPos = {x:this.pos.x-direction.x, y:this.pos.y-direction.y}
        // Add Boundary Check here

        //

        this.pos = newPos;
    }

    checkCollision = (other)=> other.id === this.id ? false : this.footprint.intersect(other.footprint);
}


