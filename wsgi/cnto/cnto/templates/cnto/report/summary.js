var CNTOCharts = CNTOCharts || {};

CNTOCharts.Summary = {};

CNTOCharts.Summary.xAxisTicks = null;
CNTOCharts.Summary.yAxisTicks = null;

CNTOCharts.Summary.color = d3.scale.ordinal().range(['steelblue', 'limegreen']);

CNTOCharts.Summary.lineGen = d3.svg.line()
        .x(function(d) {
            return CNTOCharts.Summary.xScale(d.week_start_dt) + CNTOCharts.Summary.xScale.rangeBand() / 2;
        }).y(function(d) {
            return CNTOCharts.Summary.yScale(d.week_avg);
        });

CNTOCharts.Summary.setupChart = function() {
    CNTOCharts.Summary.totalWidth = 1200;
    CNTOCharts.Summary.totalHeight = 500;

    CNTOCharts.Summary.margin = {top: 20, right: 30, bottom: 60, left: 40};
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

    CNTOCharts.Summary.chart = d3.select(".chart");

    CNTOCharts.Summary.chartBody = CNTOCharts.Summary.chart
      .append("g")
        .attr("transform", "translate(" + CNTOCharts.Summary.margin.left + "," + CNTOCharts.Summary.margin.top + ")");
};

CNTOCharts.Summary.updateData = function(data) {
    CNTOCharts.Summary.xScale.domain(data.map(function(d) { return d.week_start_dt; }));
    CNTOCharts.Summary.yScale.domain([0, d3.max(data, function(d) { return Math.max(d.week_max, d.week_avg); })]);

    // Bars
    var chartUpdated = CNTOCharts.Summary.chartBody.selectAll(".summary-group").data(data);

    var chartEnter = chartUpdated.enter();

    var chartGroup = chartEnter.append("svg:g").attr("class", "summary-group");
    chartGroup.append("svg:rect").attr("class", "summary-rect");
    chartGroup.append('svg:path').attr("class", "summary-line");

    // Rect
    chartUpdated.select("rect.summary-rect")
        .attr("class", "bar summary-rect")
        .attr("x", function(d) { return CNTOCharts.Summary.xScale(d.week_start_dt); })
        .attr("y", function(d) { return CNTOCharts.Summary.yScale(d.week_max); })
        .attr("height", function(d) { return CNTOCharts.Summary.height - CNTOCharts.Summary.yScale(d.week_max); })
        .attr("width", CNTOCharts.Summary.xScale.rangeBand())
        .attr("fill", function(d, i) {
            return CNTOCharts.Summary.color("Maximum");
        });

    // Line
    chartUpdated.select("path.summary-line")
        .attr('d', CNTOCharts.Summary.lineGen(data))
        .attr('stroke', function(d, i) {
            return CNTOCharts.Summary.color("Average");
        })
        .attr('stroke-width', 2)
        .attr('fill', 'none');


//    chartUpdated.bar(function(d) { return d; });

    chartUpdated.exit().remove();

    CNTOCharts.Summary.chartBody.select(".x-ticks").remove();
    CNTOCharts.Summary.chartBody.select(".y-ticks").remove();

    CNTOCharts.xAxisTicks = CNTOCharts.Summary.chartBody.append("g")
      .attr("class", "x axis x-ticks")
      .attr("transform", "translate(0," + CNTOCharts.Summary.height + ")")
      .call(CNTOCharts.Summary.xAxis)
      .selectAll("text").style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-65)" );

    CNTOCharts.yAxisTicks = CNTOCharts.Summary.chartBody.append("g")
      .attr("class", "y axis y-ticks")
      .call(CNTOCharts.Summary.yAxis);

    CNTOCharts.Summary.updateLegend();
};

CNTOCharts.Summary.updateLabels = function() {
    // Add the text label for the X axis
    CNTOCharts.Summary.chartBody.append("text")
        .attr("transform", "translate(" + (CNTOCharts.Summary.width / 2) + " ," + (CNTOCharts.Summary.height + CNTOCharts.Summary.margin.bottom) + ")")
        .style("text-anchor", "middle")
        .text("Week start");

    // Add the text label for the Y axis
    CNTOCharts.Summary.chartBody.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - CNTOCharts.Summary.margin.left)
        .attr("x",0 - (CNTOCharts.Summary.height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Attendance");
};

CNTOCharts.Summary.updateLegend = function() {
    // Legend
    CNTOCharts.Summary.legendRectSize = 18;
    CNTOCharts.Summary.legendSpacing = 4;

    // Data join
    var legend = CNTOCharts.Summary.chartBody.selectAll('.legend').data(CNTOCharts.Summary.color.domain());

    var legendEnter = legend.enter();

    var legendGroup = legendEnter.append('g')
            .attr('class', 'legend')
            .attr('transform', function(d, i) {
                var height = CNTOCharts.Summary.legendRectSize + CNTOCharts.Summary.legendSpacing;
                var offset =  height * CNTOCharts.Summary.color.domain().length / 2;
                var horz = -2 * CNTOCharts.Summary.legendRectSize + CNTOCharts.Summary.totalWidth - 100;
                var vert = i * height - offset;
                return 'translate(' + horz + ',' + vert + ')';
            });

    legendGroup.append('rect')
        .attr('width', CNTOCharts.Summary.legendRectSize)
        .attr('height', CNTOCharts.Summary.legendRectSize)
        .style('fill', CNTOCharts.Summary.color)
        .style('stroke', CNTOCharts.Summary.color);

    legendGroup.append('text').attr('x', CNTOCharts.Summary.legendRectSize + CNTOCharts.Summary.legendSpacing)
        .attr('y', CNTOCharts.Summary.legendRectSize - CNTOCharts.Summary.legendSpacing)
        .text(function(d) { return d; });

    legend.exit().remove();
};

$(document).ready(function () {
    CNTOCharts.Summary.setupChart();
    CNTOCharts.Summary.updateLabels();
    CNTOCharts.Summary.updateLegend();

    var dataUrl = "{% url 'get-summary-data' %}";
    $.get(dataUrl, function (result) {
        CNTOCharts.Summary.updateData(result["event-data"]);
    });

//    var counter = 0;
//    setInterval(function() {
//        data.push({
//            week_start_dt: "2015-99-" + counter,
//            week_max: counter,
//            week_avg: counter * 2
//        });
//
//        CNTOCharts.Summary.updateData(data);
//        counter += 5;
//    }, 1500);


});