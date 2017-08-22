<script>

import { Bubble } from 'vue-chartjs'

export default Bubble.extend({
  mounted () {
    this.renderChart({
      datasets: [
        {
          label: '',
          backgroundColor: '#3a9d5d',
          data: [
            {x: 4, y: 17, r: 5},
            {x: 8, y: 18, r: 5},
            {x: 9, y: 22, r: 5},
            {x: 10, y: 18, r: 5},
            {x: 7, y: 20, r: 5},
            {x: 7, y: 23, r: 5},
            {x: 8, y: 25, r: 5},
            {x: 12, y: 22, r: 5},
            {x: 10, y: 20, r: 5},
            {x: 10, y: 25, r: 5},
            {x: 12, y: 20, r: 5},
            {x: 8, y: 22, r: 5},
            {x: 5, y: 18, r: 5}
          ]
        },
        {
          label: '',
          backgroundColor: '#f87979',
          data: [
            {x: 36, y: 3, r: 5},
            {x: 38, y: 7, r: 5},
            {x: 39, y: 7, r: 5},
            {x: 33, y: 8, r: 5},
            {x: 40, y: 3, r: 5},
            {x: 35, y: 8, r: 5},
            {x: 40, y: 10, r: 5}
          ]
        },
        {
          label: '',
          backgroundColor: '#20a8d8',
          data: [
            {x: 19, y: 8, r: 5},
            {x: 15, y: 9, r: 5},
            {x: 18, y: 8, r: 5},
            {x: 16, y: 10, r: 5},
            {x: 18, y: 11, r: 5},
            {x: 20, y: 12, r: 5},
            {x: 21, y: 11, r: 5}
          ]
        }
      ]
    },
      {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false
        }
      }
    )
  }
})

</script>
