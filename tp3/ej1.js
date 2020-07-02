{
  // 1. Creación de un área de dibujo (256x256 pixeles).
  //    Si lo consideran necesario, pueden modificar el tamaño del canvas.
  //    También es posible que necesiten más de una celda para resolverlo.
  const svg = d3.create("svg")
                .attr("width", config_eja.width)
                .attr("height", config_eja.height);
  
  var circles = svg.selectAll("circle")
                    .data(circles_data_eja)
                    .enter()
                    .append("circle")
                    .attr("cx", function(d) {return d.axis_x;} )
                    .attr("cy", function(d) {return d.axis_y;} )
                    .attr("r" , function(d) {return d.radius;} )
                    .style("fill", function(d) { return d.color;});
  
  return svg.node(); 
}

config_eja = {
  var config_eja = {
    "width": 267,
    "height": 267
  };
  return config_eja;
}

circles_data_eja = {
  var circlesData = [
    {
      "axis_x":config_eja.width/2, 
      "axis_y": config_eja.height/2, 
      "radius": config_eja.width/8*3,
      "color": "#087E03"
    },
    {
      "axis_x":config_eja.width/2, 
      "axis_y": config_eja.height/2, 
      "radius": config_eja.width/8*2,
      "color": "#7F007F"
    },
    {
      "axis_x":config_eja.width/2, 
      "axis_y": config_eja.height/2, 
      "radius": config_eja.width/8*1,
      "color": "#FF0B00"
    }
];
return circlesData;
}
