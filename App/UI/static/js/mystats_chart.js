function render_chart(player_history) {

    let my_dates = [];
    let ratings = [];
    let avg = [];
    let tot = 0;

    for (let i = 0; i < player_history.length; i++) {
        my_dates.push(player_history[i][0])
        ratings.push(player_history[i][1])

        tot += player_history[i][1]
        avg.push(tot / (i + 1));
    }

    $(function() {
        $('#container').highcharts({

            title: {
                text: 'Rating history'
            },

            yAxis: {
                title: {
                    text: 'Rating'
                }
            },

            xAxis: {
                categories: my_dates,
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
    })
}