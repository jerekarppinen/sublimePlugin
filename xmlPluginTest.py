from nose.tools import *
from xmlPlugin import *
import os

LIST_OF_ARTIFACTS = [
"src/main/synapse-config/sequences/MySequence.xml",
"src/main/synapse-config/endpoints/MyEndpoint.xml",
"src/main/synapse-config/api/MyApi.xml",
"src/main/synapse-config/proxy-services/MyProxy.xml",
"src/main/synapse-config/tasks/MyTask.xml"
]

LIST_OF_ARTIFACTS_2_MISSING = [
"src/main/synapse-config/sequences/MySequence.xml",
"src/main/synapse-config/endpoints/MyEndpoint.xml",
"src/main/synapse-config/api/MyApi.xml"
]

LIST_OF_DEPENDENCIES = [
"MySequence.xml",
"MyEndpoint.xml",
"MyApi.xml",
"MyProxy.xml",
"MyTask.xml"
]

def getAbsolutePath(RELATIVE_PATH):
	dir = os.path.dirname(__file__)
	return os.path.join(dir, RELATIVE_PATH)

ARTIFACT_XML_RELATIVE_PATH = "testfolders/artifact.xml"
SYNAPSE_CONFIG_RELATIVE_PATH = "testfolders/src/main/synapse-config/dummy"

ARTIFACT_XML_ABSOLUTE_PATH = getAbsolutePath(ARTIFACT_XML_RELATIVE_PATH)
SYNAPSE_CONFIG_ABSOLUTE_PATH = getAbsolutePath(SYNAPSE_CONFIG_RELATIVE_PATH)

def test_artifactXmlFileIsParsed():
	assert ParsePaths().getArtifactXmlPath("paths.xml") == "/home/jere/ESBProjects/Korppikotka/Integrations/Mediations/Common/artifact.xml"

def test_deploymentXmlFileIsParsed():
	assert ParsePaths().getDeploymentPomPath("paths.xml") == "/home/jere/ESBProjects/Korppikotka/Integrations/Deployment/pom.xml"

def test_getListOfArtifactsFromArtifactsXmlReturnsValidList():
	assert HelperUtil().getListOfArtifactsFromArtifactsXml(ARTIFACT_XML_ABSOLUTE_PATH) == LIST_OF_ARTIFACTS

def test_getListOfDependenciesFromDeploymentPomReturnsValidList():
	assert HelperUtil().getListOfDependenciesFromDeploymentPom("pom.xml") == LIST_OF_DEPENDENCIES

#def test_find2MissingArtifactsUnderSynapseConfig():
#	assert HelperUtil().findMissingArtifacts(LIST_OF_ARTIFACTS_2_MISSING, ARTIFACT_XML_ABSOLUTE_PATH) == 2