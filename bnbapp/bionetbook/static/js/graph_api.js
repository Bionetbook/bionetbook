function getFlowchartData(){
    
	return [{"child_diff": "True", "name": "combine", "objectid": ["kttj4d", "kttj4d"], "child_type": ["components", "components"], "node_type": "Action", "child": [{"node_objectid": "0tisce", "name": ["Oligo(dT)12-18 primers", "Oligo(dT)12-18 primers"], "URL": ["/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/", "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/"], "vol": [["1.0-10.0", "ul"], ["1-10", "ul"]], "node_type": "Component", "conc": [["50.0-500.0", "ng/ul"], ["50-500", "ng/ul"]], "mass": [["500.0", "ng"], ["500", "ng"]]}, {"node_objectid": "qr1vjs", "name": ["Nucleic Acid, dNTPs (Invitrogen)", "Nucleic Acid, dNTPs (Invitrogen)"], "URL": ["/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/", "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/"], "vol": [["1", "ul"], ["1", "ul"]], "node_type": "Component", "conc": [["10", "mM"], ["10", "mM"]]}, {"node_objectid": "ddnuty", "name": ["Water, nuclease-free, sterile", "Water, nuclease-free, sterile"], "URL": ["/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/", "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/"], "vol": [["0-9", "ul"], ["0-9", "ul"]], "node_type": "Component"}, {"node_objectid": "1exatc", "name": ["None", "Total Volume"], "URL": [null, "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/"], "vol": ["None", ["12", "ul"]], "node_type": "Component"}, {"node_objectid": "f5fe2d", "name": ["Nucleic Acid, RNA, poly(A)+", "Nucleic Acid, RNA, poly(A)+"], "URL": ["/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/", "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/"], "vol": [["1.0-10.0", "ul"], ["1-10", "ul"]], "node_type": "Component", "conc": [["500.0-1000.0", "ng/ul"], ["100-1000", "ng/ul"]], "mass": [["100.0-1000.0", "ng"], ["100-1000", "ng"]]}], "duration": [120.0, 120.0]}]

};
//     var successCallback = arguments[arguments.length-1];

//     var slugs = '';
//     for (var i in arguments) {
//         if (i!=arguments.length-1)
//             slugs += arguments[i] + '/';
//     }

//     $.get("/api/json/object_aligned/" + slugs, function(data) { successCallback(data); });
// };

function callback(data) {
	// alert(data);
    $('.flowchart-container').flowchart( data );
}


