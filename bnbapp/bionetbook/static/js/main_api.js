function getFlowchartData(){
    var successCallback = arguments[arguments.length-1];

    var slugs = '';
    for (var i in arguments) {
        if (i!=arguments.length-1)
            slugs += arguments[i] + '/';
    }

    $.get("/api/json/manual_data/" + slugs, function(data) { successCallback(data); });
};

function callback(data) {
    $('.flowchart-container').flowchart( data );
}

// getFlowchartData( 'slug_A', 'slug_B', callback );
