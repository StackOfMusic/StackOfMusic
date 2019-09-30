var endpoint = 'copyright';
var copyright_list = [];
var time_list = [];
var option = new Highcharts.chart('container', {

    title: {
        text: 'My Copyright'
    },

    subtitle: {
        text: 'Source: our page'
    },

    yAxis: {
        title: {
            text: 'Profit'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        series: {
            label: {
                connectorAllowed: false
            },
            pointStart: 2010
        }
    },

    series: [{
        name: 'Copyright',
        data:(function () {
            var i;
            for(i=0; i<copyright_list.length;i++){
                data.push([
                    copyright_list[i],
                    time_list[i]
                ])
            }
        })
    }],

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

});