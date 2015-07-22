#import sublime, sublime_plugin
import xml.etree.ElementTree as ET
import os
import re

class EsbAddArtifactsCommand():
	def run(self):

		self.config = "paths.xml"

		self.parsePaths = ParsePaths()

		self.deploymentPomPath = self.parsePaths.getDeploymentPomPath("paths.xml")
		self.artifactXmlPath = self.parsePaths.getArtifactXmlPath("paths.xml")

		# get the folder where artifact.xml resides
		# drop last 12 letters for 'artifact.xml'
		self.artifactXmlFolder = self.artifactXmlPath[:-12]

		self.projectName = HelperUtil().getProjectNameFromDeploymentPom(self.deploymentPomPath)

		self.version = HelperUtil().getVersionFromDeploymentPom(self.deploymentPomPath)

		# get list of artifacts from artifacts.xml
		self.listOfArtifacts = HelperUtil().getListOfArtifactsFromArtifactsXml(self.artifactXmlPath)

		# get list of dependencies from pom.xml
		self.listOfDependencies = HelperUtil().getListOfDependenciesFromDeploymentPom(self.deploymentPomPath)

		# figure out if there are some artifacts created but not added to artifacts.xml
		self.missingArtifacts = HelperUtil().findMissingArtifacts(self.listOfArtifacts, self.artifactXmlFolder)

		# figure out if there are some artifacts created but not added to pom.xml
		self.missingDependencies = HelperUtil().findMissingDependencies(self.listOfDependencies, self.artifactXmlFolder)

		# if found any, add new artifacts to artifacts.xml
		print len(self.missingArtifacts)
		if len(self.missingArtifacts) > 0:
			WriteXmlFiles().writeArtifacts(self.missingArtifacts, self.artifactXmlPath, self.version)
		else:
			print "No new artifacts."

		# and new dependencies to pom.xml
		print len(self.missingDependencies)
		if len(self.missingDependencies) > 0:
			WriteXmlFiles().writeDependencies(self.missingDependencies, self.deploymentPomPath, self.projectName, self.version)
		else:
			print "No new dependencies"


