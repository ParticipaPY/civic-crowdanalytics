<script>

  import axios from 'axios'
  const base = 'http://159.203.77.35:8080/api'

  export const Backend = axios.create({
    baseURL: base,
    headers: {
      Accept: 'application/json'
    }
  })

  Backend.token = null

  function authCall () {
    return new Promise((resolve, reject) => {
      axios.post(`${base}${'/auth/'}`, {username: 'admin', password: '238k74i1Ct'}).then((response) => {
        resolve(response.data.token)
      }).catch((error) => {
        reject(error)
      })
    })
  }

  Backend.interceptors.request.use((config) => {
    if (Backend.token === null) {
      return authCall().then((tokenResponse) => {
        Backend.token = tokenResponse
        config.headers.Authorization = `JWT ${tokenResponse}`
        return Promise.resolve(config)
      })
    } else {
      config.headers.Authorization = `JWT ${Backend.token}`
      return Promise.resolve(config)
    }
  }, (error) => {
    return Promise.reject(error)
  })
  
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
    let projectFd = new FormData()
    let datasets = [datasetId]
    projectFd.append('name', project.name)
    projectFd.append('description', project.description)
    projectFd.append('datasets', JSON.stringify(datasets))
    projectFd.append('visibility', project.visibility)
    projectFd.append('people_editing', project.people_editing)
    return this.post('projects/', projectFd)
  }
  Backend.postSentimentAnalysis = function (projectName, projectId, datasetId, analysisConfig) {
    let sentimentAnalysisFd = new FormData()
    sentimentAnalysisFd.append('name', projectName + ' - Sentiment Analysis')
    sentimentAnalysisFd.append('project_id', projectId)
    sentimentAnalysisFd.append('dataset_id', datasetId)
    sentimentAnalysisFd.append('parameters', JSON.stringify(analysisConfig))
    return this.post('analysis/sentiment-analysis/', sentimentAnalysisFd)
  }
  Backend.postDocumentClassification = function (projectName, projectId, datasetId, analysisConfig) {
    let docClassificationFd = new FormData()
    docClassificationFd.append('name', projectName + ' - Classification')
    docClassificationFd.append('project_id', projectId)
    docClassificationFd.append('dataset_id', datasetId)
    docClassificationFd.append('parameters', JSON.stringify(analysisConfig))
    return this.post('analysis/doc-classification/', docClassificationFd)
  }
  Backend.postDocumentClustering = function (projectName, projectId, datasetId, analysisConfig) {
    let docClusteringFd = new FormData()
    docClusteringFd.append('name', projectName + ' - Clustering')
    docClusteringFd.append('project_id', projectId)
    docClusteringFd.append('dataset_id', datasetId)
    docClusteringFd.append('parameters', JSON.stringify(analysisConfig))
    return this.post('analysis/doc-clustering/', docClusteringFd)
  }
  Backend.postConceptExtraction = function (projectName, projectId, datasetId, analysisConfig) {
    let conceptExtractionFd = new FormData()
    conceptExtractionFd.append('name', projectName + ' - Concept Extraction')
    conceptExtractionFd.append('project_id', projectId)
    conceptExtractionFd.append('dataset_id', datasetId)
    conceptExtractionFd.append('parameters', JSON.stringify(analysisConfig))
    return this.post('analysis/concept-extraction/', conceptExtractionFd)
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
