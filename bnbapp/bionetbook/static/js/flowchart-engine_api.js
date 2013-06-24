(function($){

    var lastWidths = [];

    var colCount = 0;
    var colColors = []

    var onresize = function(e){

        console.log(colCount);
        // Prevent unnecessary rendering
        var widthDifferences = 0;
        $('.flowchart-table tr:first-child td').each(function(index){
            if ($(this).width() != lastWidths[index]) {
                lastWidths[index] = $(this).width();
                widthDifferences++;
            }
        });
        if (widthDifferences==0) return;

        // $('.flowchart-table tr td, .flowchart-table tr th').css({
        //     width: 99.0 / (colCount+1) + '%'
        // });

        // Fix card rows heights
        $('.flowchart-table tr').each(function(){
            $(this).find('td:not(:first-of-type)>.flowchart-card').first().children('div').each(function(){
                var index = $(this).index();
                var $siblings = $(this).parents('tr').find('td:not(:first-of-type)>.flowchart-card>div:nth-child(' + (index + 1) + ')');

                $siblings.css({ 'height' : 'auto'});

                var that = this;

                // find max height
                var maxHeight = 0;
                $siblings.each(function(){
                    var height = $(this).height();
                    if (height > maxHeight) maxHeight = height;
                });

                $siblings.each(function(){
                    if ($(this).height() >= maxHeight) return;

                    if ($(this).height() < maxHeight) {
                        $(this).height(maxHeight);
                    }
                });
            });
        });

        // Add lines
        $('.flowchart-table tr td:not(:first-child) .flowchart-line').remove();

        for (var i=1; i <= colCount; i++){
            var $filledCells = $('.flowchart-table td:nth-child('+ (i+1) +'), .flowchart-table td[colspan="' + colCount + '"]')
                .has('.flowchart-card');


            var startOffset = $('.flowchart-line-wrapper').offset().top;
            var topOffset = $filledCells.first().offset().top;
            var bottomOffset = $filledCells.last().offset().top;

            $('<div class="flowchart-line"></div>')
                .css({
                    top : topOffset - startOffset,
                    height: bottomOffset - topOffset,
                    background: 'rgba('+colColors[i-1][0]+','+colColors[i-1][1]+','+colColors[i-1][2]+',1)'
                })
                .appendTo( $('.flowchart-line-wrapper td:nth-child(' + (i+1) +') .flowchart-line-container') );
        }
    };

    var flowchart = function(container, data){
        var tableTmpl = _.template( $('#flowchart-table-template').html() );
        var rowTmpl = _.template( $('#flowchart-row-template').html() );
        var cardTmpl = _.template( $('#flowchart-card-template').html() );

        $(container).html( tableTmpl(data[0]) );
        var $tbody = $(container).find('tbody').first();

        _(data).each(function(item, index){
            var tmplData = _.extend(
                {
                    index : index+1,
                    cardTmpl : cardTmpl,
                    prepareChild : function(child, index, parent) {
                        var diff = parent.child_diff;
                        var objectids = parent.objectid;
                        var newChild = [];
                        var nonesCount = 0;
                        for (var i in objectids) {
                            if (objectids[i]=="None")
                                nonesCount++;
                        }

                        if (objectids[index]!="None") {
                            _(child).each(function(item){
                                var newItem = {};
                                _(_.keys(item)).each(function(key){
                                    if ( _(item[key]).isArray() ) {
                                        if (key=="URL" && diff=="False")
                                            newItem[key] = item[key];
                                        else {
                                            newItem[key] = item[key][index];
                                        }
                                    } else {
                                        newItem[key] = item[key];
                                    }
                                });
                                newItem.child_type = parent.child_type[index];
                                newChild.push(newItem);
                            });
                            return newChild;
                        }
                        _(child).each(function(item, i){
                            child[i].child_type = parent.child_type[index];
                        });
                        return child;
                    }
                },
                item
            );
            $tbody.append( rowTmpl(tmplData) );
        });

        colCount = $('.flowchart-table tbody tr:first td').size() - 1;

        for (var i=0; i < colCount; i++) {
            var rgba = [];
            for (var j=0; j < 3; j++)
                rgba.push(Math.floor( Math.random()* 156 + 100));
            colColors.push(rgba);
        }

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
