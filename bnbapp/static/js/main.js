function getFlowchartData(){
    return [
    {"verb_objectid": "kttj4d",
    "child_type": "components",
    "name": "combine",
    "node_type": "verb",
    "child_diff":"True",
    "URL": [
        "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/",
        "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/edit/"],
    "duration": ["240", "240"],
    "child": [
        {
            "name": ["Oligo dt", "Oligo dt"],
            "vol": [["1.0", "ul"], ["1.0", "ul"]],
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/c/f5fe2d/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/c/f5fe2d/edit/"],
            "number": "1",
            "node_objectid": "f5fe2d",
            "node_type": "components",
            "conc": [["50.0", "ng/ul"], ["100", "ng/ul"]],
            "is_sample": ["False", "False"]
        },
        {
            "name": ["dNTP", "dNTP"],
            "vol": [["1.0-10.0", "ul"], ["1.0-10.0", "ul"]],
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/c/0tisce/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/c/0tisce/edit/"],
            "number": "2",
            "node_objectid": "0tisce",
            "node_type": "components",
            "conc": [["10", "mM"], ["10", "mM"]],
            "is_sample": ["False", "False"]

        },
        {
            "name": ["RNA, poly(A)+", "RNA, poly(A)+"],
            "vol": [["1.0", "ul"], ["1.0", "ul"]],
            "number": "3",
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/c/f5fe2d/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/c/f5fe2d/edit/"],
            "node_type": "components",
            "node_objectid": "f5fe2d",
            "conc": [["100-1000", "ng/ul"], ["100-1000", "ng/ul"]],
            "is_sample": ["True", "True"]
        },
        {
            "name": ["DDW", "DDW"],
            "vol": [["up to 12", "ul"], ["up to 12", "ul"]],
            "number": "4",
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/c/1exatc/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/okeetv/kttj4d/c/1exatc/edit/"],
            "node_objectid": "1exatc",
            "node_type": "components",
            "is_sample": ["False", "False"]
        },
    ]},
    {"verb_objectid": "oy38e9",
    "child_type": "machine",
    "URL": [
        "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/oy38e9/edit/",
        "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/oy38e9/edit/"],
    "name": "heat",
    "node_type": "verb",
    "child_diff":"True",
    "duration": ["300","None"],
    "child": [
        {
            "name": ["heat block"],
            "temp": ["65", "C"],
            "time": ["5:00", "Min"],
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/oy38e9/m/bb92m1/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/oy38e9/m/bb92m1/edit/"],
            "node_objectid": "bb92m1"
        }
        ]
    },
    {"verb_objectid": "f4hds3",
    "child_type": "machine",
    "URL": [
        "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/f4hds3/edit/",
        "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/f4hds3/edit/"],
    "name": "chill",
    "node_type": "verb",
    "child_diff":"False",
    "duration": ["60","60"],
    "child": [
        {
            "name": [["heat block"],["heat block"]],
            "temp": [["4", "C"],["4", "C"]],
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/f4hds3/m/6slh85/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/f4hds3/m/6slh85/edit/"],
            "time": [["1:00", "Min"],["1:00", "Min"]],
            "node_objectid": "6slh85"
        }
        ]
    },
    {"verb_objectid": "9b92ym",
    "child_type": "machine",
    "URL": [
        "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/9b92ym/edit/",
        "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/9b92ym/edit/"],
    "name": "centrifuge",
    "node_type": "verb",
    "child_diff":"False",
    "duration": ["60", "60"],
    "child": [
        {
            "name": [["centrifuge"],["centrifuge"]],
            "temp": [["4", "C"],["4", "C"]],
            "time": [["1:00", "Min"],["1:00", "Min"]],
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/9b92ym/m/s9wupe/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/iodn2e/9b92ym/m/s9wupe/edit/"],
            "node_objectid": "s9wupe",
            "comment": ["brief", "brief"]
        }
        ]
    },
    {"verb_objectid": "892zia",
    "child_type": "components",
    "URL": [
        "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/edit/",
        "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/edit/"],
    "name": "add",
    "node_type": "verb",
    "child_diff":"True",
    "duration": ["240", "300"],
    "child": [
        {
            "name": ["1st strand cDNA synthesis buffer", "1st strand cDNA synthesis buffer"],
            "vol": [["1.0", "ul"], ["1.0", "ul"]],
            "number": "1",
            "node_objectid": "d5fd4e",
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/c/d5fd4e/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/c/d5fd4e/edit/"],
            "node_type": "components",
            "conc": [["10.0", "X"], ["10.0", "X"]],
            "is_sample": ["False", "False"]
        },
        {
            "name": ["DTT", "None"],
            "vol": [["1.0", "ul"], ["None"]],
            "number": "2",
            "node_objectid": "5gw90k",
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/c/5gw90k/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/c/5gw90k/edit/"],
            "node_type": "components",
            "conc": [["10", "mM"], ["None"]],
            "is_sample": ["False", "False"]
        },
        {
            "name": ["Nuclease Free Water", "Nuclease Free Water"],
            "vol": [["up to 19", "ul"], ["up to 19", "ul"]],
            "number": "3",
            "node_objectid": "th2c9d",
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/c/th2c9d/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/892zia/c/th2c9d/edit/"],
            "node_type": "components",
            "is_sample": ["False", "False"]

        }
        ]
    },
    {"verb_objectid": "kbzqcb",
    "child_type": "machine",
    "URL": [
        "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/kbzqcb/edit/",
        "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/kbzqcb/edit/"],
    "name": "centrifuge",
    "node_type": "verb",
    "child_diff":"False",
    "duration": ["60", "60"],
    "child": [
        {
            "name": [["centrifuge"],["centrifuge"]],
            "temp": [["4", "C"],["4", "C"]],
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/kbzqcb/m/g2943s/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/m4wn8n/kbzqcb/m/g2943s/edit/"],
            "time": [["1:00", "Min"],["1:00", "Min"]],
            "node_objectid": "g2943s",
            "comment": ["brief", "brief"]
        }
        ]
    },
    {"verb_objectid": "j4json",
    "child_type": "machine",
    "URL": [
        "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/k0ul5c/j4json/edit/",
        "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/k0ul5c/j4json/edit/"],
    "name": "incubate",
    "node_type": "verb",
    "child_diff":"True",
    "duration": ["120", "120"],
    "child": [
        {
            "name": [["incubator"],["incubator"]],
            "temp": [["50", "C"],["42", "C"]],
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/k0ul5c/j4json/m/q249s2/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/k0ul5c/j4json/m/q249s2/edit/"],
            "time": [["2:00", "Min"],["2:00", "Min"]],
            "node_objectid": "q249s2"
        }
        ]
    },
    {"verb_objectid": "muwzdb",
    "child_type": "components",
    "name": "add",
    "URL": [
        "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/muwzdb/edit/",
        "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/muwzdb/edit/"],
    "node_type": "verb",
    "child_diff":"False",
    "duration": ["60", "60"],
    "child": [
        {
            "name": ["Superscript II", "Superscript II"],
            "vol": [["1.0", "ul"], ["1.0", "ul"]],
            "number": "1",
            "node_objectid": "w3v4gn",
            "node_type": "components",
            "URL": [
                "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/muwzdb/c/w3v4gn/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/muwzdb/c/w3v4gn/edit/"],
            "conc": [["200.0", "U/ul"], ["200.0", "U/ul"]],
            "is_sample": ["False", "False"]
        }
        ]
    },
    {"verb_objectid": "aoymzg",
    "child_type": "manual",
    "name": "mix",
    "node_type": "verb",
    "URL": [
        "/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/aoymzg/edit/",
        "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/aoymzg/edit/"],
    "child_diff":"True",
    "duration": ["None", "60"],
    "child": [
        {
            "name": [["None"],["mix"]],
            "comment": [["None"],["Gentle flicking"]]
        }
        ]
    },
    {"verb_objectid": "thfavi",
    "child_type": "machine",
    "URL":
        ["/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/thfavi/edit/",
        "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/thfavi/edit/"],
    "name": "centrifuge",
    "node_type": "verb",
    "child_diff":"True",
    "duration": ["60", "60"],
    "child": [
        {
            "name": [["centrifuge"],["centrifuge"]],
            "temp": [["4", "C"],["8", "C"]],
            "URL":
                ["/bionetbook/20-bionetbook-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/thfavi/m/sib53v/edit/",
                "/bionetbook/19-bionetbook-first-strand-cdna-synthesis-oligodt/kpvqnc/thfavi/m/sib53v/edit/"],
            "time": [["1:00", "Min"],["1:00", "Min"]],
            "node_objectid": "sib53v",
            "comment": ["brief", "brief"]
        }
        ]
    }
]

};

$(function(){

    $('.flowchart-container').flowchart(getFlowchartData());

});
