<script>
import { HorizontalBar } from 'vue-chartjs'

export default HorizontalBar.extend({
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart({
      labels: ['', '', '', '', '', '', '', ''],
      datasets: [
        {
          label: 'Positive',
          backgroundColor: '#3a9d5d',
          data: [0.9, 0.8, 0.8, 0.75, 0.7, 0.62, 0.50, 0.45]
        },
        {
          label: 'Neutral',
          backgroundColor: '#b0bec5',
          data: [0.20, 0.15, 0.10, -0.05, -0.10, -0.18, -0.20, 0.15]
        },
        {
          label: 'Negative',
          backgroundColor: '#f87979',
          data: [-0.9, -0.8, -0.8, -0.75, -0.7, -0.62, -0.50, -0.45]
        }
      ]
    },
      {
        responsive: true,
        maintainAspectRatio: false
      })
  }
})

//   import { Line } from 'vue-chartjs'

//   export default Line.extend({
//     props: {
//       chartData: {
//         type: Array | Object,
//         required: false
//       },
//       chartLabels: {
//         type: Array,
//         required: true
//       }
//     },
//     data () {
//       return {
//         options: {
//           scales: {
//             yAxes: [{
//               ticks: {
//                 beginAtZero: true
//               },
//               gridLines: {
//                 display: true
//               }
//             }],
//             xAxes: [ {
//               gridLines: {
//                 display: false
//               }
//             }]
//           },
//           legend: {
//             display: false
//           },
//           responsive: true,
//           maintainAspectRatio: false
//         }
//       }
//     },
//     mounted () {
//       this.renderChart({
//         labels: ['public transit', 'private transit', 'non-motor powered transit', 'infrastructure'],
//         datasets: [
//           {
//             label: 'downloads',
//             borderColor: '#249EBF',
//             pointBackgroundColor: 'white',
//             borderWidth: 1,
//             pointBorderColor: '#249EBF',
//             backgroundColor: 'transparent',
//             data: [97, 43, 136, 37]
//           }
//         ]
//       }, this.options)
//     }
//   })

</script>
