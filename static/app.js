function drawChart(svg, data, update) {
	const padding = 30;
	const timeSpan = 1000;
	canvas_width = svg.style("width").replace("px", "");
	canvas_height = svg.style("height").replace("px", "");

	var xScaler = d3.scaleLinear()
		.domain([d3.min(data, d => d.x), d3.max(data, d => d.x)])
		.range([1.5 * padding, canvas_width - 1.5 * padding]);
	var yScaler = d3.scaleLinear()
		.domain([d3.min(data, d => d.y), d3.max(data, d => d.y)])
		.range([canvas_height - 1.5 * padding, 1.5 * padding]);
	var xAxisFunc = d3.axisBottom().scale(xScaler).tickValues([]);
	var yAxisFunc = d3.axisLeft().scale(yScaler).tickValues([]);

	// draw/update circles
	var sel = svg.selectAll("circle").data(data);
	if (update) {
		sel = sel.transition().duration(timeSpan);
	}
	else {
		sel = sel.enter().append("circle");
	}
	sel.attr("cx", d => xScaler(d.x))
		.attr("cy", d => yScaler(d.y))
		.attr("r", 2)
		.attr("fill", function (d) {
			if (d.label == 1) {return "red"}
			else {return "black"}
		});

	// draw/update axis
	if (update) {
		svg.select("g.x.axis").transition().duration(timeSpan)
			.call(xAxisFunc);
		svg.select("g.y.axis").transition().duration(timeSpan)
			.call(yAxisFunc);
	}
	else {
		var xOffset = canvas_height - padding;
		svg.append("g")
			.attr("transform", `translate(0, ${xOffset})`)
			.call(xAxisFunc);
		svg.append("g")
			.attr("transform", `translate(${padding}, 0)`)
			.call(yAxisFunc);
	}

    // axis text
    if (!update) {
        var xAxisTextLoc = [canvas_width / 2, canvas_height];
        svg.append("text")
            .attr("transform",
                `translate(${xAxisTextLoc[0]}, ${xAxisTextLoc[1]})`)
          .style("text-anchor", "middle")
          .text("UMAP 1");

        var yAxisTextLoc = [0, -canvas_height / 2];
        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("x", yAxisTextLoc[1])
            .attr("y", yAxisTextLoc[0])
        .attr("dy", "1em")
          .style("text-anchor", "middle")
          .text("UMAP 2");
    }
}
