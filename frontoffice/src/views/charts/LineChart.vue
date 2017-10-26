<script>
import { Line } from 'vue-chartjs'

export default Line.extend({
  mounted () {
    this.renderChart(
      {
        labels: ['city', 'homeless', 'school', 'fix', 'community', 'help', 'youth', 'street', 'housing', 'repair', 'program', 'road', 'trash', 'park', 'center'],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#20a8d8',
            borderColor: '#20a8d8',
            data: [139, 136, 118, 110, 98, 80, 77, 70, 66, 57, 55, 54, 53, 53, 51],
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
