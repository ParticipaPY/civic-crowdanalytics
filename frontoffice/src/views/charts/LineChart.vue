<script>
import { Line } from 'vue-chartjs'

export default Line.extend({
  mounted () {
    this.renderChart(
      {
        labels: ['Parking', 'Cars', 'Drive', 'People', 'Reduce', 'Road', 'Bike', 'Park', 'Buses', 'Walk', 'Avenue', 'Allow'],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#3a9d5d',
            borderColor: '#3a9d5d',
            data: [80, 60, 56, 55, 43, 38, 33, 28, 20, 18, 17, 10],
            fill: false,
            lineTension: 0
          }
        ]
      },
      {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        scales: {
          yAxes: [
            {
              gridLines: {
                display: true
              },
              scaleLabel: {
                display: true,
                labelString: 'Occurrences'
              }
            }
          ]
        }
      }
    )
  }
})
</script>
