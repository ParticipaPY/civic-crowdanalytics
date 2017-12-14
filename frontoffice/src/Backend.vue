<script>

  import axios from 'axios'

  export const Backend = axios.create({
    baseURL: 'http://159.203.77.35:8080/api',
    headers: {
      Accept: 'application/json'
    }
  })

  Backend.token = null

  Backend.auth = function () {
    if (this.token === null) {
      this.post('/auth/', {
        username: 'admin',
        password: '238k74i1Ct'
      }).then(
        response => {
          Backend.token = response.data.token
          Backend.defaults.headers.common['Authorization'] = response.data.token
        }
      ).catch(
        e => console.log(e)
      )
    }
  }

  Backend.interceptors.request.use(Backend.auth())
  
  Backend.projects = function () {
    return this.get('projects/')
  }

  Backend.getProjectSummary = function (projectId) {
    return this.get('/projects/' + projectId)
  }

  Backend.postProject = function (project, dataset, attributes) {
    var server = this
    let datasetFd = new FormData()
    let attributesFd = []
    for (let attr of attributes) {
      let item = {}
      item.name = attr.name
      item.attribute_type = attr.attribute_type
      item.included_in_analysis = attr.included_in_analysis
      attributesFd.push(item)
    }
    datasetFd.append('name', dataset.name)
    datasetFd.append('file', dataset.file, dataset.file.fileName)
    datasetFd.append('attributes', JSON.stringify(attributesFd))
    server.post('datasets/', datasetFd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }).then(
      response => {
        var datasetId = response.data.id
        server.post('projects/', {
          name: project.name,
          description: project.description,
          datasets: [datasetId],
          visibility: project.visibility,
          people_editing: project.people_editing
        }).then(
          response => {
            // MANUAL ANALYSIS FOR NOW
            server.post('analysis/sentiment-analysis/', {
              name: project.name + ' - Sentiment Analysis',
              project: response.data.id,
              dataset: datasetId,
              arguments: {'neu_inf_lim': -0.2, 'neu_sup_lim': 0.2}
            }).then(
              response => { console.log(response) }
            ).catch(e => console.error(e))
            server.post('analysis/doc-classification/', {
              name: project.name + ' - Classification',
              project: response.data.id,
              dataset: datasetId,
              arguments: {}
            }).then(
              response => { console.log(response) }
            ).catch(e => console.error(e))
            server.post('analysis/doc-clustering/', {
              name: project.name + ' - Clustering',
              project: response.data.id,
              dataset: datasetId,
              arguments: {}
            }).then(
              response => { console.log(response) }
            ).catch(e => console.error(e))
            server.post('analysis/concept-extraction/', {
              name: project.name + ' - Concept Extraction',
              project: response.data.id,
              dataset: datasetId,
              arguments: {}
            }).then(
              response => { console.log(response) }
            ).catch(e => console.error(e))
            return true
          }
        ).catch(
          e => {
            console.error(e)
          }
        )
      }
    ).catch(
      e => {
        console.error(e)
      }
    )
  }

  Backend.getSentimentAnalysis = function (id) {
    return this.get('/analysis/sentiment-analysis/' + id)
  }

</script>
