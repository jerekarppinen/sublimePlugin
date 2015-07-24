from nose.tools import *
from xmlPlugin import *
import os
import filecmp

def getAbsolutePath(RELATIVE_PATH):
	dir = os.path.dirname(__file__)
	return os.path.join(dir, RELATIVE_PATH)

FINALLY_EXPECTED_LIST_OF_ARTIFACTS = [
"src/main/synapse-config/sequences/MySequence.xml",
"src/main/synapse-config/endpoints/MyEndpoint.xml",
"src/main/synapse-config/api/MyApi.xml",
"src/main/synapse-config/proxy-services/MyProxy.xml",
"src/main/synapse-config/tasks/MyTask.xml"
]

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
'MySequence',
'MyEndpoint',
'MyApi',
'MyProxy',
'MyTask'
]

LIST_OF_PROPERTIES = {
'MyApi': 'fi.company.project.api_._MyApi',
'MySequence': 'fi.company.project.sequence_._MySequence',
'MyProxy': 'fi.company.project.proxy-service_._MyProxy',
'.company.project.task._MyTask': 'fi.company.project.task._MyTask',
'MyEndpoint': 'fi.company.project.endpoint_._MyEndpoint'
}



LIST_OF_MISSING_PROPERTIES = [
'src/main/synapse-config/sequences/MySequence.xml',
'src/main/synapse-config/proxy-services/MyProxy.xml'
]

LIST_OF_DEPENDENCIES_2_MISSING = [
'MySequence',
'MyEndpoint',
'MyApi'
]

LIST_OF_2_MISSING_DEPENDENCIES = [
"src/main/synapse-config/proxy-services/MyProxy.xml",
"src/main/synapse-config/tasks/MyTask.xml"
]

LIST_OF_2_MISSING_ARTIFACTS = [
"src/main/synapse-config/proxy-services/MyProxy.xml",
"src/main/synapse-config/tasks/MyTask.xml"
]

TESTFOLDERS_PATH = getAbsolutePath("testfolders/")
ARTIFACT_XML_ABSOLUTE_PATH = getAbsolutePath("testfolders/artifact.xml")
ARTIFACT_XML_MISSING_TWO_ARTIFACTS_ABSOLUTE_PATH = getAbsolutePath("testfolders/artifact_missing_two_artifacts.xml")

def test_artifactXmlFileIsParsed():
	assert ParsePaths().getArtifactXmlPath("paths.xml") == "/home/jere/Projects/SublimePlugin/testfolders/artifact.xml"

def test_deploymentXmlFileIsParsed():
	assert ParsePaths().getDeploymentPomPath("paths.xml") == "/home/jere/Projects/SublimePlugin/testfolders/deployment/pom.xml"

def test_getListOfArtifactsFromArtifactsXmlThatReturnsValidList():
	assert HelperUtil().getListOfArtifactsFromArtifactsXml(ARTIFACT_XML_ABSOLUTE_PATH).sort() == LIST_OF_ARTIFACTS.sort()

def test_getListOfDependenciesFromDeploymentPom():
	assert HelperUtil().getListOfDependenciesFromDeploymentPom(TESTFOLDERS_PATH + "deployment/pom.xml") == LIST_OF_DEPENDENCIES

def test_find2MissingArtifactsUnderSynapseConfigWhichShouldBeInArtifactXml():
	assert HelperUtil().findMissingArtifacts(LIST_OF_ARTIFACTS_2_MISSING, TESTFOLDERS_PATH) == LIST_OF_2_MISSING_ARTIFACTS

def test_find2MissingDependenciesUnderSynapseConfigWhichShouldBeInPomDependencies():
	assert HelperUtil().findMissingDependencies(LIST_OF_DEPENDENCIES_2_MISSING, TESTFOLDERS_PATH) == LIST_OF_2_MISSING_DEPENDENCIES

def test_getProjectNameFromDeploymentPom():
	assert HelperUtil().getProjectNameFromDeploymentPom(TESTFOLDERS_PATH + "deployment/pom.xml") == "fi.company.project"

def test_getVersionFromDeploymentPom():
	assert HelperUtil().getVersionFromDeploymentPom(TESTFOLDERS_PATH + "deployment/pom.xml") == "1.0.0"

def test_dontFindAnyMissingDependenciesUnderSynapseConfigWhichShouldBeInPomDependencies():
	assert HelperUtil().findMissingDependencies(LIST_OF_DEPENDENCIES, TESTFOLDERS_PATH) == []

def test_getListOfPropertiesFromDeploymentPom():
	assert HelperUtil().getListOfPropertiesFromDeploymentPom(TESTFOLDERS_PATH + "deployment/pom.xml") == LIST_OF_PROPERTIES

# def test_artifactXmlWrite():
# 	assert WriteXmlFiles().writeArtifacts(LIST_OF_2_MISSING_ARTIFACTS, ARTIFACT_XML_MISSING_TWO_ARTIFACTS_ABSOLUTE_PATH, "1.0.0") == True

# def test_deploymentDependenciesWrite():
# 	assert WriteXmlFiles().writeDependencies(LIST_OF_2_MISSING_DEPENDENCIES, TESTFOLDERS_PATH + "deployment/pom.xml", "fi.company.project" , "1.0.0") == "

# def test_writeDeploymentProperties():
# 	assert WriteXmlFiles().writeProperties(LIST_OF_MISSING_PROPERTIES, TESTFOLDERS_PATH + "deployment/pom.xml", "fi.company.project" , "1.0.0") == ""