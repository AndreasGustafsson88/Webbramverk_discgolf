var chart;

        function requestData()
        {
            // Ajax call to get the Data from Flask
            var requests = $.get('/data');


            var tm = requests.done(function (result)
            {
                var series = chart.series[0],
                    shift = series.data.length > 15 ;

                // add the points
                chart.series[0].addPoint(result, true, shift);

                // call it after two seconds
                setTimeout(requestData, 2000);
            });
        }

        $(document).ready(function() {
            chart = new Highcharts.Chart({
                chart: {
                    renderTo: 'data-container',
                    defaultSeriesType: 'spline',
                    events: {
                        load: requestData
                    }
                },
                title: {
                    text: 'My Latest Rounds'
                },
                xAxis: {
                    type: 'datetime',
                    tickPixelInterval: 100,
                    maxZoom: 20 * 1000
                },
                yAxis: {
                    minPadding: 0.2,
                    maxPadding: 0.2,
                    title: {
                        text: 'Ranking',
                        margin: 80
                    }
                },
                series: [{
                    name: 'Rating',
                    data: []
                }]
            });

        });