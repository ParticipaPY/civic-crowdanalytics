<script>

import { Scatter } from 'vue-chartjs'

export default Scatter.extend({
  mounted () {
    this.renderChart({
      datasets: [
        {
          label: 'Positive',
          fill: false,
          backgroundColor: '#3a9d5d',
          borderColor: '#3a9d5d',
          pointStyle: 'triangle',
          pointRadius: 5,
          data: [
              {x: 0, y: 1},
              {x: 0.2, y: 0.95},
              {x: 0.4, y: 0.91},
              {x: 0.6, y: 0.86},
              {x: 0.8, y: 0.79},
              {x: 1, y: 0.72},
              {x: 1.2, y: 0.65},
              {x: 1.4, y: 0.59},
              {x: 1.6, y: 0.51},
              {x: 1.8, y: 0.46},
              {x: 2, y: 0.40},
              {x: 2.2, y: 0.35},
              {x: 2.4, y: 0.33},
              {x: 2.6, y: 0.30}
          ]
        },
        {
          label: 'Neutral',
          fill: false,
          backgroundColor: '#b0bec5',
          borderColor: '#b0bec5',
          pointStyle: 'triangle',
          pointRadius: 5,
          data: [
              {x: 2.8, y: 0.20},
              {x: 3, y: 0.14},
              {x: 3.2, y: 0.11},
              {x: 3.4, y: 0.09},
              {x: 3.6, y: 0.09},
              {x: 3.8, y: 0.09},
              {x: 4, y: 0.02},
              {x: 4.2, y: -0.03},
              {x: 4.4, y: -0.03},
              {x: 4.6, y: -0.03},
              {x: 4.8, y: -0.08},
              {x: 5.2, y: -0.08}
          ]
        },
        {
          label: 'Negative',
          fill: false,
          backgroundColor: '#f87979',
          borderColor: '#f87979',
          pointStyle: 'triangle',
          pointRadius: 5,
          data: [
              {x: 5.4, y: -0.23},
              {x: 5.6, y: -0.26},
              {x: 5.8, y: -0.31},
              {x: 6, y: -0.37},
              {x: 6.2, y: -0.37},
              {x: 6.4, y: -0.41},
              {x: 6.6, y: -0.42},
              {x: 6.8, y: -0.51},
              {x: 7, y: -0.53},
              {x: 7.2, y: -0.60},
              {x: 7.4, y: -0.67},
              {x: 7.6, y: -0.68},
              {x: 7.8, y: -0.71},
              {x: 8, y: -0.71}
          ]
        }]
    },
      {
        responsive: true,
        maintainAspectRatio: false,
        showLines: false,
        legend: {
          display: true
        },
        scales: {
          yAxes: [
            {
              gridLines: {
                display: true
              },
              scaleLabel: {
                display: true,
                labelString: 'Aggregate Score'
              }
            }
          ],
          xAxes: [
            {
              display: false,
              gridLines: {
                display: false
              }
            }
          ]
        }
      })
  }
})

</script>