class WriteXmlFiles():
	def writeArtifacts(self, missingArtifacts, artifactXmlPath, version):

		for missingArtifact in missingArtifacts:

					artifactParts = missingArtifact.split("/")

					artifactType = artifactParts[3]
					artifactName = artifactParts[4]

					projectName = "korppikotka"

					artifactTypeWithPossiblePlural = artifactType

					artifactType = HelperUtil().getRidOfPlural(artifactType)

					groupId = "fi.mystes." + projectName + "." + artifactType
					artifactType = "synapse/" + artifactType
					
					tree = ET.parse(artifactXmlPath)
					root = tree.getroot()
					artifactElement = ET.Element("artifact", groupId=groupId, name=artifactName, serverRole="EnterpriseServiceBus", type=artifactType, version=version)

					fileElement = ET.Element("file")
					fileElement.text = "src/main/synapse-config/" + artifactTypeWithPossiblePlural + "/" + artifactName

					root.append(artifactElement)
					artifactElement.append(fileElement)

					tree.write(artifactXmlPath)

	def writeDependencies(self, missingDependencies, deploymentPomPath, projectName, version):

		for missingDependency in missingDependencies:
			# a little hack to extract artifact type from the file path
			result = re.search('src/main/synapse-config/(.*)/', missingDependency)
			artifactType = result.group(1)
			artifactTypeWithPossiblePlural = artifactType
			artifactType = HelperUtil().getRidOfPlural(artifactType)

			groupId = projectName + "." + artifactType

			positionOfLastForwardSlash = missingDependency.rfind("/")
			positionOfLastPoint = missingDependency.rfind(".")

			artifactName = missingDependency[positionOfLastForwardSlash+1:positionOfLastPoint]
			
			simpleType = "xml"

			ET.register_namespace('', 'http://maven.apache.org/POM/4.0.0')

			tree = ET.parse(deploymentPomPath)
			root = tree.getroot()

			dependenciesElement = root.find("{http://maven.apache.org/POM/4.0.0}dependencies")
			
			dependencyElement = ET.Element("dependency")

			groupIdElement = ET.Element("groupId")
			groupIdElement.text = groupId

			artifactIdElement = ET.Element("artifactId")
			artifactIdElement.text = artifactName

			versionElement = ET.Element("version")
			versionElement.text = version

			typeElement = ET.Element("type")
			typeElement.text = simpleType


			dependencyElement.append(groupIdElement)
			dependencyElement.append(artifactIdElement)
			dependencyElement.append(versionElement)
			dependencyElement.append(typeElement)

			dependenciesElement.append(dependencyElement)

			tree.write(deploymentPomPath)



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

	def getProjectNameFromDeploymentPom(self, deploymentPomPath):
		tree = ET.parse(deploymentPomPath)
		parent = tree.findall("{http://maven.apache.org/POM/4.0.0}parent")
		for element in parent:
			projectName = element.find("{http://maven.apache.org/POM/4.0.0}groupId")
		return projectName.text

	def getVersionFromDeploymentPom(self, deploymentPomPath):
		tree = ET.parse(deploymentPomPath)
		parent = tree.findall("{http://maven.apache.org/POM/4.0.0}parent")
		for element in parent:
			version = element.find("{http://maven.apache.org/POM/4.0.0}version")
		return version.text		

	# takes list of artifacts found from artifact.xml and compares it to actual files
	def findMissingArtifacts(self, listOfArtifacts, artifactXmlFolder):
			ignoredFiles = ["synapse.xml"]
			foundFiles = []
			missingArtifacts = []

			# concat our synapse-config folder
			self.synapseConfigFolder = artifactXmlFolder + "src/main/synapse-config"

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
			return missingArtifacts

	# takes list of dependencies found from pom.xml and compares it to actual files
	# note that I first tried to implement finding missing artifacts and dependencies in the same function
	# but listOfArtifacts contain full filepaths and listOfDependencies contain just names, and I could not get
	# comparing substrings work when I had to find them inside a list
	# (e.g '[MyApi.xml, MyProxy.xml]' found in (src/main/synapse-config/api/MyApi.xml, src/main/synapse-config/proxy-services/MyProxy.xml))

	def findMissingDependencies(self, listOfDependencies, artifactXmlFolder):
			ignoredFiles = ["synapse.xml"]
			foundFiles = []
			missingDependencies = []

			# concat our synapse-config folder
			self.synapseConfigFolder = artifactXmlFolder + "src/main/synapse-config"

			# iterate folders with assumed artifacts
			for subdir, dirs, files in os.walk(self.synapseConfigFolder):
				for file in files:
					if file not in ignoredFiles:

						# strip file path so we can compare more easily
						# full path is for example something like: '/home/user/ESBProjects/Projectname/Integrations/Mediations/Common/src/main/synapse-config/api/someapi.xml'
						# Python does not provide switch-case so use bunch of ifs
						if os.path.join(subdir, file).find("api") > -1:
							position = os.path.join(subdir, file).find("api")
							# now path will be: 'MyApi.xml'
							# position + 4 because want to exclude api/							
							foundFile = os.path.join(subdir, file)[position+4:]

						elif os.path.join(subdir, file).find("proxy-services") > -1:
							position = os.path.join(subdir, file).find("proxy-services")
							foundFile = os.path.join(subdir, file)[position+15:]

						elif os.path.join(subdir, file).find("sequences") > -1:
							position = os.path.join(subdir, file).find("sequences")
							foundFile = os.path.join(subdir, file)[position+10:]

						elif os.path.join(subdir, file).find("endpoints") > -1:
							position = os.path.join(subdir, file).find("endpoints")
							foundFile = os.path.join(subdir, file)[position+10:]

						elif os.path.join(subdir, file).find("tasks") > -1:
							position = os.path.join(subdir, file).find("tasks")
							foundFile = os.path.join(subdir, file)[position+6:]

						position = os.path.join(subdir, file).find("src")

						foundFileWithFullPath = os.path.join(subdir, file)[position:]

						if not foundFile in listOfDependencies:
							missingDependencies.append(foundFileWithFullPath)

			return missingDependencies

	def getRidOfPlural(self, artifactType):
		# get rid of plural
		if artifactType[-1] == "s":
			artifactType = artifactType[:-1]

		return artifactType


EsbAddArtifactsCommand().run()