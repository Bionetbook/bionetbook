(function($){

    var lastWidths = [];


    var colColors = [];

    var addLines = function(){
        // Add lines
        $('.flowchart-table .flowchart-line').remove();

        var colCount = $('.flowchart-line-wrapper:first .flowchart-line-container').size();
        for (var i=2; i < colCount; i++){
            var $filledCells = $('.flowchart-table .flowchart-table-cell:nth-child('+ (i+1) +'), .flowchart-table .flowchart-table-cell[colspan="' + (colCount-2) + '"]')
                .has('.flowchart-card');


            var startOffset = $('.flowchart-line-wrapper').offset().top;
            var topOffset = $filledCells.first().find('.flowchart-card').offset().top;
            var bottomOffset = $filledCells.last().find('.flowchart-card').offset().top;

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
            card.data[0].push({value : ''});
        }
        var initialRowLength = card.data[rowIndex+1].length;
        for (var i=0; i<keysCount-initialRowLength; i++) {
            card.data[rowIndex+1].push({ value : "None" });
        }
        for (var cellIndex=0; cellIndex<keysCount; cellIndex++) {
            cell = card.data[rowIndex+1][cellIndex];
            if (!cell) {
                card.data[rowIndex+1][cellIndex] = { value : " "};
            } else if (!cell.value || cell.value=="None") {
                card.data[rowIndex+1][cellIndex].value = " ";
            }

            if (_(card.data[rowIndex+1][cellIndex].value).isArray()) {
                card.data[rowIndex+1][cellIndex].value = card.data[rowIndex+1][cellIndex].value.join(' ');
            }
        }

        return card;
    };

    var generateHeaders = function(json){
        var headers = ['',''];
        for (var i=0; i<json[0].objectid.length; i++) {
            headers.push('Process '+(i+1));
        }
        return headers;
    };
    var keySortRule = function(key){
        return key=="technique_comment" ? 1 : 0;
    };

    var prepareData = function(json, options){
        var headers = generateHeaders(json);
        var rows = [];
        _(json).each(function(verb, verbIndex){
            var row = [
            {
                isTable : false,
                isInline : false,
                isVerb : true,
                name : verb.name,
                index : verbIndex+1,
                span: 1,
                display: true
            }, {
                isTable : true,
                data : [
                    [{value: "Name"}]
                ],
                span : 1,
                display: true
            }];

            var cardsCount =  verb.child_diff=="True" ? verb.child_type.length : 1;
            for (var i=0; i<cardsCount; i++) {
                var childType = verb.child_type[i];
                row.push({
                    isTable : (childType=="machine" || childType=="components" || childType=="thermocycle") && verb.child.length>1,
                    isInline : childType=="manual" || verb.child.length==1,
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
                "display_order",
                "diff"
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
                    row[1].data.push([{value: _(child.name).find(function(name){ return name!="None"})}]);

                // For each of cards
                for (var cardIndex=0; cardIndex<cardsCount; cardIndex++){
                    var card = row[cardIndex+2];
                    if (card.isTable) {

                        card.data.push([]);
                        // and each of child properties
                        var childKeys = child.display_order ? _(child.display_order).flatten() : _.chain(child).keys().sortBy(keySortRule);
                        if (child.display_order) keysCount=childKeys.length;

                        _(childKeys).each(function(key){
                            if (_(ignoredChildFields).contains(key)) return;
                            // If key is not ignored
                            // Find column to put value
                            var colIndex = -1;
                            _(card.data[0]).each(function(currentKey, currentIndex){
                                if (currentKey.value == key)
                                    colIndex = currentIndex;
                            });
                            // add caption to card row
                            if (colIndex==-1) {
                                card.data[0].push({
                                    value: key,
                                    color: options.displayDiff && _(child.diff).contains(key) ? 'red' : ''
                                });
                                colIndex = card.data[0].length-1;
                            }
                            card.data[childIndex+1][colIndex] = {
                                value: child[key] ? child[key][cardIndex] : "",
                                isLink: key=="link"
                            };

                        });
                        // Fill blank fields
                        normalizeCardData(card, keysCount, childIndex);

                        // Add Urls
                        card.data[childIndex+1][keysCount] = {
                            value: child['URL'][cardIndex],
                            isUrl: true
                        };
                    } else if (card.isInline){
                        card.data = [];
                        if (_(child.display_order).isUndefined()) {
                            var newLine = [];
                            _.chain(child).keys().sortBy(keySortRule).each( function( key ) {
                                if (_(ignoredChildFields).contains(key)) return;
                                var value = child[key];
                                if (!value || value[cardIndex]=="" || value[cardIndex]=="None") return;
                                var newItem = {
                                    key : key,
                                    value : value[cardIndex]
                                };
                                newLine.push(newItem);
                            });
                            card.data.push(newLine);
                        } else {
                            var processDisplayOrderItem = function(displayOrderRow){
                                var newLine = [];
                                _(displayOrderRow).each(function(key){
                                    var value = child[key];
                                    if (!value || value[cardIndex]=="" ||value[cardIndex]=="None") return;
                                    var newItem = {
                                        key : key,
                                        value : value[cardIndex]
                                    };
                                    newLine.push(newItem);
                                });
                                card.data.push(newLine);
                            };

                            if (_(child.display_order).any(function(item){
                                return _(item).isArray();
                            })) {
                                _(child.display_order).each(processDisplayOrderItem);
                            } else {
                                processDisplayOrderItem(child.display_order);
                            }

                        }

                        if (child.URL)
                            card.url = child.URL[cardIndex];
                    }
                }
            });

            // Remove empty columns
            _(row).each(function(card, index){
                if (index>1 && card.isTable) {
                    for (var keyIndex=card.data[0].length-2; keyIndex>=0; keyIndex--) {
                        var isEmpty = _(card.data).all(function(row, index){
                            return index===0 || row[keyIndex].value==" ";
                        });
                        if (isEmpty)
                            _(card.data).each(function(value, index){
                                value.splice(keyIndex, 1);
                                card.data[index] = value;
                            });
                    }
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

    var flowchart = function(container, data, options){
        var tableTmpl = _.template( $('#new-flowchart-table-template').html() );
        var preparedData = prepareData(data, options);
        $(container).html( tableTmpl(preparedData) );
    };

    var defaults = {
        displayDiff : true
    };

    $.fn.flowchart = function(data, options){
        options = options || {};
        var o = _.extend({}, defaults, options);

        var result = this.each(function(){
            flowchart(this, data, o);
        });

        $(window).on('resize', onresize);
        $(window).trigger('resize');

        return result;
    };


})(jQuery);
