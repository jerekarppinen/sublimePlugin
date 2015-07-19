#import sublime, sublime_plugin
import xml.etree.ElementTree as ET
import os
from __builtin__ import any as b_any

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
			#self.artifacts.append(elem.text.split("/"))
			self.artifacts.append(elem.text)
		return self.artifacts

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

	def writeDeploymentPom(self, missingArtifacts, deploymentPom):
		pass
		
	def writeArtifacts(self, missingArtifacts, artifactXml):
		for missingArtifact in missingArtifacts:
			artifactParts = missingArtifact.split("/")

			artifactType = artifactParts[3]
			artifactName = artifactParts[4]
			projectName = "korppikotka"
			version = "1.0.0"

			#self.addChild('/home/jere/ESBProjects/Korppikotka/Integrations/Mediations/Common/artifact.xml', 'Endpoint', 'endpoint', 'korppikotka', '1.0.0')
			self.addChild(artifactXml, artifactType, artifactName, projectName, version)


	def addChild(self, artifactXml, artifactType, artifactName, projectName, version):

		artifactTypeWithPossiblePlural = artifactType

		# get rid of plural
		if artifactType[-1] == "s":
			artifactType = artifactType[:-1]

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

EsbhelperCommand().run()