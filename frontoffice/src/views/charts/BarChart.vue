<script>
import { Bar } from 'vue-chartjs'
import {Backend} from '../../Backend'

export default Bar.extend({
  components: {
    Backend
  },
  props: {
    analysisId: {type: Number, required: true}
  },
  data () {
    return {
      data: [],
      labels: [],
      quantity: []
    }
  },
  watch: {
    analysisId: function (n, o) {
      if (n !== 0 || n !== o) {
        this.getChart()
      }
    }
  },
  methods: {
    getChart: function () {
      Backend.getDocumentClassification(this.analysisId).then(
        response => {
          this.data = response.data.result
          this.formatDataset(this.data)
          this.renderChart({
            labels: this.labels,
            datasets: [
              {
                label: 'Ideas',
                data: this.quantity,
                backgroundColor: [
                  'rgba(255, 99, 132, 0.5)',
                  'rgba(54, 162, 235, 0.5)',
                  'rgba(255, 206, 86, 0.5)',
                  'rgba(255, 206, 86, 0.5)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 0.5)'
                ],
                borderColor: [
                  'rgba(255,99,132,1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
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
                      labelString: 'Number of Ideas'
                    }
                  }
                ],
                xAxes: [
                  {
                    categoryPercentage: 0.7,
                    barPercentage: 1.0
                  }
                ]
              }
            })
        }
      ).catch(
        e => {
          console.log(e)
        }
      )
    },
    formatDataset: function () {
      let parsed = JSON.parse(this.data)
      if (parsed.length > 0) {
        for (let d of parsed) {
          this.labels.push(d.category)
          this.quantity.push(d.ideas.length)
        }
      }
    }
  }
})
</script>
