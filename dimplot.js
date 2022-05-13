function dimplot(div_id, data){

    const margins = {left: 100, right: 200, top: 100, bottom: 200};
    const size = { width: 960, height: 600 };
    var datafiltered = data;

    var svg = d3.select(div_id)
        .append('svg')
        .attr("width", size.width)
        .attr("height", size.height)
        .append('g')
            .attr("transform", "translate(" + margins.left + "," + margins.top + ")")

    var xscale = d3.scale.linear()
                .domain(d3.extent(data, d => d.x))
                .range([margins.left, size.width - margins.right]);
    
    var yscale = d3.scale.linear()
                .domain(d3.extent(data, d => d.y))
                .range([size.height - margins.bottom, margins.top]);

    var xaxis = d3.svg.axis()
                .scale(xscale)
                .orient("bottom");
    
    var yaxis = d3.svg.axis()
                .scale(yscale)
                .orient("left");

    svg.append('g')
        .attr("class", "xaxis")
        .call(xaxis);
    
    svg.append('g')
        .attr("class", "yaxis")
        .call(yaxis);
    
    var circles = svg.append('g')
                    .selectAll("circle")
                    .data(data)
                    .enter()
                    .append("circle")
                    // .attr("fill", "pink")
                    .attr("cx", d => xscale(d.x))
                    .attr("cy", d => yscale(d.y))
                    .attr("r", 3)
                    .attr("class", "non_brushed");

    var brush = d3.svg.brush()
                .x(xscale)
                .y(yscale)
                .extent([8, 5])
                .on("brush", highlight_points)
                .on("brushend", update_data);

    comm = new CommAPI("get_data_update", (ret) => { console.log('comm called') });
    
    svg.append('g')
        .call(brush)
        .call(brush.event);

    function highlight_points(){
      circles.attr("class", "non_brushed");  
      var extent = brush.extent();
      if (extent) {
        const [[x0, y0], [x1, y1]] = extent;
        circles.data(data)
              .filter(d => x0 <= d.x && d.x < x1 && y0 <= d.y && d.y < y1)
              .attr("class", "brushed");
        datafiltered = data.filter(d => x0 <= d.x && d.x < x1 && y0 <= d.y && d.y < y1);
        // console.log(datafiltered)
      } 
        
    }

    function update_data(){
      comm.call({"datafiltered": datafiltered });
    }
}