{
  // 1. Creación de un área de dibujo (256x256 pixeles).
  //    Si lo consideran necesario, pueden modificar el tamaño del canvas.
  //    También es posible que necesiten más de una celda para resolverlo.

  const svg = d3.create("svg")
                .attr("width", config_ejb.width)
                .attr("height", config_ejb.height);
  
  var circles = svg.selectAll("g")
                    .data(circles_data_ejb)
                    .enter()
                    .append("g");
  
  circles.append("circle")
    .attr("cx", function(d) {return d.axis_x;} )
    .attr("cy", function(d) {return d.axis_y;} )
    .attr("r" , function(d) {return d.radius;} )
    .style("fill", function(d) { return d.color;});
  
  // n. Retornamos el canvas.
  return svg.node(); 
}

config_ejb = {
  var config_ejb = {
    "width": 267,
    "height": 267,
    "dimmension": 17
  };
  return config_ejb;
}

circles_data_ejb = {
  var colorIndex = config_ejb.dimmension*config_ejb.dimmension;
  var circlesData = [];
  
  for (var i = 0; i < config_ejb.dimmension; i++) {
    for (var j = 0; j < config_ejb.dimmension; j++) {
      var color = `rgb(${1+i*267/config_ejb.dimmension}, ${1+j*267/config_ejb.dimmension}, 0)`
      var elem = { "axis_x":(i*15)+10, "axis_y": (j*15)+10, "radius": 5, "color": color};
      circlesData.push(elem);
      colorIndex--;
    }
  }
  return circlesData;
}
