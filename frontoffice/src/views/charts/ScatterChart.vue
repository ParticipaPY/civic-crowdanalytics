<script>

import {Scatter} from 'vue-chartjs'
import {Backend} from '../../Backend'
import _ from 'lodash'

function truncate (text, max) {
  return text.substr(0, max - 1) + (text.length > max ? '…' : '')
}

export default Scatter.extend({
  components: {
    Backend
  },
  props: {
    analysisId: {type: Number, required: true}
  },
  data () {
    return {
      data: [],
      positiveData: [],
      neutralData: [],
      negativeData: []
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
      Backend.getSentimentAnalysis(this.analysisId).then(
        response => {
          this.data = response.data.result
          this.formatDataset(this.data)
          this.renderChart({
            datasets: [
              {
                label: 'Positive',
                fill: false,
                backgroundColor: '#3a9d5d',
                borderColor: '#3a9d5d',
                pointStyle: 'triangle',
                pointRadius: 5,
                data: this.positiveData
              },
              {
                label: 'Neutral',
                fill: false,
                backgroundColor: '#b0bec5',
                borderColor: '#b0bec5',
                pointStyle: 'triangle',
                pointRadius: 5,
                data: this.neutralData
              },
              {
                label: 'Negative',
                fill: false,
                backgroundColor: '#f87979',
                borderColor: '#f87979',
                pointStyle: 'triangle',
                pointRadius: 5,
                data: this.negativeData
              }
            ]
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
              },
              tooltips: {
                callbacks: {
                  label: function (tooltipItem, data) {
                    let dataset = data.datasets[tooltipItem.datasetIndex]
                    let object = dataset.data[tooltipItem.index]
                    return `${truncate(object.label, 100)}`
                  }
                }
              },
              onClick: (e, i) => {
                console.log(i)
                console.log(this.data)
                console.log(i[0]._index)
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
      let ret = []
      if (parsed.length > 0) {
        let positiveParsed = _.filter(parsed, (v, k) => v.sentiment === 'pos')[0]
        let neutralParsed = _.filter(parsed, (v, k) => v.sentiment === 'neu')[0]
        let negativeParsed = _.filter(parsed, (v, k) => v.sentiment === 'neg')[0]
        let totalDataLength = positiveParsed.ideas.length + neutralParsed.ideas.length + negativeParsed.ideas.length
        let dataXPosIncrement = 10 / totalDataLength
        let header = 0
        positiveParsed.ideas = _.orderBy(positiveParsed.ideas, ['score'], ['desc'])
        neutralParsed.ideas = _.orderBy(neutralParsed.ideas, ['score'], ['desc'])
        negativeParsed.ideas = _.orderBy(negativeParsed.ideas, ['score'], ['desc'])
        for (let pos of positiveParsed.ideas) {
          let obj = {}
          obj.x = dataXPosIncrement * header
          obj.y = pos.score
          obj.label = pos.idea
          header += 1
          this.positiveData.push(obj)
        }
        for (let neu of neutralParsed.ideas) {
          let obj = {}
          obj.x = dataXPosIncrement * header
          obj.y = neu.score
          obj.label = neu.idea
          header += 1
          this.neutralData.push(obj)
        }
        for (let neg of negativeParsed.ideas) {
          let obj = {}
          obj.x = dataXPosIncrement * header
          obj.y = neg.score
          obj.label = neg.idea
          header += 1
          this.negativeData.push(obj)
        }
        ret.push(this.positiveData, this.neutralData, this.negativeData)
      }
      return ret
    }
  }
})

</script>
