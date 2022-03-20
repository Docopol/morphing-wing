let x1 = 100;
let x2 = 300;
let level = 400 / 4 + 5;
let radius = 3;

function midpoint(x1, x2) {
  return (x1 + x2) / 2;
}

function iter(
  currentX,
  currentY,
  distance,
  previousX,
  previousY,
  ) {
    circle(currentX, currentY, radius);
    line(currentX, currentY, previousX, previousY);
    distance = distance / 2;
    if (currentY < 150) {
      iter(midpoint(currentX, currentX + distance), currentY + 10,
           distance,currentX,currentY);
      iter(midpoint(currentX, currentX - distance), currentY + 10, 
           distance,currentX,currentY);
    }
}

function setup() {
  createCanvas(400, 400);
  background(220);
  line(x1, height / 4, x2, height / 4);
  line(x1, height / 4 + 5, x1, height / 4 - 5);
  line(x2, height / 4 + 5, x2, height / 4 - 5);
  iter(midpoint(x1, x2), level, x2 - x1, midpoint(x1,x2), level);
}
