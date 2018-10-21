// from data.js
var tableData = data;

// YOUR CODE HERE!
var tbody = d3.select("tbody");


console.log(data);

tableData.forEach((sighting) => {
  var row = tbody.append("tr");
  Object.entries(sighting).forEach(([key, value]) => {
    var cell = tbody.append("td");
    cell.text(value);
  });
});


// Select the submit button
var submit = d3.select("#filter-badge");

submit.on("click", function() {

  // Prevent the page from refreshing
  d3.event.preventDefault();

  // Select the input element and get the raw HTML node
  var inputElement = d3.select("#date");

  // Get the value property of the input element
  var inputValue = inputElement.property("value");


  var filteredData = tableData.filter(sighting => sighting.datetime === inputValue);

  // clear table
  var tbody = d3.select("tbody");
  tbody.html("");
  // render filtered data
  console.log(filteredData);

  filteredData.forEach((sighting) => {
    var row = tbody.append("tr");
    Object.entries(sighting).forEach(([key, value]) => {
      var cell = tbody.append("td");
      cell.text(value);
    });
  });
});