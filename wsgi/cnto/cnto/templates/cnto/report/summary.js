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
    var margin = {top: 20, right: 30, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(20, "");

    var chart = d3.select(".chart")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    x.domain(data.map(function(d) { return d.week_start_dt; }));
    y.domain([0, d3.max(data, function(d) { return d.week_max; })]);

    chart.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    chart.append("g")
      .attr("class", "y axis")
      .call(yAxis);

    chart.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.week_start_dt); })
      .attr("y", function(d) { return y(d.week_max); })
      .attr("height", function(d) { return height - y(d.week_max); })
      .attr("width", x.rangeBand());

    chart.append("g")
            .attr("class", "y axis")
            .call(yAxis)
        .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Attendances");
}

$(document).ready(function () {
    var data = {{ event_data|safe }};
    generateChart(data);
});