import os
import xml.etree.ElementTree as ET

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
		#print dependencies
		return dependencies

	def getListOfPropertiesFromDeploymentPom(self, deploymentPomPath):
		properties = {}
		tree = ET.parse(deploymentPomPath)
		allProperties = tree.findall("{http://maven.apache.org/POM/4.0.0}properties/*")
		for foundProperty in allProperties:
			tagNameStrippedNameSpace = foundProperty.tag[35:]
			delimiterPosition =  tagNameStrippedNameSpace.find("_._")
			properties[tagNameStrippedNameSpace[delimiterPosition+3:]] = tagNameStrippedNameSpace

		#print properties
		return properties

	def getProjectNameFromDeploymentPom(self, deploymentPomPath):
		tree = ET.parse(deploymentPomPath)
		parent = tree.findall("{http://maven.apache.org/POM/4.0.0}parent")
		for element in parent:
			projectName = element.find("{http://maven.apache.org/POM/4.0.0}groupId")
		return projectName.text

	def getProjectVersionFromDeploymentPom(self, deploymentPomPath):
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

						# -4 because of .xml
						if not foundFile[:-4] in listOfDependencies:
							#print foundFile[:-4], foundFileWithFullPath, listOfDependencies
							missingDependencies.append(foundFileWithFullPath)

			#print missingDependencies
			return missingDependencies

	def findMissingProperties(self, listOfProperties, artifactXmlFolder):
		ignoredFiles = ["synapse.xml"]
		foundFiles = []
		missingProperties = []

		# concat our synapse-config folder
		self.synapseConfigFolder = artifactXmlFolder + "src/main/synapse-config"

		for subdir, dirs, files in os.walk(self.synapseConfigFolder):
			for file in files:
				if not file in ignoredFiles:
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

					if listOfProperties.get(file[:-4]) == None:
						missingProperties.append(foundFileWithFullPath)

		return missingProperties

	def getRidOfPlural(self, artifactType):
		# get rid of plural
		if artifactType[-1] == "s":
			artifactType = artifactType[:-1]

		return artifactType