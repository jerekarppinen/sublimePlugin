import sys
import os
import shutil
import unittest

from lxml import etree
import lxml.etree
import lxml.builder

from WriteXmlFiles import WriteXmlFiles
from ParsePaths import ParsePaths
from HelperUtil import HelperUtil
from ImportTools import ImportTools

if not os.path.exists("xmlunittest-0.3.1"):
	ImportTools().getXmlUnitTest()

sys.path.append("xmlunittest-0.3.1")
from xmlunittest import XmlTestCase

deploymentPomPath = "testfolders2/deployment/pom.xml"
arfifactXmlPath = "testfolders2/artifact.xml"
artifactXmlFolder = "testfolders2/"

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

	def createFullDeploymentPomFile(self):

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

	def createNotFullDeploymentPomFile(self):

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
		</dependencies>
		   <properties>
		      <fi.company.project.sequence_._MySequence>capp/EnterpriseServiceBus</fi.company.project.sequence_._MySequence>
		      <fi.company.project.endpoint_._MyEndpoint>capp/EnterpriseServiceBus</fi.company.project.endpoint_._MyEndpoint>
		      <fi.company.project.api_._MyApi>capp/EnterpriseServiceBus</fi.company.project.api_._MyApi>
		    </properties>
	</project>
		"""

		xml =  lxml.etree.fromstring(projectXml)

		with open(deploymentPomPath, "w") as f:
			f.write(lxml.etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8"))			

	def createFullArtifactXmlFile(self):

		projectXml = """
		<artifacts>
	    <artifact groupId="fi.mystes.project.sequence" name="MySequence" serverRole="EnterpriseServiceBus" type="synapse/sequence" version="1.0.0">
	        <file>src/main/synapse-config/sequences/MySequence.xml</file>
	    </artifact>
	    <artifact groupId="fi.mystes.project.endpoint" name="MyEndpoint" serverRole="EnterpriseServiceBus" type="synapse/endpoint" version="1.0.0">
	        <file>src/main/synapse-config/endpoints/MyEndpoint.xml</file>
	    </artifact>
	    <artifact groupId="fi.mystes.project.api" name="MyApi" serverRole="EnterpriseServiceBus" type="synapse/api" version="1.0.0">
	        <file>src/main/synapse-config/api/MyApi.xml</file>
	    </artifact>
	    <artifact groupId="fi.mystes.project.proxy-service" name="MyProxy" serverRole="EnterpriseServiceBus" type="synapse/proxy-service" version="1.0.0">
	        <file>src/main/synapse-config/proxy-services/MyProxy.xml</file>
	    </artifact>
	    <artifact groupId="fi.mystes.project.task" name="MyTask" serverRole="EnterpriseServiceBus" type="synapse/task" version="1.0.0">
	        <file>src/main/synapse-config/tasks/MyTask.xml</file>
	    </artifact>
		</artifacts>
		"""

		xml =  lxml.etree.fromstring(projectXml)

		with open(arfifactXmlPath, "w") as f:
			f.write(lxml.etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8"))

	def createNotFullArtifactXmlFile(self):

		projectXml = """
		<artifacts>
	    <artifact groupId="fi.mystes.project.sequence" name="MySequence" serverRole="EnterpriseServiceBus" type="synapse/sequence" version="1.0.0">
	        <file>src/main/synapse-config/sequences/MySequence.xml</file>
	    </artifact>
	    <artifact groupId="fi.mystes.project.endpoint" name="MyEndpoint" serverRole="EnterpriseServiceBus" type="synapse/endpoint" version="1.0.0">
	        <file>src/main/synapse-config/endpoints/MyEndpoint.xml</file>
	    </artifact>
	    <artifact groupId="fi.mystes.project.api" name="MyApi" serverRole="EnterpriseServiceBus" type="synapse/api" version="1.0.0">
	        <file>src/main/synapse-config/api/MyApi.xml</file>
	    </artifact>
		</artifacts>
		"""

		xml =  lxml.etree.fromstring(projectXml)

		with open(arfifactXmlPath, "w") as f:
			f.write(lxml.etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8"))			

	def deleteFoldersAndFiles(self):
		shutil.rmtree('testfolders2')


class Happy_PathsXmlFileContainsCorrectFilePaths(unittest.TestCase):

	def test_PathsXmlFileExists(self):
		self.assertTrue(os.path.isfile("paths.xml"))

	def test_DeploymentPomPathContainsPomXml(self):
		tree = etree.parse("paths.xml")
		element = tree.xpath("//paths/deployment/deploymentPomPath/text()")
		self.assertEquals(element[0][-7:], "pom.xml")

	def test_ArtifactXmlContainsArtifactXml(self):
		tree = etree.parse("paths.xml")
		element = tree.xpath("//paths/artifactXmls/artifactXml/text()")
		self.assertEquals(element[0][-12:], "artifact.xml")

class Happy_DeploymentPomIsRead(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		Background().createFoldersAndFiles()
		Background().createFullDeploymentPomFile()

	@classmethod
	def tearDownClass(cls):
		Background().deleteFoldersAndFiles()

	

	def test_projectNameIsReadFromTheFile(self):
		self.assertEquals(HelperUtil().getProjectNameFromDeploymentPom(deploymentPomPath), "fi.company.project")

	def test_projectVersionIsReadFromTheFile(self):
		self.assertEquals(HelperUtil().getProjectVersionFromDeploymentPom(deploymentPomPath), "1.0.0")

	def test_listOfDependenciesAreReadFromTheFile(self):
		self.assertEquals(HelperUtil().getListOfDependenciesFromDeploymentPom(deploymentPomPath), ["MySequence", "MyEndpoint", "MyApi", "MyProxy", "MyTask"])

	def test_listOfPropertiesAreReadFromTheFile(self):
		self.assertEquals(HelperUtil().getListOfPropertiesFromDeploymentPom(deploymentPomPath), {'MyApi': 'fi.company.project.api_._MyApi', 'MySequence': 'fi.company.project.sequence_._MySequence', 'MyProxy': 'fi.company.project.proxy-service_._MyProxy', '.company.project.task._MyTask': 'fi.company.project.task._MyTask', 'MyEndpoint': 'fi.company.project.endpoint_._MyEndpoint'})

	def test_noMissingDependenciesAreFoundUnderSynapseConfigFolder(self):
		self.assertEquals(HelperUtil().findMissingDependencies(["MySequence", "MyEndpoint", "MyApi", "MyProxy", "MyTask"], artifactXmlFolder), [])

class Happy_ArtifactXmlIsRead(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		Background().createFoldersAndFiles()
		Background().createFullArtifactXmlFile()

	@classmethod
	def tearDownClass(cls):
		Background().deleteFoldersAndFiles()

	def test_artifactXmlFileContainsFiveComponents(self):
		self.assertEquals(HelperUtil().getListOfArtifactsFromArtifactsXml(arfifactXmlPath), ['src/main/synapse-config/sequences/MySequence.xml', 'src/main/synapse-config/endpoints/MyEndpoint.xml', 'src/main/synapse-config/api/MyApi.xml', 'src/main/synapse-config/proxy-services/MyProxy.xml', 'src/main/synapse-config/tasks/MyTask.xml'])

class Happy_TwoComponentsAreMissingUnderSynapseConfigAndThenAddedToDeploymentPomAndArtifactXml(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		Background().createFoldersAndFiles()
		Background().createNotFullArtifactXmlFile()
		Background().createNotFullDeploymentPomFile()

	@classmethod
	def tearDownClass(cls):
		pass
		#Background().deleteFoldersAndFiles()

	def test_twoMissingComponentsAreFoundRelatedToArtifactsXml(self):
		self.assertEquals(HelperUtil().findMissingArtifacts(['src/main/synapse-config/sequences/MySequence.xml', 'src/main/synapse-config/endpoints/MyEndpoint.xml', 'src/main/synapse-config/api/MyApi.xml'], artifactXmlFolder), ['src/main/synapse-config/proxy-services/MyProxy.xml', 'src/main/synapse-config/tasks/MyTask.xml'])

	def test_twoMissingDependenciesAreFoundRelatedToDeploymentPom(self):
		self.assertEquals(HelperUtil().findMissingDependencies(["MySequence", "MyEndpoint", "MyApi"], artifactXmlFolder), ['src/main/synapse-config/proxy-services/MyProxy.xml', 'src/main/synapse-config/tasks/MyTask.xml'])

	def test_twoMissingPropertiesAreFoundRelatedToDeploymentPom(self):
		self.assertEquals(HelperUtil().findMissingProperties({'MySequence': 'fi.company.project.sequence_._MySequence', 'MyEndpoint': 'fi.company.project.endpoint_._MyEndpoint', 'MyApi': 'fi.company.project.api_._MyApi'}, artifactXmlFolder), ['src/main/synapse-config/proxy-services/MyProxy.xml', 'src/main/synapse-config/tasks/MyTask.xml'])

	def test_twoMissingComponentsAreWrittenToArtifactXml(self):
		self.assertEquals(WriteXmlFiles().writeArtifacts(['src/main/synapse-config/proxy-services/MyProxy.xml', 'src/main/synapse-config/tasks/MyTask.xml'], arfifactXmlPath, "1.0.0"), None)

	def test_assertArtifactXml(self):
		root = ET.parse(arfifactXmlPath)
		self.assertEquals(root, True)
 
if __name__ == '__main__':
		unittest.main()
 