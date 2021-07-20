function renderChart(buildings, datasetOn, datasetOff)	{
    var barChartData = {
        labels: buildings,
        barPercentage: 0.1,
        categoryPercentage: 0.5,
//        barThickness: 'flex',
//        maxBarThickness: 8,
//        minBarLength: 2,
        datasets: [{
            label: 'Online',
            backgroundColor: 'rgba(0, 255, 0, 0.7)',
            data: datasetOn
        }, {
            label: 'Offline',
            backgroundColor: 'rgba(255, 0, 0, 0.7)',
            data: datasetOff
        }]
    };
    window.onload = function() {
        var ctx = document.getElementById('canvas').getContext('2d');
        window.myBar = new Chart(ctx, {
            type: 'bar',
            data: barChartData,
            options: {
                title: {
                    display: true,
                    text: 'Network Status Across Buildings'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false
                },
                responsive: true,
                scales: {
                    xAxes: [{
                        stacked: true,
                    }],
                    yAxes: [{
                        stacked: true,
                    ticks: {
                        beginAtZero: true,
                        stepSize: 1
                    }
                    }]
                }
            }
        });
    };
}

//buildings, datasetOn, datasetOff