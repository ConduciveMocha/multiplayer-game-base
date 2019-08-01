const makeDrawFunction = (drawFunction, ftnName) => (ctx, obj) => {
  try {
    ctx.save();
    drawFunction(ctx, obj);
    ctx.stroke();
    ctx.restore();
    return true;
  } catch (error) {
    console.error(`Error in ${ftnName}. Invalid arguments passed.`);
    console.debug(obj);
    return false;
  }
};

const drawRectangle = makeDrawFunction((ctx, obj) => {
  ctx.fillStyle = obj.color;
  ctx.fillRect(obj.x, obj.y, obj.width, obj.height);
}, "drawRectangle");

const drawCircle = makeDrawFunction((ctx, obj) => {
  ctx.fillStyle = obj.color;
  ctx.arc(obj.x, obj.y, obj.rad, 0, 2 * Math.PI);
}, "drawCircle");
