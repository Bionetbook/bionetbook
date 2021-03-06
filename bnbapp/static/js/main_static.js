function getFlowchartData() {
    return [
    {
        "name": "call-for-protocol",
        "objectid": [
            "None",
            "ahd90y"
        ],
        "child_type": [
            "None",
            "components"
        ],
        "node_type": "Action",
        "child_diff": "True",
        "child": [
            {
                "name": [
                    "None",
                    "Nucleic Acid, RNA, poly(A)+"
                ],
                "objectid": [
                    "None",
                    "f7zg5q"
                ],
                "URL": [
                    "/None",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/ljkq9h/ahd90y/edit/"
                ],
                "node_type": "Component",
                "conc": [
                    ["None"],
                    [
                        "100",
                        "ng/ul"
                    ]
                ],
                "mass": [
                    ["None"],
                    [
                        "100-1000",
                        "ng"
                    ]
                ]
            }
        ],
        "duration": [
            "None",
            "None"
        ]
    },
    {
        "name": "combine",
        "objectid": [
            "kttj4d",
            "kttj4d"
        ],
        "child_type": [
            "components",
            "components"
        ],
        "node_type": "Action",
        "child_diff": "True",
        "child": [
            {
                "name": [
                    "Oligo(dT)12-18 primers",
                    "Oligo(dT)12-18 primers"
                ],
                "objectid": [
                    "0tisce",
                    "0tisce"
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/"
                ],
                "vol": [
                    [
                        "1.0-10.0",
                        "ul"
                    ],
                    [
                        "1.0-10.0",
                        "ul"
                    ]
                ],
                "node_type": "Component",
                "conc": [
                    [
                        "50.0-500.0",
                        "ng/ul"
                    ],
                    [
                        "50.0-500.0",
                        "ng/ul"
                    ]
                ],
                "mass": [
                    [
                        "500.0",
                        "ng"
                    ],
                    [
                        "500.0",
                        "ng"
                    ]
                ]
            },
            {
                "name": [
                    "Nucleic Acid, dNTPs (Invitrogen)",
                    "Nucleic Acid, dNTPs (Invitrogen)"
                ],
                "objectid": [
                    "qr1vjs",
                    "qr1vjs"
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/"
                ],
                "vol": [
                    [
                        "1",
                        "ul"
                    ],
                    [
                        "1",
                        "ul"
                    ]
                ],
                "node_type": "Component",
                "conc": [
                    [
                        "100",
                        "mM"
                    ],
                    [
                        "10",
                        "mM"
                    ]
                ]
            },
            {
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/"
                ],
                "vol": [
                    [
                        "0-9",
                        "ul"
                    ],
                    [
                        "0-9",
                        "ul"
                    ]
                ],
                "node_type": "Component",
                "name": [
                    "Water, nuclease-free, sterile",
                    "Water, nuclease-free, sterile"
                ],
                "objectid": [
                    "ddnuty",
                    "ddnuty"
                ]
            },
            {
                "name": [
                    "Nucleic Acid, RNA, poly(A)+",
                    "Nucleic Acid, RNA, poly(A)+"
                ],
                "objectid": [
                    "f5fe2d",
                    "f5fe2d"
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/"
                ],
                "vol": [
                    [
                        "5.0-10.0",
                        "ul"
                    ],
                    [
                        "1.0-10.0",
                        "ul"
                    ]
                ],
                "node_type": "Component",
                "conc": [
                    [
                        "500.0-1000.0",
                        "ng/ul"
                    ],
                    [
                        "500.0-1000.0",
                        "ng/ul"
                    ]
                ],
                "mass": [
                    [
                        "100.0-1000.0",
                        "ng"
                    ],
                    [
                        "100.0-1000.0",
                        "ng"
                    ]
                ]
            }
        ],
        "duration": [
            "None",
            "None"
        ]
    },
    {
        "name": "heat",
        "objectid": [
            "oy38e9",
            "None"
        ],
        "child_type": [
            "machine",
            "None"
        ],
        "node_type": "Action",
        "child_diff": "True",
        "child": [
            {
                "name": [
                    "bb92m1",
                    "None"
                ],
                "temp": [
                    [
                        "70",
                        "C"
                    ],
                    ["None"]
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/oy38e9/edit/",
                    "None"
                ],
                "node_type": "Machine",
                "objectid": [
                    "bb92m1",
                    "None"
                ],
                "time": [
                    [
                        "5",
                        "min"
                    ],
                    ["None"]
                ]
            }
        ],
        "duration": [
            "None",
            "None"
        ]
    },
    {
        "name": "chill",
        "objectid": [
            "f4hds3",
            "f4hds3"
        ],
        "child_type": [
            "machine",
            "machine"
        ],
        "node_type": "Action",
        "child_diff": "False",
        "child": [
            {
                "name": [
                    "6slh85",
                    "6slh85"
                ],
                "temp": [
                    [
                        "0",
                        "C"
                    ],
                    [
                        "0",
                        "C"
                    ]
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/f4hds3/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/f4hds3/edit/"
                ],
                "node_type": "Machine",
                "objectid": [
                    "6slh85",
                    "6slh85"
                ],
                "time": [
                    [
                        "1",
                        "min"
                    ],
                    [
                        "1",
                        "min"
                    ]
                ]
            }
        ],
        "duration": [
            "None",
            "None"
        ]
    },
    {
        "name": "centrifuge",
        "objectid": [
            "9b92ym",
            "9b92ym"
        ],
        "child_type": [
            "machine",
            "machine"
        ],
        "node_type": "Action",
        "child_diff": "False",
        "child": [
            {
                "name": [
                    "centrifuge",
                    "centrifuge"
                ],
                "temp": [
                    [
                        "15.0",
                        "C"
                    ],
                    [
                        "15.0",
                        "C"
                    ]
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/9b92ym/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/9b92ym/edit/"
                ],
                "node_type": "Machine",
                "objectid": [
                    "s9wupe",
                    "s9wupe"
                ],
                "time": [
                    [
                        "1.0",
                        "min"
                    ],
                    [
                        "1.0",
                        "min"
                    ]
                ]
            }
        ],
        "duration": [
            "1.0",
            "1.0"
        ]
    },
    {
        "name": "add",
        "objectid": [
            "892zia",
            "892zia"
        ],
        "child_type": [
            "components",
            "components"
        ],
        "node_type": "Action",
        "child_diff": "True",
        "child": [
            {
                "URL": [
                    "None",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/edit/"
                ],
                "vol": [
                    ["None"],
                    [
                        "19",
                        "ul"
                    ]
                ],
                "node_type": "Component",
                "name": [
                    "None",
                    "Total volume"
                ],
                "objectid": [
                    "None",
                    "4fsep6"
                ]
            },
            {
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/edit/"
                ],
                "vol": [
                    [
                        "1",
                        "ul"
                    ],
                    [
                        "1",
                        "ul"
                    ]
                ],
                "node_type": "Component",
                "name": [
                    "Water, nuclease-free, sterile",
                    "Water, nuclease-free, sterile"
                ],
                "objectid": [
                    "th2c9d",
                    "th2c9d"
                ]
            },
            {
                "name": [
                    "Buffer, First strand cDNA synthesis (Invitrogen)",
                    "Buffer, First strand cDNA synthesis (Invitrogen)"
                ],
                "objectid": [
                    "d5fd4e",
                    "d5fd4e"
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/edit/"
                ],
                "vol": [
                    [
                        "4",
                        "ul"
                    ],
                    [
                        "4",
                        "ul"
                    ]
                ],
                "node_type": "Component",
                "conc": [
                    [
                        "7",
                        "X"
                    ],
                    [
                        "7",
                        "X"
                    ]
                ]
            },
            {
                "name": [
                    "Reducing agent, Dithiothreitol (DTT)",
                    "Reducing agent, Dithiothreitol (DTT)"
                ],
                "objectid": [
                    "5gw90k",
                    "5gw90k"
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/edit/"
                ],
                "vol": [
                    [
                        "2",
                        "ul"
                    ],
                    [
                        "2",
                        "ul"
                    ]
                ],
                "node_type": "Component",
                "conc": [
                    [
                        "100",
                        "mM"
                    ],
                    [
                        "100",
                        "mM"
                    ]
                ]
            }
        ],
        "duration": [
            "None",
            "None"
        ]
    },
    {
        "name": "centrifuge",
        "objectid": [
            "kbzqcb",
            "kbzqcb"
        ],
        "child_type": [
            "machine",
            "machine"
        ],
        "node_type": "Action",
        "child_diff": "False",
        "child": [
            {
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/kbzqcb/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/kbzqcb/edit/"
                ],
                "node_type": "Machine",
                "name": [
                    "g2943s",
                    "g2943s"
                ],
                "objectid": [
                    "g2943s",
                    "g2943s"
                ],
                "time": [
                    [
                        "1",
                        "min"
                    ],
                    [
                        "1",
                        "min"
                    ]
                ]
            }
        ],
        "duration": [
            "None",
            "None"
        ]
    },
    {
        "name": "incubate",
        "objectid": [
            "j4json",
            "j4json"
        ],
        "child_type": [
            "machine",
            "machine"
        ],
        "node_type": "Action",
        "child_diff": "False",
        "child": [
            {
                "name": [
                    "q249s2",
                    "q249s2"
                ],
                "temp": [
                    [
                        "42",
                        "C"
                    ],
                    [
                        "42",
                        "C"
                    ]
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/k0ul5c/j4json/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/k0ul5c/j4json/edit/"
                ],
                "node_type": "Machine",
                "objectid": [
                    "q249s2",
                    "q249s2"
                ],
                "time": [
                    [
                        "2",
                        "min"
                    ],
                    [
                        "2",
                        "min"
                    ]
                ]
            }
        ],
        "duration": [
            "None",
            "None"
        ]
    },
    {
        "name": "add",
        "objectid": [
            "muwzdb",
            "muwzdb"
        ],
        "child_type": [
            "components",
            "components"
        ],
        "node_type": "Action",
        "child_diff": "False",
        "child": [
            {
                "name": [
                    "Enzyme, SuperScript II reverse transcriptase (Invitrogen)",
                    "Enzyme, SuperScript II reverse transcriptase (Invitrogen)"
                ],
                "objectid": [
                    "w3v4gn",
                    "w3v4gn"
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/muwzdb/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/muwzdb/edit/"
                ],
                "vol": [
                    [
                        "1",
                        "ul"
                    ],
                    [
                        "1",
                        "ul"
                    ]
                ],
                "node_type": "Component",
                "conc": [
                    [
                        "200",
                        "U/ul"
                    ],
                    [
                        "200",
                        "U/ul"
                    ]
                ],
                "mass": [
                    [
                        "200",
                        "U"
                    ],
                    [
                        "200",
                        "U"
                    ]
                ]
            }
        ],
        "duration": [
            "None",
            "None"
        ]
    },
    {
        "name": "mix",
        "objectid": [
            "aoymzg",
            "aoymzg"
        ],
        "child_type": [
            "manual",
            "manual"
        ],
        "node_type": "Action",
        "child_diff": "False",
        "child": [
            {
                "duration": [
                    "30.0",
                    "30.0"
                ],
                "duration_units": [
                    "sec",
                    "sec"
                ],
                "verb": [
                    "mix",
                    "mix"
                ],
                "technique_comment": [
                    "gently flicking",
                    "gently flicking"
                ]
            }
        ],
        "duration": [
            "30.0",
            "30.0"
        ]
    },
    {
        "name": "centrifuge",
        "objectid": [
            "thfavi",
            "thfavi"
        ],
        "child_type": [
            "machine",
            "machine"
        ],
        "node_type": "Action",
        "child_diff": "False",
        "child": [
            {
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/thfavi/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/thfavi/edit/"
                ],
                "node_type": "Machine",
                "name": [
                    "sib53v",
                    "sib53v"
                ],
                "objectid": [
                    "sib53v",
                    "sib53v"
                ],
                "time": [
                    [
                        "1",
                        "min"
                    ],
                    [
                        "1",
                        "min"
                    ]
                ]
            }
        ],
        "duration": [
            "None",
            "None"
        ]
    },
    {
        "name": "incubate",
        "objectid": [
            "bavsb0",
            "bavsb0"
        ],
        "child_type": [
            "machine",
            "machine"
        ],
        "node_type": "Action",
        "child_diff": "False",
        "child": [
            {
                "name": [
                    "nil70h",
                    "nil70h"
                ],
                "temp": [
                    [
                        "70",
                        "C"
                    ],
                    [
                        "70",
                        "C"
                    ]
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/1dmjii/bavsb0/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/1dmjii/bavsb0/edit/"
                ],
                "node_type": "Machine",
                "objectid": [
                    "nil70h",
                    "nil70h"
                ],
                "time": [
                    [
                        "15",
                        "min"
                    ],
                    [
                        "15",
                        "min"
                    ]
                ]
            }
        ],
        "duration": [
            "None",
            "None"
        ]
    },
    {
        "name": "incubate",
        "objectid": [
            "adrmwt",
            "adrmwt"
        ],
        "child_type": [
            "machine",
            "machine"
        ],
        "node_type": "Action",
        "child_diff": "False",
        "child": [
            {
                "name": [
                    "lwikji",
                    "lwikji"
                ],
                "temp": [
                    [
                        "0",
                        "C"
                    ],
                    [
                        "0",
                        "C"
                    ]
                ],
                "URL": [
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/8ylelp/adrmwt/edit/",
                    "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/8ylelp/adrmwt/edit/"
                ],
                "node_type": "Machine",
                "objectid": [
                    "lwikji",
                    "lwikji"
                ],
                "time": [
                    [
                        "2",
                        "min"
                    ],
                    [
                        "2",
                        "min"
                    ]
                ]
            }
        ],
        "duration": [
            "None",
            "None"
        ]
    }
];
}


$(function() {
    $('.flowchart-container').flowchart(getFlowchartData());
});

// Comment everything before
// Production code
// Uncomment everything after

// function getFlowchartData(){
//     var successCallback = arguments[arguments.length-1];

//     var slugs = '';
//     for (var i in arguments) {
//         if (i!=arguments.length-1)
//             slugs += arguments[i] + '/';
//     }

//     $.get("/api/json/manual_data/" + slugs, function(data) { successCallback(data); });
// };

// function callback(data) {
//     $('.flowchart-container').flowchart( data );
// }

// getFlowchartData( 'slug_A', 'slug_B', callback );
