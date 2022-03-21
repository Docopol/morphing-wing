let x1 = 100;
let x2 = 300;
let level = 400 / 4 + 5;
let radius = 3;

function midpoint(x1, x2) {
  return (x1 + x2) / 2;
}

function func(slope, x1, y1, x) {
  return slope * (x - x1) + y1;
}

function iter(currentX, currentY, distance, previousX, previousY) {
  circle(currentX, currentY, radius);
  x15 = midpoint(currentX, previousX);
  y15 = midpoint(currentY, previousY);
  circle(x15, y15, radius);
  slope = (currentY - previousY) / (currentX - previousX);
  tangent = -1 / slope;
  line(currentX, currentY, previousX, previousY);
  line(x15, y15, currentX, func(tangent, x15, y15, currentX));
  line(x15, y15, previousX, func(tangent, x15, y15, previousX));
  distance = distance / 2;
  if (currentY < 135) {
    iter(
      midpoint(currentX, currentX + distance), currentY + 10, distance, currentX, currentY);
    iter(
      midpoint(currentX, currentX - distance), currentY + 10, distance, currentX, currentY);
  }
}

function setup() {
  createCanvas(400, 400);
  background(220);
  line(x1, height / 4, x2, height / 4);
  line(x1, height / 4 + 5, x1, height / 4 - 5);
  line(x2, height / 4 + 5, x2, height / 4 - 5);
  iter(midpoint(x1, x2), level, x2 - x1, midpoint(x1, x2), level);
}
