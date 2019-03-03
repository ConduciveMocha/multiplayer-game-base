
// Object that represents a game object's footprint
export default class Footprint{ 
    // Default constructor create empty footprint
    constructor(dim={x:0,y:0}){
        this.dim = dim;
        this.arr = [...Array(dim.y)].map(x=>Array(dim.x).fill(0))
    }

    
    // Create Footprint from array
    static fromArray(arr){
        let newFootprint = new Footprint({x:arr[0].length, y:arr.length});
        for(let i = 0; i < newFootprint.dim.y; i++)
            for(let j = 0; j < newFootprint.dim.x; j++) {
                if(arr[i][j] === 1) 
                    newFootprint.arr[i][j] = 1;
                else if (arr[i][j] !== 0) 
                    throw Error('Invalid Array Passed');
            }
        return newFootprint;
    }
    // Create a footprint, filled with 1's of a given size;
    static filledFootprint(dim) {
        let newFootprint = new Footprint(dim);
        newFootprint.arr = [...Array(dim.y)].map(x=>Array(dim.x).fill(1));
        return newFootprint;
    }
    // Slices the footprint along x direction;
    sliceX(start, end=this.dim.x){
        return Footprint.fromArray(this.arr.map(x=>x.slice(start,end)))
    }
    // Slice along y
    sliceY(start,end=this.dim.y) {
        return Footprint.fromArray(this.arr.slice(start,end))
    }

    // Functions to pad the footprint with 0's
    extendX = (n) =>{
        this.arr.map(x=>x.concat(Array(n).fill(0)));
        this.dim.x += n;
    }
    prependX = (n) => {
        this.arr.map(x=>Array(n).fill(0).concat(x));
        this.dim.x+=n;
    };
    extendY = (n) => {
        this.arr.concat([...Array(n)].map(x=>Array(this.dim.x).fill(0)));
        this.dim.y+=n;}
    prependY = (n) => {
        [...Array(n)].map(x=>Array(this.dim.x).fill(0)).concat(this.arr);
        this.dim.y+=n;
    }


    // Checks if two Footprints intersect
    intersect(other) {
        if(this.dim.x !== other.dim.x || this.dim.y !== other.dim.y) 
            throw new Error("Arrays must be same shape");
        for(let i =0; i < this.dim.y;i++) 
            for(let j=0; j<this.dim.x;j++)
                if(this.arr[i][j] && other.arr[i][j]) return true;

        return false;
    }

    // Merges the two Footprints. If allowIntersect is false, intersect will be run on the
    // two footprints and if it returns true, an error will be thrown.
    merge(other, allowIntersect=true) {
        if(this.dim.x !== other.dim.x || this.dim.y !== other.dim.y) 
            throw new Error("Arrays must be same shape");
        if(!allowIntersect && this.intersect(other))
            throw new Error("Arrays cannot intersect if allowIntersect is true");
        let fpArr = [[],[]];
        for(let i =0; i < this.dim.y; i++) 
            for(let j=0; j < this.dim.x; j++)
                fpArr[i][j] = (this.arr[i][j] || other.arr[i][j]) ? 1 : 0;
        return Footprint.fromArray(fpArr);   
    }

}



