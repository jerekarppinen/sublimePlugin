import os
import unittest
from lxml import etree

import ParsePaths

class PathsXmlFileContainsCorrectFilePaths(unittest.TestCase):

	def test_givenPathsXmlFileExists(self):
		self.assertTrue(os.path.isfile("paths.xml"))

	def test_thenDeploymentPomPathContainsPomXml(self):
		tree = etree.parse("paths.xml")
		element = tree.xpath("//paths/deployment/deploymentPomPath/text()")
		self.assertEquals(element[0][-7:], "pom.xml")

	def test_andArtifactXmlContainsArtifactXml(self):
		tree = etree.parse("paths.xml")
		element = tree.xpath("//paths/artifactXmls/artifactXml/text()")
		self.assertEquals(element[0][-12:], "artifact.xml")

if __name__ == '__main__':
    unittest.main()