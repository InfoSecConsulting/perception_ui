var Index = function() {

    var dashboardMainChart = null;

    return {

        //main function
        init: function() {
            InfoSec.addResizeHandler(function() {
                jQuery('.vmaps').each(function() {
                    var map = jQuery(this);
                    map.width(map.parent().width());
                });
            });

            Index.initCharts();
            Index.initMiniCharts();
        },


        initCharts: function() {
            if (Morris.EventEmitter) {
                // Morris.Area 
                dashboardMainChart = Morris.Donut({
                    element: 'statistics',
                    padding: 0,
                    behaveLikeLine: false,
                    gridEnabled: false,
                    gridLineColor: false,
                    axes: false,
                    fillOpacity: 1,
                    data: [
                        {value: 50, label: 'Windows 7'},
                        {value: 8, label: 'Windows 8'},
                        {value: 18, label: 'Server 2012'},
                        {value: 3, label: 'Linux'}
                    ],
                    lineColors: ['#3175af', '#5C9BD1'],
                    xkey: 'dated',
                    ykeys: ['stat1', 'stat2'],
                    labels: ['Title1', 'Title2'],
                    pointSize: 0,
                    lineWidth: 0,
                    hideHover: 'auto',
                    resize: true
                });

            }
        },

        redrawCharts: function() {
            dashboardMainChart.resizeHandler();
        },

        initMiniCharts: function() {

            // IE8 Fix: function.bind polyfill
            if (InfoSec.isIE8() && !Function.prototype.bind) {
                Function.prototype.bind = function(oThis) {
                    if (typeof this !== "function") {
                        // closest thing possible to the ECMAScript 5 internal IsCallable function
                        throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
                    }

                    var aArgs = Array.prototype.slice.call(arguments, 1),
                        fToBind = this,
                        fNOP = function() {},
                        fBound = function() {
                            return fToBind.apply(this instanceof fNOP && oThis ? this : oThis,
                                aArgs.concat(Array.prototype.slice.call(arguments)));
                        };

                    fNOP.prototype = this.prototype;
                    fBound.prototype = new fNOP();

                    return fBound;
                };
            }

            $("#sparkline_bar").sparkline([8, 9, 10, 11, 10, 10, 12, 10, 10, 11, 9, 12, 11], {
                type: 'bar',
                width: '100',
                barWidth: 6,
                height: '45',
                barColor: '#F36A5B',
                negBarColor: '#e02222'
            });

            $("#sparkline_bar2").sparkline([9, 11, 12, 13, 12, 13, 10, 14, 13, 11, 11, 12, 11], {
                type: 'bar',
                width: '100',
                barWidth: 6,
                height: '45',
                barColor: '#5C9BD1',
                negBarColor: '#e02222'
            });
												
												 $("#sparkline_bar3").sparkline([8, 9, 10, 11, 10, 10, 12, 10, 10, 11, 9, 12, 11, 10, 9, 11, 13, 13, 12], {
                type: 'bar',
                width: '100',
                barWidth: 5,
                height: '55',
                barColor: '#35aa47',
                negBarColor: '#e02222'
            });

            $("#sparkline_bar4").sparkline([9, 11, 12, 13, 12, 13, 10, 14, 13, 11, 11, 12, 11, 11, 10, 12, 11, 10], {
                type: 'bar',
                width: '100',
                barWidth: 5,
                height: '55',
                barColor: '#ffb848',
                negBarColor: '#e02222'
            });

            $("#sparkline_line").sparkline([9, 10, 9, 10, 10, 11, 12, 10, 10, 11, 11, 12, 11, 10, 12, 11, 10, 12], {
                type: 'line',
                width: '100',
                height: '55',
                lineColor: '#ffb848'
            });
												
											
											$('.easy-pie-chart .number.transactions').easyPieChart({
                animate: 1000,
                size: 75,
                lineWidth: 3,
                barColor: InfoSec.getBrandColor('yellow')
            });

            $('.easy-pie-chart .number.visits').easyPieChart({
                animate: 1000,
                size: 75,
                lineWidth: 3,
                barColor: InfoSec.getBrandColor('green')
            });

            $('.easy-pie-chart .number.bounce').easyPieChart({
                animate: 1000,
                size: 75,
                lineWidth: 3,
                barColor: InfoSec.getBrandColor('red')
            });

            $('.easy-pie-chart-reload').click(function () {
                $('.easy-pie-chart .number').each(function () {
                    var newValue = Math.floor(100 * Math.random());
                    $(this).data('easyPieChart').update(newValue);
                    $('span', this).text(newValue);
                });
            });
           
        }

    };

}();