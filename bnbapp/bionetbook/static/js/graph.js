function getFlowchartData(successCallback){
    $.get("/api/json/manual_data/",
        function(data) {
            successCallback(data);
    });
};

// $(function(){
//     getFlowchartData(function(data) {
//         $('.flowchart-container').flowchart( data );
//     });
// });

function callback(data) {
	$('.flowchart-container').flowchart( data );
}

getFlowchartData( callback );
