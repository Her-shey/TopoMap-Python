function scatterplot(div_id, data){

    const margins = {left: 100, right: 100, top: 100, bottom: 100};
    const size = {width: 960, height: 600};
    const colordict = ["gold", "blue", "green", "yellow", "grey", "pink", "brown", "slateblue", "grey1", "orange"];

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
    
    svg.append('g')
        .selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("fill", d => colordict[d.group])
        .attr("cx", d => xscale(d.x))
        .attr("cy", d => yscale(d.y))
        .attr("r", 2);

}