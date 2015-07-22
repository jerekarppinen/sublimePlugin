#import sublime, sublime_plugin
import xml.etree.ElementTree as ET
import os

class ParsePaths():
	def getDeploymentPom(self, pathsFile):
		pathsFile = os.path.dirname(os.path.abspath(__file__)) + "/" + pathsFile
		tree = ET.parse(pathsFile)
		for elem in tree.iterfind("deployment/deploymentPomPath"):
			return elem.text

	def getArtifactXml(self, pathsFile):
		pathsFile = os.path.dirname(os.path.abspath(__file__)) + "/" + pathsFile
		tree = ET.parse(pathsFile)
		for elem in tree.iterfind("artifactXmls/artifactXml"):
			return elem.text

class HelperUtil():
	def getListOfArtifacts(self, artifactXml):
		self.artifacts = []
		tree = ET.parse(artifactXml)
		for elem in tree.iterfind("artifact/file"):
			self.artifacts.append(elem.text.strip())
		return self.artifacts

	def findMissingArtifacts(self, listOfArtifacts, artifactXmlFolder):
		ignoredFiles = ["synapse.xml"]
		foundFiles = []
		missingArtifacts = []

		# concat our synapse-config folder
		self.synapseConfigFolder = artifactXmlFolder + listOfArtifacts[0][:23]
		print self.synapseConfigFolder

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
						print foundFile
						missingArtifacts.append(foundFile)

		return missingArtifacts

class EsbhelperCommand():
	def run(self):
		self.parsePaths = ParsePaths()
		self.deploymentPom = self.parsePaths.getDeploymentPom("paths.xml")
		self.artifactXml = self.parsePaths.getArtifactXml("paths.xml")

		# get the folder where artifact.xml resides
		# drop last 12 letters for 'artifact.xml'
		self.artifactXmlFolder = self.artifactXml[:-12]

		# get list of artifacts from artifacts.xml
		self.HelperUtil = HelperUtil()
		self.listOfArtifacts = self.HelperUtil.getListOfArtifacts(self.artifactXml)

		# figure out if there are some artifacts created but not added to artifacts.xml
		self.missingArtifacts = self.HelperUtil.findMissingArtifacts(self.listOfArtifacts, self.artifactXmlFolder)

		# if found any, add new artifacts to artifacts.xml
		if len(self.missingArtifacts) > 0:
			self.writeArtifacts(self.missingArtifacts, self.artifactXml)
			self.writeDeploymentPom(self.missingArtifacts, self.deploymentPom)

			#print "Following items were added: \n\r"
			#for item in self.missingArtifacts:
			#	print item


		else:
			print "No updates necessary."

	def writeDeploymentPom(self, missingArtifacts, deploymentPom):
		for missingArtifact in missingArtifacts:
			artifactParts = missingArtifact.split("/")

			artifactType = self.getRidOfPlural(artifactParts[3])

			artifactName = artifactParts[4]
			projectName = "korppikotka"
			version = "1.0.0"
			dependencyType = "xml"

			groupId = "fi.mystes.korppikotka."+artifactType

			self.addDeploymentPomChildren(groupId, artifactName, version, dependencyType, artifactType, projectName)

		
	def writeArtifacts(self, missingArtifacts, artifactXml):
		for missingArtifact in missingArtifacts:
			artifactParts = missingArtifact.split("/")

			artifactType = artifactParts[3]
			artifactName = artifactParts[4]
			projectName = "korppikotka"
			version = "1.0.0"

			#self.addChild('/home/jere/ESBProjects/Korppikotka/Integrations/Mediations/Common/artifact.xml', 'Endpoint', 'endpoint', 'korppikotka', '1.0.0')
			self.addArtifactXmlChild(artifactXml, artifactType, artifactName, projectName, version)


	def addDeploymentPomChildren(self, groupId, artifactName, version, dependencyType, artifactType, projectName):

			self.addDeploymentDependencies(groupId, artifactName, version, dependencyType, artifactType)
			self.addDeploymentProperties(groupId, artifactName, version, dependencyType, artifactType, projectName)

	def addDeploymentProperties(self, groupId, artifactName, version, dependencyType, artifactType, projectName):

		ET.register_namespace('', 'http://maven.apache.org/POM/4.0.0')

		tree = ET.parse(self.deploymentPom)
		root = tree.getroot()

		for child_or_root in root:
			if child_or_root.tag == "{http://maven.apache.org/POM/4.0.0}properties":
				propertiesElement = child_or_root

		propertyElement = ET.Element("fi.mystes." + projectName + "." + artifactType + "_._" + artifactName)
		propertyElement.text = "capp/EnterpriseServiceBus"

		propertiesElement.append(propertyElement)

		tree.write(self.deploymentPom)

		

	def addDeploymentDependencies(self, groupId, artifactName, version, dependencyType, artifactType):

		ET.register_namespace('', 'http://maven.apache.org/POM/4.0.0')

		tree = ET.parse(self.deploymentPom)
		root = tree.getroot()

		dependenciesElement = root.find("{http://maven.apache.org/POM/4.0.0}dependencies")
		
		dependencyElement = ET.Element("dependency")

		groupIdElement = ET.Element("groupId")
		groupIdElement.text = "fi.mystes.korppikotka." + artifactType

		artifactIdElement = ET.Element("artifactId")
		artifactIdElement.text = artifactName

		versionElement = ET.Element("version")
		versionElement.text = version

		versionElement = ET.Element("type")
		versionElement.text = dependencyType


		dependencyElement.append(groupIdElement)
		dependencyElement.append(artifactIdElement)
		dependencyElement.append(versionElement)

		dependenciesElement.append(dependencyElement)

		tree.write(self.deploymentPom)


	def addArtifactXmlChild(self, artifactXml, artifactType, artifactName, projectName, version):

		artifactTypeWithPossiblePlural = artifactType

		artifactType = self.getRidOfPlural(artifactType)

		groupId = "fi.mystes." + projectName + "." + artifactType
		artifactType = "synapse/" + artifactType
		
		tree = ET.parse(artifactXml)
		root = tree.getroot()
		artifactElement = ET.Element("artifact", groupId=groupId, name=artifactName, serverRole="EnterpriseServiceBus", type=artifactType, version=version)

		fileElement = ET.Element("file")
		fileElement.text = "src/main/synapse-config/" + artifactTypeWithPossiblePlural + "/" + artifactName

		root.append(artifactElement)
		artifactElement.append(fileElement)
		tree.write(artifactXml)

	def getRidOfPlural(self, artifactType):
		# get rid of plural
		if artifactType[-1] == "s":
			artifactType = artifactType[:-1]

		return artifactType

EsbhelperCommand().run()