<script>

  import axios from 'axios'

  export const Backend = axios.create({
    baseURL: 'http://10.20.5.117:8000/api',
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

  Backend.postDataset = function (dataset, attributes) {
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
    return this.post('datasets/', datasetFd)
  }
  Backend.postProject = function (project, datasetId) {
    return this.post('projects/', {
      name: project.name,
      description: project.description,
      datasets: [datasetId],
      visibility: project.visibility,
      people_editing: project.people_editing
    })
  }
  Backend.postSentimentAnalysis = function (projectName, projectId, datasetId) {
    return this.post('analysis/sentiment-analysis/', {
      name: projectName + ' - Sentiment Analysis',
      project: projectId,
      dataset: datasetId,
      arguments: {'neu_inf_lim': -0.2, 'neu_sup_lim': 0.2}
    })
  }
  Backend.postDocumentClassification = function (projectName, projectId, datasetId) {
    return this.post('analysis/doc-classification/', {
      name: projectName + ' - Classification',
      project: projectId,
      dataset: datasetId,
      arguments: {}
    })
  }
  Backend.postDocumentClustering = function (projectName, projectId, datasetId) {
    return this.post('analysis/doc-clustering/', {
      name: projectName + ' - Clustering',
      project: projectId,
      dataset: datasetId,
      arguments: {}
    })
  }
  Backend.postConceptExtraction = function (projectName, projectId, datasetId) {
    return this.post('analysis/concept-extraction/', {
      name: projectName + ' - Concept Extraction',
      project: projectId,
      dataset: datasetId,
      arguments: {}
    })
  }

  Backend.getSentimentAnalysis = function (id) {
    return this.get('/analysis/sentiment-analysis/' + id)
  }
  Backend.getConceptExtraction = function (id) {
    return this.get('/analysis/concept-extraction/' + id)
  }
  Backend.getDocumentClassification = function (id) {
    return this.get('/analysis/doc-classification/' + id)
  }
  Backend.getDocumentClustering = function (id) {
    return this.get('/analysis/doc-clustering/' + id)
  }

</script>
