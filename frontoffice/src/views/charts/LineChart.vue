<script>
import { Line } from 'vue-chartjs'
import {Backend} from '../../Backend'
// import _ from 'lodash'

export default Line.extend({
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
      labelData: []
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
      Backend.getConceptExtraction(this.analysisId).then(
        response => {
          this.data = response.data.result
          this.formatDataset(this.data)
          this.renderChart(
            {
              labels: this.labels,
              datasets: [
                {
                  label: 'Data One',
                  backgroundColor: '#20a8d8',
                  borderColor: '#20a8d8',
                  data: this.labelData,
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
      ).catch(
        e => {
          console.log(e)
        }
      )
    },
    formatDataset: function () {
      let parsed = JSON.parse(this.data)
      if (parsed.length > 0) {
        for (let o of parsed) {
          this.labels.push(o.concept)
          this.labelData.push(o.occurrences)
        }
      }
    }
  }
})
</script>
