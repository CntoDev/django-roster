function generateChart(data) {
//    var margin = {top: 20, right: 30, bottom: 30, left: 40},
//        width = 960 - margin.left - margin.right,
//        height = 500 - margin.top - margin.bottom;
//
//    var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);
//
//    var y = d3.scale.linear().range([height, 0]);
//
//    var xAxis = d3.svg.axis().scale(x).orient("bottom");
//
//    var yAxis = d3.svg.axis().scale(y).orient("left");
//
//    var chart = d3.select(".chart")
//        .attr("width", width + margin.left + margin.right)
//        .attr("height", height + margin.top + margin.bottom)
//        .append("g")
//        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
//
//    x.domain(data.map(function(d) { return d.week_start_dt; }));
//    y.domain([0, d3.max(data, function(d) { return d.week_max; })]);
//
//    chart.append("g")
//        .attr("class", "x axis")
//        .attr("transform", "translate(0," + height + ")")
//        .call(xAxis);
//
//    chart.append("g")
//        .attr("class", "y axis")
//        .call(yAxis);
//
//    chart.selectAll(".bar")
//            .data(data)
//        .enter().append("rect")
//            .attr("class", "bar")
//            .attr("x", function(d) { return x(d.week_start_dt); })
//            .attr("y", function(d) { return y(d.week_max); })
//            .attr("width", x.rangeBand())
//            .attr("height", function(d) { return height - y(d.week_max); });
    var totalWidth = 1200;
    var totalHeight = 500;

    var margin = {top: 20, right: 30, bottom: 30, left: 40},
        width = totalWidth - margin.left - margin.right,
        height = totalHeight - margin.top - margin.bottom;

    var xScale = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var yScale = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left")
        .ticks(20, "");

    var chart = d3.select(".chart")
//        .attr("width", width + margin.left + margin.right)
//        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    xScale.domain(data.map(function(d) { return d.week_start_dt; }));
    yScale.domain([0, d3.max(data, function(d) { return d.week_max; })]);

    var lineGen = d3.svg.line()
        .x(function(d) {
            return xScale(d.week_start_dt) + xScale.rangeBand() / 2;
        }).y(function(d) {
            return yScale(d.week_avg);
        });

    chart.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    chart.append("g")
      .attr("class", "y axis")
      .call(yAxis);

    var color = d3.scale.ordinal().range(['steelblue', 'limegreen']);

    // Bars
    var chartEnter = chart.selectAll(".bar").data(data).enter();
    chartEnter.append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return xScale(d.week_start_dt); })
        .attr("y", function(d) { return yScale(d.week_max); })
        .attr("height", function(d) { return height - yScale(d.week_max); })
        .attr("width", xScale.rangeBand())
        .attr("fill", function(d, i) {
            return color("Maximum");
        });

    // Line
    chartEnter.append('svg:path')
        .attr('d', lineGen(data))
        .attr('stroke', function(d, i) {
            return color("Average");
        })
        .attr('stroke-width', 2)
        .attr('fill', 'none');

    // Legend
    var legendRectSize = 18;
    var legendSpacing = 4;

    var legend = chart.selectAll('.legend')
            .data(color.domain())
        .enter()
            .append('g')
            .attr('class', 'legend')
            .attr('transform', function(d, i) {
                var height = legendRectSize + legendSpacing;
                var offset =  height * color.domain().length / 2;
                var horz = -2 * legendRectSize + totalWidth - 100;
                var vert = i * height - offset;
                return 'translate(' + horz + ',' + vert + ')';
            });

    legend.append('rect')
        .attr('width', legendRectSize)
        .attr('height', legendRectSize)
        .style('fill', color)
        .style('stroke', color);

    legend.append('text')
        .attr('x', legendRectSize + legendSpacing)
        .attr('y', legendRectSize - legendSpacing)
        .text(function(d) { return d; });

    // Add the text label for the X axis
    chart.append("text")
        .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom) + ")")
        .style("text-anchor", "middle")
        .text("Week start");

    // Add the text label for the Y axis
    chart.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Attendance");
}

$(document).ready(function () {
    var data = {{ event_data|safe }};
    generateChart(data);
});