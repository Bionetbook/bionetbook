function getFlowchartData(){
    var successCallback = arguments[arguments.length-1];

    var slugs = '';
    for (var i in arguments) {
        if (i!=arguments.length-1)
            slugs += arguments[i] + '/';
    }

    $.get("/api/json/object_aligned/" + slugs, function(data) { successCallback(data); });
};

function callback(data) {
	// alert(data);
    $('.flowchart-container').flowchart( data );
}