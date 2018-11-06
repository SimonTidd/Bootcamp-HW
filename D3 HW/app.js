
// couldn't get the labels fully working
// also, I tried for quite awhile to change the thickness of the axes
// and to change the font also - Googling didn't help much


//set up chart area as svg

var svgWidth = 960;
var svgHeight = 500;

var margin = {
  top: 20,
  right: 40,
  bottom: 60,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group to hold our chart, and shift the latter by left and top margins.
var svg = d3
  .select(".chart")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Import Data
var file = "data.csv"
d3.csv(file).then(successHandle, errorHandle);

function errorHandle(error){
  throw error;
}


function successHandle(Data) {

  // Step 1: Parse Data
   // ==============================

  // bring in the state abreviations also to use as labels
  
   Data.forEach(function(data) {
    data.obesity = +data.obesity;
    data.smokes = +data.smokes;
    data.abbr = +data.abbr;
  });

  // Step 2: Create scale functions
  // plot data with a buffer of 2 at ends of both x and y ranges
  // ==============================
  var xLinearScale = d3.scaleLinear()
    .domain([d3.min(Data, d => d.smokes)-2, d3.max(Data, d => d.smokes)+2])
    .range([0, width]);

  var yLinearScale = d3.scaleLinear()
    .domain([d3.min(Data, d => d.obesity)-2, d3.max(Data, d => d.obesity)+2])
    .range([height, 0]);

  // Step 3: Create axis functions
  // ==============================
  var bottomAxis = d3.axisBottom(xLinearScale)
  
  var leftAxis = d3.axisLeft(yLinearScale);

  // Step 4: Append Axes to the chart
  // ==============================
  chartGroup.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);

  chartGroup.append("g")
    .call(leftAxis);

   // Step 5: Create Circles
  // ==============================
  var circlesGroup = chartGroup.selectAll("circle")
  .data(Data)
  .enter()
  .append("circle")
  .attr("cx", d => xLinearScale(d.smokes))
  .attr("cy", d => yLinearScale(d.obesity))
  .attr("r", "20")
  .attr("fill", "blue")
  .attr("opacity", ".5");

    // Create axes labels
  chartGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left + 40)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .attr("class", "axisText")
    .text("Obesity (% of Population");

  chartGroup.append("text")
    .attr("transform", `translate(${width / 2}, ${height + margin.top + 30})`)
    .attr("class", "axisText")
    .text("Smokers (% of Population)");

  //add state labels to circles

  svg.selectAll("text")
    .data(Data)
    .enter()
    .append("text")
    .text(function(d) {
      return d.abbr;
    })
    .attr("x", function(d) {
      return d.obesity;
    })
    .attr("y", function(d) {
      return d.smokes;
    })
    .attr('text-anchor', 'middle')
    .attr("font-size", "15px")
    .attr("fill", "red")

}
