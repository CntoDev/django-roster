var CNTOCharts = CNTOCharts || {};

CNTOCharts.Summary = {};

CNTOCharts.Summary.setupChart = function(data) {
    CNTOCharts.Summary.totalWidth = 1200;
    CNTOCharts.Summary.totalHeight = 500;

    CNTOCharts.Summary.margin = {top: 20, right: 30, bottom: 30, left: 40};
    CNTOCharts.Summary.width = CNTOCharts.Summary.totalWidth - CNTOCharts.Summary.margin.left - CNTOCharts.Summary.margin.right;
    CNTOCharts.Summary.height = CNTOCharts.Summary.totalHeight - CNTOCharts.Summary.margin.top - CNTOCharts.Summary.margin.bottom;

    CNTOCharts.Summary.xScale = d3.scale.ordinal()
        .rangeRoundBands([0, CNTOCharts.Summary.width], .1);

    CNTOCharts.Summary.yScale = d3.scale.linear()
        .range([CNTOCharts.Summary.height, 0]);

    CNTOCharts.Summary.xAxis = d3.svg.axis()
        .scale(CNTOCharts.Summary.xScale)
        .orient("bottom");

    CNTOCharts.Summary.yAxis = d3.svg.axis()
        .scale(CNTOCharts.Summary.yScale)
        .orient("left")
        .ticks(20, "");

    CNTOCharts.Summary.chart = d3.select(".chart")
//        .attr("CNTOCharts.Summary.width", CNTOCharts.Summary.width + CNTOCharts.Summary.margin.left + CNTOCharts.Summary.margin.right)
//        .attr("CNTOCharts.Summary.height", CNTOCharts.Summary.height + CNTOCharts.Summary.margin.top + CNTOCharts.Summary.margin.bottom)
      .append("g")
        .attr("transform", "translate(" + CNTOCharts.Summary.margin.left + "," + CNTOCharts.Summary.margin.top + ")");

    CNTOCharts.Summary.xScale.domain(data.map(function(d) { return d.week_start_dt; }));
    CNTOCharts.Summary.yScale.domain([0, d3.max(data, function(d) { return d.week_max; })]);

    var lineGen = d3.svg.line()
        .x(function(d) {
            return CNTOCharts.Summary.xScale(d.week_start_dt) + CNTOCharts.Summary.xScale.rangeBand() / 2;
        }).y(function(d) {
            return CNTOCharts.Summary.yScale(d.week_avg);
        });

    CNTOCharts.Summary.chart.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + CNTOCharts.Summary.height + ")")
      .call(CNTOCharts.Summary.xAxis);

    CNTOCharts.Summary.chart.append("g")
      .attr("class", "y axis")
      .call(CNTOCharts.Summary.yAxis);

    CNTOCharts.Summary.color = d3.scale.ordinal().range(['steelblue', 'limegreen']);

    // Bars
    CNTOCharts.Summary.chartEnter = CNTOCharts.Summary.chart.selectAll(".bar").data(data).enter();
    CNTOCharts.Summary.chartEnter.append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return CNTOCharts.Summary.xScale(d.week_start_dt); })
        .attr("y", function(d) { return CNTOCharts.Summary.yScale(d.week_max); })
        .attr("height", function(d) { return CNTOCharts.Summary.height - CNTOCharts.Summary.yScale(d.week_max); })
        .attr("width", CNTOCharts.Summary.xScale.rangeBand())
        .attr("fill", function(d, i) {
            return CNTOCharts.Summary.color("Maximum");
        });

    // Line
    CNTOCharts.Summary.chartEnter.append('svg:path')
        .attr('d', lineGen(data))
        .attr('stroke', function(d, i) {
            return CNTOCharts.Summary.color("Average");
        })
        .attr('stroke-width', 2)
        .attr('fill', 'none');

    // Legend
    CNTOCharts.Summary.legendRectSize = 18;
    CNTOCharts.Summary.legendSpacing = 4;

    var legend = CNTOCharts.Summary.chart.selectAll('.legend')
            .data(CNTOCharts.Summary.color.domain())
        .enter()
            .append('g')
            .attr('class', 'legend')
            .attr('transform', function(d, i) {
                var height = CNTOCharts.Summary.legendRectSize + CNTOCharts.Summary.legendSpacing;
                var offset =  height * CNTOCharts.Summary.color.domain().length / 2;
                var horz = -2 * CNTOCharts.Summary.legendRectSize + CNTOCharts.Summary.totalWidth - 100;
                var vert = i * height - offset;
                return 'translate(' + horz + ',' + vert + ')';
            });

    legend.append('rect')
        .attr('width', CNTOCharts.Summary.legendRectSize)
        .attr('height', CNTOCharts.Summary.legendRectSize)
        .style('fill', CNTOCharts.Summary.color)
        .style('stroke', CNTOCharts.Summary.color);

    legend.append('text')
        .attr('x', CNTOCharts.Summary.legendRectSize + CNTOCharts.Summary.legendSpacing)
        .attr('y', CNTOCharts.Summary.legendRectSize - CNTOCharts.Summary.legendSpacing)
        .text(function(d) { return d; });

    // Add the text label for the X axis
    CNTOCharts.Summary.chart.append("text")
        .attr("transform", "translate(" + (CNTOCharts.Summary.width / 2) + " ," + (CNTOCharts.Summary.height + CNTOCharts.Summary.margin.bottom) + ")")
        .style("text-anchor", "middle")
        .text("Week start");

    // Add the text label for the Y axis
    CNTOCharts.Summary.chart.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - CNTOCharts.Summary.margin.left)
        .attr("x",0 - (CNTOCharts.Summary.height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Attendance");
};

$(document).ready(function () {
    var data = {{ event_data|safe }};
    CNTOCharts.Summary.setupChart(data);
});