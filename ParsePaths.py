import os
import xml.etree.ElementTree as ET

class ParsePaths():
	def getDeploymentPomPath(self, pathsFile):
		pathsFile = os.path.dirname(os.path.abspath(__file__)) + "/" + pathsFile
		tree = ET.parse(pathsFile)
		for elem in tree.iterfind("deployment/deploymentPomPath"):
			return elem.text

	def getArtifactXmlPath(self, pathsFile):
		pathsFile = os.path.dirname(os.path.abspath(__file__)) + "/" + pathsFile
		tree = ET.parse(pathsFile)
		for elem in tree.iterfind("artifactXmls/artifactXml"):
			return elem.text