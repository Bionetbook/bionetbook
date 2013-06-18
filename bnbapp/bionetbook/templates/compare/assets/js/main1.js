

// var getFlowchartData = function(username, successCallback) {
//   $.get("http://somewebsite.com",
//     "{username:" + username + "}",
//     function(data) {
//       alert("data received 1! " + data);
//       successCallback(data);
//     },
//     "html")
//   return 31337;
// }

// signIn("bob", function(data) {
//   alert("data received 2! " + data);
// });


// var compare_url = "/api/json/primetest/manual_json/"

function getFlowchartData(successCallback){
    $.get("/api/json/manual_data/",
        function(data) {
            successCallback(data);
    });
};

$(function(){
    getFlowchartData(function(data) {
        $('.flowchart-container').flowchart( data );
    });
});