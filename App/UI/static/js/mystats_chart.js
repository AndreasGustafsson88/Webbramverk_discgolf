        Highcharts.chart('container', {

            title: {
                text: 'Rating history'
            },

            yAxis: {
                title: {
                    text: 'Rating'
                }
            },

            xAxis: {
                categories: mydates,
                labels: {
                    enabled: false
                }

            },

            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },

            series: [{
                name: 'My latest rounds',
                data: ratings
            }, {
                name: 'Average rating',
                data: avg
            }, ],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }
        })
