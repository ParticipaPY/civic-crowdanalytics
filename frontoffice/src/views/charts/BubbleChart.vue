<script>

import { Bubble } from 'vue-chartjs'
import {Backend} from '../../Backend'

function truncate (text, max) {
  return text.substr(0, max - 1) + (text.length > max ? '…' : '')
}

export default Bubble.extend({
  components: {
    Backend
  },
  props: {
    analysisId: {type: Number, required: true}
  },
  data () {
    return {
      data: [],
      clusters: [],
      renderDatasets: [],
      colorArray: ['#1985AC', '#D39E00', '#F63C3A', '#3A9D5D', '#39B2D5']
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
    formatDataset: function () {
      let parsed = JSON.parse(this.data)
      if (parsed.length > 0) {
        this.clusters = parsed
        for (let i in parsed) {
          let newobj = {}
          newobj.label = 'Cluster ' + i
          newobj.backgroundColor = this.colorArray[i]
          newobj.data = []
          for (let j of parsed[i].ideas) {
            let ideaobj = {}
            ideaobj.x = j.posx
            ideaobj.y = j.posy
            ideaobj.r = 5
            ideaobj.label = j.idea
            newobj.data.push(ideaobj)
          }
          this.renderDatasets.push(newobj)
        }
      }
    },
    getChart: function () {
      Backend.getDocumentClustering(this.analysisId).then(
        response => {
          this.data = response.data.result
          this.formatDataset()
          this.renderChart({
            datasets: this.renderDatasets
          },
            {
              responsive: true,
              maintainAspectRatio: false,
              legend: {
                display: false
              },
              scales: {
                xAxes: [{
                  gridLines: { display: false },
                  scaleLabel: { display: false },
                  ticks: { display: false }
                }],
                yAxes: [{
                  gridLines: { display: false },
                  scaleLabel: { display: false },
                  ticks: { display: false }
                }]
              },
              tooltips: {
                callbacks: {
                  label: function (tooltipItem, data) {
                    let dataset = data.datasets[tooltipItem.datasetIndex]
                    let object = dataset.data[tooltipItem.index]
                    return `${truncate(object.label, 100)}`
                  }
                }
              }
            }
          )
        }
      )
    }
  }
})

</script>
