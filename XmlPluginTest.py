import os
import shutil
import unittest
from lxml import etree
import lxml.etree
import lxml.builder
from WriteXmlFiles import WriteXmlFiles
from ParsePaths import ParsePaths
from HelperUtil import HelperUtil

import ParsePaths

deploymentPomPath = "testfolders2/deployment/pom.xml"
artifactXmlFolder = "testfolders2"

class Background():

	def createFoldersAndFiles(self):

		if not os.path.exists("testfolders2/deployment"):
			os.makedirs("testfolders2/deployment")

		if not os.path.exists("testfolders2/src/main/synapse-config/api"):
			os.makedirs("testfolders2/src/main/synapse-config/api")

		if not os.path.exists("testfolders2/src/main/synapse-config/endpoints"):
			os.makedirs("testfolders2/src/main/synapse-config/endpoints")

		if not os.path.exists("testfolders2/src/main/synapse-config/proxy-services"):
			os.makedirs("testfolders2/src/main/synapse-config/proxy-services")

		if not os.path.exists("testfolders2/src/main/synapse-config/sequences"):
			os.makedirs("testfolders2/src/main/synapse-config/sequences")

		if not os.path.exists("testfolders2/src/main/synapse-config/tasks"):
			os.makedirs("testfolders2/src/main/synapse-config/tasks")

		open("testfolders2/src/main/synapse-config/api/MyApi.xml", 'a').close()
		open("testfolders2/src/main/synapse-config/endpoints/MyEndpoint.xml", 'a').close()
		open("testfolders2/src/main/synapse-config/proxy-services/MyProxy.xml", 'a').close()
		open("testfolders2/src/main/synapse-config/sequences/MySequence.xml", 'a').close()
		open("testfolders2/src/main/synapse-config/tasks/MyTask.xml", 'a').close()

	def createFullPomFile(self):

		projectXml = """
		<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
		   <parent>
		      <artifactId>Project-Integrations</artifactId>
		      <groupId>fi.company.project</groupId>
		      <version>1.0.0</version>
		   </parent>
		   <dependencies>
		      <dependency>
		         <groupId>fi.company.project.sequence</groupId>
		         <artifactId>MySequence</artifactId>
		         <type>xml</type>
		         <version>1.0.0</version>
		      </dependency>
		      <dependency>
		         <groupId>fi.company.project.endpoint</groupId>
		         <artifactId>MyEndpoint</artifactId>
		         <type>xml</type>
		         <version>1.0.0</version>
		      </dependency>
		      <dependency>
		         <groupId>fi.company.project.api</groupId>
		         <artifactId>MyApi</artifactId>
		         <type>xml</type>
		         <version>1.0.0</version>
		      </dependency>
		      <dependency>
		         <groupId>fi.company.project.proxy-service</groupId>
		         <artifactId>MyProxy</artifactId>
		         <type>xml</type>
		         <version>1.0.0</version>
		      </dependency>
		      <dependency>
		         <groupId>fi.company.project.task</groupId>
		         <artifactId>MyTask</artifactId>
		         <type>xml</type>
		         <version>1.0.0</version>
		      </dependency>
		</dependencies>
		   <properties>
		      <fi.company.project.sequence_._MySequence>capp/EnterpriseServiceBus</fi.company.project.sequence_._MySequence>
		      <fi.company.project.endpoint_._MyEndpoint>capp/EnterpriseServiceBus</fi.company.project.endpoint_._MyEndpoint>
		      <fi.company.project.api_._MyApi>capp/EnterpriseServiceBus</fi.company.project.api_._MyApi>
		      <fi.company.project.proxy-service_._MyProxy>capp/EnterpriseServiceBus</fi.company.project.proxy-service_._MyProxy>
		      <fi.company.project.task._MyTask>capp/EnterpriseServiceBus</fi.company.project.task._MyTask>
		    </properties>
	</project>
		"""

		xml =  lxml.etree.fromstring(projectXml)

		with open(deploymentPomPath, "w") as f:
			f.write(lxml.etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8"))

	def deleteFoldersAndFiles(self):
		shutil.rmtree('testfolders2')


class Happy_PathsXmlFileContainsCorrectFilePaths(unittest.TestCase):

	def test_given_PathsXmlFileExists(self):
		self.assertTrue(os.path.isfile("paths.xml"))

	def test_then_DeploymentPomPathContainsPomXml(self):
		tree = etree.parse("paths.xml")
		element = tree.xpath("//paths/deployment/deploymentPomPath/text()")
		self.assertEquals(element[0][-7:], "pom.xml")

	def test_and_ArtifactXmlContainsArtifactXml(self):
		tree = etree.parse("paths.xml")
		element = tree.xpath("//paths/artifactXmls/artifactXml/text()")
		self.assertEquals(element[0][-12:], "artifact.xml")

class Happy_DeploymentPomIsRead(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		Background().createFoldersAndFiles()
		Background().createFullPomFile()

	@classmethod
	def tearDownClass(cls):
		Background().deleteFoldersAndFiles()

	

	def test_then_projectNameIsReadFromTheFile(self):
		self.assertEquals(HelperUtil().getProjectNameFromDeploymentPom(deploymentPomPath), "fi.company.project")

	def test_and_projectVersionIsReadFromTheFile(self):
		self.assertEquals(HelperUtil().getProjectVersionFromDeploymentPom(deploymentPomPath), "1.0.0")

	def test_and_listOfDependenciesAreReadFromTheFile(self):
		self.assertEqual(HelperUtil().getListOfDependenciesFromDeploymentPom(deploymentPomPath), ["MySequence", "MyEndpoint", "MyApi", "MyProxy", "MyTask"])

	def test_and_listOfPropertiesAreReadFromTheFile(self):
		self.assertEqual(HelperUtil().getListOfPropertiesFromDeploymentPom(deploymentPomPath), {'MyApi': 'fi.company.project.api_._MyApi', 'MySequence': 'fi.company.project.sequence_._MySequence', 'MyProxy': 'fi.company.project.proxy-service_._MyProxy', '.company.project.task._MyTask': 'fi.company.project.task._MyTask', 'MyEndpoint': 'fi.company.project.endpoint_._MyEndpoint'})

	def test_and_noMissingDependenciesAreFoundUnderSynapseConfigFolder(self):
		self.assertEqual(HelperUtil().findMissingDependencies(["MySequence", "MyEndpoint", "MyApi", "MyProxy", "MyTask"], artifactXmlFolder), [])


if __name__ == '__main__':
		unittest.main()
 