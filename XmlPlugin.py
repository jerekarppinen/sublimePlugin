import sublime, sublime_plugin
import re
from WriteXmlFiles import WriteXmlFiles
from ParsePaths import ParsePaths
from HelperUtil import HelperUtil

class EsbAddArtifactsCommand(sublime_plugin.TextCommand):
		def run(self):

			self.config = "paths.xml"

			self.deploymentPomPath = ParsePaths().getDeploymentPomPath("paths.xml")
			self.artifactXmlPath = ParsePaths().getArtifactXmlPath("paths.xml")

			# get the folder where artifact.xml resides
			# drop last 12 letters for 'artifact.xml'
			self.artifactXmlFolder = self.artifactXmlPath[:-12]

			self.projectName = HelperUtil().getProjectNameFromDeploymentPom(self.deploymentPomPath)

			self.version = HelperUtil().getVersionFromDeploymentPom(self.deploymentPomPath)

			# get list of artifacts from artifacts.xml
			self.listOfArtifacts = HelperUtil().getListOfArtifactsFromArtifactsXml(self.artifactXmlPath)

			# get list of dependencies from pom.xml
			self.listOfDependencies = HelperUtil().getListOfDependenciesFromDeploymentPom(self.deploymentPomPath)

			# get list of properties from pom.xml
			self.listOfProperties = HelperUtil().getListOfPropertiesFromDeploymentPom(self.deploymentPomPath)

			# figure out if there are some artifacts created but not added to artifacts.xml
			self.missingArtifacts = HelperUtil().findMissingArtifacts(self.listOfArtifacts, self.artifactXmlFolder)

			# figure out if there are some artifacts created but not added to pom.xml
			self.missingDependencies = HelperUtil().findMissingDependencies(self.listOfDependencies, self.artifactXmlFolder)

			# and finally the same for properties
			self.missingProperties = HelperUtil().findMissingProperties(self.listOfProperties, self.artifactXmlFolder)

			# if found any, add new artifacts to artifacts.xml
			print "New artifacts:", len(self.missingArtifacts), self.missingArtifacts
			if len(self.missingArtifacts) > 0:
				WriteXmlFiles().writeArtifacts(self.missingArtifacts, self.artifactXmlPath, self.version)

			#and new dependencies to pom.xml
			print "New dependencies:", len(self.missingDependencies), self.missingDependencies
			if len(self.missingDependencies) > 0:
				WriteXmlFiles().writeDependencies(self.missingDependencies, self.deploymentPomPath, self.projectName, self.version)

			#and new properties to pom.xml
			print "New properties:", len(self.missingProperties), self.missingProperties
			if len(self.missingProperties) > 0:
				WriteXmlFiles().writeProperties(self.missingProperties, self.deploymentPomPath, self.projectName, self.version)

			self.message = self.missingArtifacts + self.missingDependencies + self.missingProperties

			sublime.message_dialog("Added components: " + self.message)


EsbAddArtifactsCommand().run()