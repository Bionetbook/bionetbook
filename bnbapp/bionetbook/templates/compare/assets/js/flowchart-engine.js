(function($){
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
                            console.log(newChild);
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
        return this.each(function(){
            flowchart(this, data);
        });
    };
})(jQuery);
