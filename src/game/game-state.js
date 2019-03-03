import {MoveEnum} from './game-object';
export default class GameState{
    constructor(dim={x:20,y:15},background,player, environmentObjects, playerObjects) {
        this.dim = dim;
        this.background= background;
        this.player = player;
        this.environmentObjects = environmentObjects;
        this.playerObjects = playerObjects;
    }
    // TODO: Reimplement with R-Tree cause they look cool
    checkMovement(direction) {
        this.player.move(direction);
        for(let otherP in this.playerObjects) 
            if(otherP.checkCollision(this.player)) {
                this.player.away(direction)
                return false;
            }
        return true;
    }
}