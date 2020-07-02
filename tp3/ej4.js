{
  var svg = d3.create('svg')
    .attr('width', config_ejd.width)
    .attr('height', config_ejd.height);
  
  var triangles = svg.selectAll("g")
    .data(triangles_data_ejd)
    .enter()
    .append("g");
  
  triangles.append('path')
           .attr("d", function(d) {return d.d;})
           .attr('transform', function(d) { return d.transform;})
           .style("fill", function(d) {return d.fill;})
           .style("stroke", function(d) {return d.stroke;})
           .style("stroke-width", function(d) {return d.stroke_width;});
  
  return svg.node(); 
}

config_ejd = {
  var trianglePerRow = 17;
  var width = Math.floor(trianglePerRow*57);
  var height = Math.floor(trianglePerRow*57);
  var spaceRow = 10;
  var spaceColumn = 10;
  
  let config_ejd = {
    "trianglePerRow": trianglePerRow,
    "width": Math.floor(trianglePerRow*57),
    "height": Math.floor(trianglePerRow*57),
    "spaceRow": 10,
    "spaceColumn": 10
  };
  return config_ejd;
}

triangles_data_ejd = {
  var triangle = d3.symbol().type(d3.symbolTriangle).size(config_ejd.height*10 / config_ejd.trianglePerRow);
  console.log(triangle());
  var trianglesData = [];
  
  for (var i = -1; i < config_ejd.trianglePerRow*2; i++) {
    for (var j = -1; j < config_ejd.trianglePerRow; j++) {
      //var x_gap = (i*33 + config_ejd.spaceRow);
      var x_gap = (i*33 + config_ejd.spaceRow);
      var y_gap = (j*50 + config_ejd.spaceColumn);
      var translateValue = 'translate('+x_gap+','+y_gap+')';
      var colorFill = 'white';
      var colorStroke = 'red';
      if (i % 2 != 0) {
        translateValue += ' rotate(180 0 -5)';
        colorFill = 'yellow';
        colorStroke = 'blue';
      }
      var oneTriangle = {
        "d": triangle(),
        "fill": colorFill,
        "stroke": colorStroke,
        "stroke_width": 3,
        "transform": translateValue
      };
      
      trianglesData.push(oneTriangle);
    }
  }
  return trianglesData;
}
