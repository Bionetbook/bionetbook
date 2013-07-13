(function($){

    var lastWidths = [];


    var colColors = [];

    var addLines = function(){
        // Add lines
        $('.flowchart-table .flowchart-table-cell:not(:first-of-type) .flowchart-line').remove();

        var colCount = $('.flowchart-table-row:first .flowchart-table-cell').size();
        for (var i=2; i < colCount; i++){
            var $filledCells = $('.flowchart-table .flowchart-table-cell:nth-child('+ (i+1) +'), .flowchart-table .flowchart-table-cell[colspan="' + (colCount-2) + '"]')
                .has('.flowchart-card');


            var startOffset = $('.flowchart-line-wrapper').offset().top;
            var topOffset = $filledCells.first().offset().top;
            var bottomOffset = $filledCells.last().offset().top;

            $('<div class="flowchart-line"></div>')
                .css({
                    top : topOffset - startOffset,
                    height: bottomOffset - topOffset,
                    background: 'rgba('+colColors[i-2][0]+','+colColors[i-2][1]+','+colColors[i-2][2]+',1)'
                })
                .appendTo( $('.flowchart-line-wrapper td:nth-child(' + (i+1) +') .flowchart-line-container') );
        }
    };

    var onresize = function(e){
        $('.flowchart-table .flowchart-table-row').each(function(){
            // Maximum rows count
            var rowCount = 0;
            $(this).find('.flowchart-card-inner-table').each(function(){
                var innerTableRowsCount = $(this).find('.flowchart-card-inner-table-row').size();
                if (innerTableRowsCount>rowCount)
                    rowCount = innerTableRowsCount;
            });

            for (var i=1; i<=rowCount; i++) {
                var maxHeight = 0;
                $(this).find('.flowchart-card-inner-table .flowchart-card-inner-table-row:nth-child('+i+') .flowchart-card-inner-table-cell-content').each(function(){
                    $(this).css({height:'auto'});
                    maxHeight = Math.max(maxHeight, $(this).height());
                });

                $(this).find('.flowchart-card-inner-table .flowchart-card-inner-table-row:nth-child('+i+') .flowchart-card-inner-table-cell-content').each(function(){
                    $(this).height(maxHeight);
                });

            }
        });

        addLines();
    };



    var normalizeCardData = function(card, keysCount, rowIndex){
        if (card.data[0].length==keysCount) {
            card.data[0].push('');
        }
        var initialRowLength = card.data[rowIndex+1].length;
        for (var i=0; i<keysCount-initialRowLength; i++) {
            card.data[rowIndex+1].push("None");
        }
        _(card.data[rowIndex+1]).each(function(cell, index, list){
            if (!cell || cell=="None")
                list[index] = "&lt;blank&gt;";
        });

        return card;
    };

    var generateHeaders = function(json){
        var headers = ['',''];
        for (var i=0; i<json[0].objectid.length; i++) {
            headers.push('Process '+(i+1));
        }
        return headers;
    };

    var prepareData = function(json){
        var headers = generateHeaders(json);
        var rows = [];
        _(json).each(function(verb, verbIndex){
            var row = [
            {
                isTable : false,
                name : verb.name,
                index : verbIndex+1,
                span: 1,
                display: true
            }, {
                isTable : true,
                data : [
                    ["Name"]
                ],
                span : 1,
                display: true
            }];

            var cardsCount =  verb.child_diff=="True" ? verb.child_type.length : 1;
            for (var i=0; i<cardsCount; i++) {
                row.push({
                    isTable : true,
                    data : [
                        []
                    ],
                    display: verb.objectid[i]!="None",
                    span: verb.child_diff=="True" ? 1 : verb.child_type.length
                });
            }

            var ignoredChildFields = [
                "URL",
                "node_type",
                "name",
                "verb",
                "objectid",
                "display_order"
            ];
            // find count of unique keys

            var uniqueKeys = _.union.apply(_, _(verb.child).map(function(child){
                return _(child).keys();
            }));
            var keysCount = _(uniqueKeys).filter(function(key){
                            return !_(ignoredChildFields).contains(key);
                        });
            keysCount = keysCount.length;
            console.log('keysCount', keysCount);

            _(verb.child).each(function(child, childIndex){
                if (child.name)
                    row[1].data.push([_(child.name).find(function(name){ return name!="None"})]);
                // For each of cards
                for (var cardIndex=0; cardIndex<cardsCount; cardIndex++){
                    var card = row[cardIndex+2];
                    card.data.push([]);
                    // and each of child properties
                    _.chain(child).keys().each(function(key){
                        if (_(ignoredChildFields).contains(key)) return;
                        // If key is not ignored
                        // Find column to put value
                        var colIndex = _(card.data[0]).indexOf(key);
                        // add caption to card row
                        if (colIndex==-1) {
                            card.data[0].push(key);
                            colIndex = card.data[0].length-1;
                        }
                        card.data[childIndex+1][colIndex] = child[key][cardIndex];
                    });



                    // Fill blank fields
                    normalizeCardData(card, keysCount, childIndex);

                    // Add Urls
                    card.data[childIndex+1][keysCount] = child['URL'][cardIndex];

                }
            });

            rows.push(row);
        });

        for (var i=0; i < headers.length-1; i++) {
            var rgba = [];
            for (var j=0; j < 3; j++)
                rgba.push(Math.floor( Math.random()* 156 + 100));
            colColors.push(rgba);
        }

        return {
            rows : rows,
            headers : headers
        };
    };

    var flowchart = function(container, data){
        var tableTmpl = _.template( $('#new-flowchart-table-template').html() );
        var preparedData = prepareData(data)
        $(container).html( tableTmpl(preparedData) );
    };

    $.fn.flowchart = function(data){
        var result = this.each(function(){
            flowchart(this, data);
        });

        $(window).on('resize', onresize);
        $(window).trigger('resize');

        return result;
    };


})(jQuery);
