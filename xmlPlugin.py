#import sublime, sublime_plugin
import xml.etree.ElementTree as ET
import os

class EsbAddArtifactsCommand():
	def run(self):

		self.config = "paths.xml"

		self.parsePaths = ParsePaths()

		self.deploymentPomPath = self.parsePaths.getDeploymentPomPath("paths.xml")
		self.artifactXmlPath = self.parsePaths.getArtifactXmlPath("paths.xml")

		# get the folder where artifact.xml resides
		# drop last 12 letters for 'artifact.xml'
		self.artifactXmlFolder = self.artifactXmlPath[:-12]
		print self.artifactXmlFolder

		# get list of artifacts from artifacts.xml
		self.listOfArtifacts = HelperUtil().getListOfArtifactsFromArtifactsXml(self.artifactXmlPath)

		# get list of dependencies from pom.xml
		HelperUtil().getListOfDependenciesFromDeploymentPom(self.deploymentPomPath)

		# figure out if there are some artifacts created but not added to artifacts.xml
		self.missingArtifacts = HelperUtil().findMissingArtifacts(self.listOfArtifacts, self.artifactXmlFolder)

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

class HelperUtil():
	def getListOfArtifactsFromArtifactsXml(self, artifactXmlPath):
		self.artifacts = []
		tree = ET.parse(artifactXmlPath)
		for elem in tree.iterfind("artifact/file"):
			#print elem.text.strip()
			self.artifacts.append(elem.text.strip())
		return self.artifacts


	def getListOfDependenciesFromDeploymentPom(self, deploymentPomPath):
		dependencies = []
		tree = ET.parse(deploymentPomPath)
		allDependencies = tree.findall("{http://maven.apache.org/POM/4.0.0}dependencies/{http://maven.apache.org/POM/4.0.0}dependency")
		for dependency in allDependencies:
			artifactId = dependency.find("{http://maven.apache.org/POM/4.0.0}artifactId")
			dependencies.append(artifactId.text)
		return dependencies

	def findMissingArtifacts(self, listOfArtifacts, artifactXmlFolder):
			ignoredFiles = ["synapse.xml"]
			foundFiles = []
			missingArtifacts = []

			# concat our synapse-config folder
			self.synapseConfigFolder = artifactXmlFolder + listOfArtifacts[0][:23]

			# iterate folders with assumed artifacts
			for subdir, dirs, files in os.walk(self.synapseConfigFolder):
				for file in files:
					if file not in ignoredFiles:
						# strip file path so we can compare more easily
						# full path is for example something like: '/home/user/ESBProjects/Projectname/Integrations/Mediations/Common/src/main/synapse-config/api/someapi.xml'
						position = os.path.join(subdir, file).find("src")
						# now path will be: 'src/main/synapse-config/api/someapi.xml'
						foundFile = os.path.join(subdir, file)[position:]

						if not foundFile in listOfArtifacts:
							missingArtifacts.append(foundFile)

			print missingArtifacts
			return missingArtifacts


EsbAddArtifactsCommand().run()