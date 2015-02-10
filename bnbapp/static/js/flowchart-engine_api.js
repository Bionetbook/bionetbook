(function($) {

    var containerElement;
    var lastData, lastTexts;
    var lastWidths = [];
    var colColors = [];

    var defaults = {
        displayDiff: false,
        displayComments: false,
        displayTexts: false,
        contextMenu : {
            diff : true,
            comments : true,
            texts : true
        }
    };

    var currentOptions = defaults;

    var addLines = function() {
        // Add lines
        $('.flowchart-table .flowchart-line').remove();

        var colCount = $('.flowchart-line-wrapper:first .flowchart-line-container').size();
        for (var i = 2; i < colCount; i++) {
            var $filledCells = $('.flowchart-table .flowchart-table-cell:nth-child(' + (i + 1) + '), .flowchart-table .flowchart-table-cell[colspan="' + (colCount - 2) + '"]')
                .has('.flowchart-card');

            var startOffset = $('.flowchart-line-wrapper').offset().top;
            var topOffset = $filledCells.first().find('.flowchart-card').offset().top;
            var bottomOffset = $filledCells.last().find('.flowchart-card').offset().top;

            $('<div class="flowchart-line"></div>')
                .css({
                    top: topOffset - startOffset,
                    height: bottomOffset - topOffset,
                    background: 'rgba(' + colColors[i - 2][0] + ',' + colColors[i - 2][1] + ',' + colColors[i - 2][2] + ',1)'
                })
                .appendTo($('.flowchart-line-wrapper td:nth-child(' + (i + 1) + ') .flowchart-line-container'));
        }
    };

    var addContextMenu = function() {
        $.contextMenu( 'destroy' );

        var items = {
            'comments': {
                name: 'Show comments',
                type: 'checkbox',
                selected: currentOptions.displayComments,
                events: {
                    change: function(key, opt) {
                        currentOptions.displayComments = !currentOptions.displayComments;
                        flowchart();
                        $(window).trigger('resize');
                    }
                }
            },
            'diff': {
                name: 'Show diffs',
                type: 'checkbox',
                selected: currentOptions.displayDiff,
                events: {
                    change: function(key, opt) {
                        currentOptions.displayDiff = !currentOptions.displayDiff;
                        flowchart();
                        $(window).trigger('resize');
                    }
                }
            },
            'texts': {
                name: 'Show texts',
                type: 'checkbox',
                selected: currentOptions.displayTexts,
                disabled: lastTexts.length==0,
                events: {
                    change: function(key, opt) {
                        currentOptions.displayTexts = !currentOptions.displayTexts;
                        flowchart();
                        $(window).trigger('resize');
                    }
                }
            }
        };

        _(currentOptions.contextMenu).each( function( value, key ) {
            if (!value)
                delete items[key];
        })

        $(containerElement).contextMenu({
            selector: '.flowchart-table',
            items: items,
            zIndex: 200
        });
    };

    var onresize = function(e) {
        var $textOverlay = $(containerElement).find('.flowchart-table-text-overlay-container').css({ height: 'auto' });

        $(containerElement).css({position: 'relative'});
        $(containerElement).find('.flowchart-table-body').css({ height : 'auto' });

        $(containerElement).find('.flowchart-table .flowchart-table-row').each(function(rowIndex) {
            // Maximum rows count
            var rowCount = 0;
            $(this).find('.flowchart-card-inner-table').each(function() {
                var innerTableRowsCount = $(this).find('.flowchart-card-inner-table-row').size();
                if (innerTableRowsCount > rowCount)
                    rowCount = innerTableRowsCount;
            });

            for (var i = 1; i <= rowCount; i++) {
                var maxHeight = 0;
                $(this).find('.flowchart-card-inner-table .flowchart-card-inner-table-row:nth-child(' + i + ') .flowchart-card-inner-table-cell-content').each(function() {
                    $(this).css({
                        height: 'auto'
                    });
                    maxHeight = Math.max(maxHeight, $(this).height());
                });

                $(this).find('.flowchart-card-inner-table .flowchart-card-inner-table-row:nth-child(' + i + ') .flowchart-card-inner-table-cell-content').each(function() {
                    $(this).height(maxHeight);
                });
            }
        });

        var $tBody = $(containerElement).find('.flowchart-table-body');
        var totalHeight = Math.max( $textOverlay.height(), $tBody.height() );

        $tBody.height(totalHeight);
        $textOverlay.css({
            height : totalHeight,
            width: $tBody.innerWidth(),
            top : $tBody.offset().top - $(containerElement).offset().top + 1,
            left : $tBody.offset().left - $(containerElement).offset().left + 1
        });

        if (currentOptions.displayTexts) {
            $textOverlay.css({display: 'block'});
        } else {
            $textOverlay.css({display: 'none'});
        }

        addLines();
        addContextMenu();
    };

    var normalizeCardData = function(card, keysCount, rowIndex) {
        if (card.data[0].length == keysCount) {
            card.data[0].push({
                value: ''
            });
        }
        var initialRowLength = card.data[rowIndex + 1].length;
        for (var i = 0; i < keysCount - initialRowLength; i++) {
            card.data[rowIndex + 1].push({
                value: "None"
            });
        }
        for (var cellIndex = 0; cellIndex < keysCount; cellIndex++) {
            cell = card.data[rowIndex + 1][cellIndex];
            if (!cell) {
                card.data[rowIndex + 1][cellIndex] = {
                    value: " "
                };
            } else if (!cell.value || cell.value == "None") {
                card.data[rowIndex + 1][cellIndex].value = " ";
            }

            if (_(card.data[rowIndex + 1][cellIndex].value).isArray()) {
                card.data[rowIndex + 1][cellIndex].value = card.data[rowIndex + 1][cellIndex].value.join(' ');
            }
        }

        return card;
    };

    var generateHeaders = function(json) {
        var headers = ['', ''];
        for (var i = 0; i < json[0].objectid.length; i++) {
            headers.push('Process ' + (i + 1));
        }
        return headers;
    };
    var keySortRule = function(key) {
        return key == "technique_comment" ? 1 : 0;
    };
    var getDiff = function(childKey) {
        var diff = false;
        if (childKey) {
            _(childKey).each(function(cardValue) {
                if (cardValue && cardValue != childKey[0])
                    diff = true;
            });
        }
        return diff;
    }

    var prepareData = function(json, options) {
        var headers = generateHeaders(json);
        lastTexts = [];

        var rows = [];

        // Generate colors
        if (colColors.length == 0)
            for (var i = 0; i < headers.length - 1; i++) {
                var rgba = [];
                for (var j = 0; j < 3; j++)
                    rgba.push(Math.floor(Math.random() * 156 + 100));
                colColors.push(rgba);
            }

        _(json).each(function(verb, verbIndex) {
            // For everything except text
            if (verb.text && _(verb.text).isArray()) {
                lastTexts = verb.text;
                return;
            }

            var row = [{
                isTable: false,
                isInline: false,
                isVerb: true,
                name: verb.name,
                index: verbIndex + 1,
                span: 1,
                display: true,
                objectid : _(verb.objectid).isArray() ? verb.objectid[0] : verb.objectid
            }, {
                isTable: true,
                data: [
                    [{
                        value: "Name"
                    }]
                ],
                span: 1,
                display: true
            }];

            var cardsCount = verb.child_diff == "True" ? verb.child_type.length : 1;
            for (var i = 0; i < cardsCount; i++) {
                var childType = verb.child_type[i];
                row.push({
                    isTable: (childType == "machine" || childType == "components" || childType == "thermocycle") && verb.child.length > 1,
                    isInline: childType == "manual" || verb.child.length == 1,
                    data: [
                        []
                    ],
                    display: verb.objectid[i] != "None",
                    span: verb.child_diff == "True" ? 1 : verb.child_type.length
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

            var uniqueKeys = _.union.apply(_, _(verb.child).map(function(child) {
                return _(child).keys();
            }));
            var keysCount = _(uniqueKeys).filter(function(key) {
                return !_(ignoredChildFields).contains(key);
            });
            keysCount = keysCount.length;
            console.log('keysCount', keysCount);

            _(verb.child).each(function(child, childIndex) {
                if (child.name)
                    row[1].data.push([{
                        value: _(child.name).find(function(name) {
                            return name != "None"
                        })
                    }]);

                // For each of cards
                for (var cardIndex = 0; cardIndex < cardsCount; cardIndex++) {
                    var card = row[cardIndex + 2];
                    if (card.isTable) {

                        card.data.push([]);
                        // and each of child properties
                        var childKeys = child.display_order ? _(child.display_order).flatten() : _.chain(child).keys().sortBy(keySortRule);
                        if (child.display_order) keysCount = childKeys.length;

                        _(childKeys).each(function(key) {
                            if (_(ignoredChildFields).contains(key)) return;
                            // If key is not ignored
                            // Find column to put value
                            var colIndex = -1;
                            _(card.data[0]).each(function(currentKey, currentIndex) {
                                if (currentKey.value == key)
                                    colIndex = currentIndex;
                            });
                            // add caption to card row
                            if (colIndex == -1) {
                                card.data[0].push({
                                    value: key
                                });
                                colIndex = card.data[0].length - 1;
                            }

                            // Figure out if value differs from another card
                            var diff = _(child.diff).contains(key) ? getDiff(child[key]) : false;

                            var value = child[key] ? child[key][cardIndex] : "";

                            card.data[childIndex + 1][colIndex] = {
                                value: !options.displayComments && key == "technique_comment" ? "" : value,
                                isLink: key == "link",
                                color: options.displayDiff && diff ? 'red' : ''
                            };

                        });
                        // Fill blank fields
                        normalizeCardData(card, keysCount, childIndex);

                        // Add Urls
                        if (child.URL && child['URL'][cardIndex])
                            card.data[childIndex + 1][keysCount] = {
                                value: child['URL'][cardIndex],
                                isUrl: true
                            };
                        else
                            card.data[childIndex + 1][keysCount] = {
                                value: ''
                            }
                    } else if (card.isInline) {
                        card.data = [];
                        if (_(child.display_order).isUndefined()) {
                            child.display_order = _.chain(child).keys().sortBy(keySortRule).filter(function(key) {
                                return !_(ignoredChildFields).contains(key);
                            }).value();
                        }

                        var processDisplayOrderItem = function(displayOrderRow) {
                            var newLine = [];
                            _(displayOrderRow).each(function(key) {
                                var value = child[key];
                                if (!value || value[cardIndex] == "" || value[cardIndex] == "None") return;
                                if (key != "technique_comment" || options.displayComments) {
                                    // Figure out if value differs from another card
                                    var diff = _(child.diff).contains(key) ? getDiff(child[key]) : false;
                                    var newItem = {
                                        key: key,
                                        value: value[cardIndex],
                                        color: options.displayDiff && diff ? 'red' : ''
                                    };
                                    newLine.push(newItem);
                                }
                            });
                            card.data.push(newLine);
                        };

                        if (_(child.display_order).any(function(item) {
                            return _(item).isArray();
                        })) {
                            _(child.display_order).each(processDisplayOrderItem);
                        } else {
                            processDisplayOrderItem(child.display_order);
                        }

                        if (child.URL)
                            card.url = child.URL[cardIndex];
                    }
                }
            });

            // Remove empty columns
            _(row).each(function(card, index) {
                if (index > 1 && card.isTable) {
                    for (var keyIndex = card.data[0].length - 2; keyIndex >= 0; keyIndex--) {
                        var isEmpty = _(card.data).all(function(row, index) {
                            return index === 0 || row[keyIndex].value == " ";
                        });
                        if (isEmpty)
                            _(card.data).each(function(value, index) {
                                value.splice(keyIndex, 1);
                                card.data[index] = value;
                            });
                    }
                }
            });

            rows.push(row);
        });

        return {
            rows: rows,
            headers: headers,
            texts : lastTexts
        };
    };

    var flowchart = function(container, data, options) {
        container = container || containerElement;
        data = data || lastData;
        options = options || currentOptions;

        var tableTmpl = _.template($('#new-flowchart-table-template').html());
        var preparedData = prepareData(data, options);
        $(container).html(tableTmpl(preparedData));
    };


    $.fn.flowchart = function(data, options) {

        data = data || lastData;
        lastData = data;
        if (!data) return;

        options = options || {};
        currentOptions = _.extend({}, defaults, currentOptions, options);

        containerElement = this;

        var result = this.each(function() {
            flowchart(this, data, currentOptions);
        });

        $(window).on('resize', onresize);
        $(window).trigger('resize');

        return result;
    };


})(jQuery);
