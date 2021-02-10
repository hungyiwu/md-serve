var dataset = $.ajax({
	url: "/api/v1/coord/0.0",
	async: false,
	dataType: "json",
}).responseJSON;

var canvas_width = 500;
var canvas_height = 300;
var padding = 30;

var xScale = d3.scaleLinear()
	.domain([0, d3.max(dataset, function(d) {return d.x;})])
        .range([padding, canvas_width - padding * 2]);

var yScale = d3.scaleLinear()
	.domain([0, d3.max(dataset, function(d) {return d.y;})])
        .range([canvas_height - padding, padding]);

var xAxis = d3.axisBottom().scale(xScale).ticks(5);
var yAxis = d3.axisLeft().scale(yScale).ticks(5);
var svg = d3.select("#canvas");

svg.selectAll("circle").data(dataset).enter()
	.append("circle")
        .attr("cx", function (d) {return xScale(d.x);})
        .attr("cy", function (d) {return yScale(d.y);})
	.attr("r", 2);

svg.append("g")
	.attr("class", "x axis")
        .attr("transform", "translate(0," + (canvas_height - padding) +")")
        .call(xAxis);

svg.append("g")
	.attr("class", "y axis")
        .attr("transform", "translate(" + padding +",0)")
        .call(yAxis);

function updateChart(svg, data) {
	xScale.domain([0, d3.max(data, d => d.x)]);
        yScale.domain([0, d3.max(data, d => d.y)]);
        
	svg.selectAll("circle").data(data)
		.transition().duration(1000)
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y));

	// update axes
	svg.select(".x.axis").transition().duration(1000).call(xAxis);
	svg.select(".y.axis").transition().duration(1000).call(yAxis);
}

function fetchData(key) {
	var data = $.ajax({
		url: `/api/v1/coord/${key}`,
		async: false,
		dataType: "json",
	}).responseJSON;
	return data;
}


d3.select("#slider").on("input", function () {
	var current_value = parseFloat(this.value).toFixed(1);
	d3.select("#slider-label").text(current_value);
	dataset = fetchData(current_value);
	updateChart(svg, dataset);
    });
