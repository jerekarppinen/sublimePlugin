from nose.tools import *
from xmlPlugin import *


LIST_OF_ARTIFACTS =  [
"src/main/synapse-config/sequences/MySequence.xml",
"src/main/synapse-config/endpoints/MyEndpoint.xml",
"src/main/synapse-config/api/MyApi.xml",
"src/main/synapse-config/proxy-services/MyProxy.xml",
"src/main/synapse-config/tasks/MyTask.xml"
]

LIST_OF_DEPENDENCIES =  [
"MySequence.xml",
"MyEndpoint.xml",
"MyApi.xml",
"MyProxy.xml",
"MyTask.xml"
]

def test_artifactXmlFileIsParsed():
	assert ParsePaths().getArtifactXmlPath("paths.xml") == "/home/jere/ESBProjects/Korppikotka/Integrations/Mediations/Common/artifact.xml"

def test_deploymentXmlFileIsParsed():
	assert ParsePaths().getDeploymentPomPath("paths.xml") == "/home/jere/ESBProjects/Korppikotka/Integrations/Deployment/pom.xml"

def test_getListOfArtifactsFromArtifactsXmlReturnsValidList():
	assert HelperUtil().getListOfArtifactsFromArtifactsXml("artifact.xml") == LIST_OF_ARTIFACTS

def test_getListOfDependenciesFromDeploymentPomReturnsValidList():
	assert HelperUtil().getListOfDependenciesFromDeploymentPom("pom.xml") == LIST_OF_DEPENDENCIES
