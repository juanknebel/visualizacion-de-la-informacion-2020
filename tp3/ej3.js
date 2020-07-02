{
  // 1. Creación de un área de dibujo (256x256 pixeles).
  //    Si lo consideran necesario, pueden modificar el tamaño del canvas.
  //    También es posible que necesiten más de una celda para resolverlo.
  const svg = d3.create("svg")
                .attr("width",config_ejc.width)
                .attr("height",config_ejc.height);
     
  var circles = svg.selectAll("g")
                    .data(circles_data_ejc)
                    .enter()
                    .append("g");

  circles.append("circle")
    .attr("cx", function(d) {return d.axis_x;} )
    .attr("cy", function(d) {return d.axis_y;} )
    .attr("r" , function(d) {return d.radius;} )
    .style("fill", function(d) { return d.color;});
  return svg.node();
}

config_ejc = {
  var dimmension = 17;
  var width = 1016;
  var height = 1011;
  var borderGap = width / dimmension / 10;
  var maxRadius = width / dimmension / 3.5;
  var distanceBetweenCircles = maxRadius*3.5;
  let config_ejc = {
    "dimmension": dimmension,
    "width": width,
    "height": height,
    "borderGap": borderGap,
    "maxRadius": maxRadius,
    "distanceBetweenCircles": distanceBetweenCircles
  };
  return config_ejc;
}

circles_data_ejc = { 

  var center = Math.floor(config_ejc.dimmension / 2);
  
  // Distance from (x, y) to (center, center).
  var distance = function(x, y) {
    return Math.sqrt(Math.pow(x - center, 2) + Math.pow(y - center, 2));
  }
  
  var radiusScale = function(distance) {
    if (distance == 0) {
      distance = 1; 
    }
    return config_ejc.maxRadius/distance;
  }
  
  //var max = distance(0, 0);
  
  //var radiusScale = d3.scalePow().exponent(0.2).domain([max, 0]).range([1,maxRadius]);
  
  var circlesData = [];
  
  for (var i = 0; i < config_ejc.dimmension; i++) {
    for (var j = 0; j < config_ejc.dimmension; j++) {
      var rad =  radiusScale(distance(i, j));
      var elem = { "axis_x":(j*config_ejc.distanceBetweenCircles) + config_ejc.borderGap, "axis_y": (i*config_ejc.distanceBetweenCircles) + config_ejc.borderGap, "radius": rad, "color": "black"};
      circlesData.push(elem);
    }
  }
  
  return circlesData;
}
