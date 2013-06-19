(function($){
    var onresize = function(e){
        // var $siblings = $(this).parents('tr').find('td:not(:first-child)>.flowchart-card');

        // // clear <br>'s
        // $siblings.each(function(){
        //     $(this).children('div').each(function(){
        //         $(this).children('br').remove();
        //     });
        // });

        // $(this).children('div').each(function(){

        // });
        //

        $('.flowchart-table tr').each(function(){
            $(this).find('td:not(:first-of-type)>.flowchart-card').first().children('div').each(function(){
                var index = $(this).index();
                var $siblings = $(this).parents('tr').find('td:not(:first-of-type)>.flowchart-card>div:nth-child(' + index + ')');

                $siblings.css({ 'height' : 'auto'});

                var that = this;

                // find max height
                var maxHeight = 0;
                $siblings.each(function(){
                    var height = $(this).height();
                    if (height > maxHeight) maxHeight = height;
                });

                $siblings.each(function(){
                    console.log('height', $(this).height());
                    if ($(this).height() >= maxHeight) return;

                    if ($(this).height() < maxHeight) {
                        $(this).height(maxHeight);
                    }
                });
            });
        });
    };

    var flowchart = function(container, data){
        var tableTmpl = _.template( $('#flowchart-table-template').html() );
        var rowTmpl = _.template( $('#flowchart-row-template').html() );
        var cardTmpl = _.template( $('#flowchart-card-template').html() );

        $(container).html( tableTmpl(data) );
        var $tbody = $(container).find('tbody').first();

        _(data).each(function(item, index){
            var tmplData = _.extend(
                {
                    index : index+1,
                    cardTmpl : cardTmpl,
                    prepareChild : function(child, index, diff, durations) {
                        var newChild = [];
                        if (durations[index]!="None") {
                            _(child).each(function(item){
                                var newItem = {};
                                _(_.keys(item)).each(function(key){
                                    if (_(item[key]).isArray()) {
                                        if (key=="URL" && diff=="False")
                                            newItem[key] = item[key];
                                        else {
                                            newItem[key] = item[key][index];
                                        }
                                    } else {
                                        newItem[key] = item[key];
                                    }
                                });
                                newChild.push(newItem);
                            });
                            return newChild;
                        }
                        return child;
                    }
                },
                item
            );
            $tbody.append( rowTmpl(tmplData) );
        });


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
