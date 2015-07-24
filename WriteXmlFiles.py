import xml.etree.ElementTree as ET

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
			artifactElement = ET.Element("artifact", groupId=groupId, name=artifactName[:-4], serverRole="EnterpriseServiceBus", type=artifactType, version=version)

			fileElement = ET.Element("file")
			fileElement.text = "src/main/synapse-config/" + artifactTypeWithPossiblePlural + "/" + artifactName

			root.append(artifactElement)
			artifactElement.append(fileElement)

		tree.write(artifactXmlPath)

	def writeDependencies(self, missingDependencies, deploymentPomPath, projectName, version):

		ET.register_namespace('', 'http://maven.apache.org/POM/4.0.0')

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

	def writeProperties(self, missingProperties, deploymentPomPath, projectName, version):

		ET.register_namespace('', 'http://maven.apache.org/POM/4.0.0')

		tree = ET.parse(deploymentPomPath)
		root = tree.getroot()

		for missingProperty in missingProperties:

			# a little hack to extract artifact type from the file path
			result = re.search('src/main/synapse-config/(.*)/', missingProperty)
			artifactType = result.group(1)
			artifactTypeWithPossiblePlural = artifactType
			artifactType = HelperUtil().getRidOfPlural(artifactType)

			groupId = projectName + "." + artifactType + "_._"

			positionOfLastForwardSlash = missingProperty.rfind("/")
			positionOfLastPoint = missingProperty.rfind(".")

			artifactName = missingProperty[positionOfLastForwardSlash+1:positionOfLastPoint]

			propertyElement = ET.Element(groupId+artifactName)

			propertyElement.text = "capp/EnterpriseServiceBus"

			propertiesElement = root.find("{http://maven.apache.org/POM/4.0.0}properties")

			propertiesElement.append(propertyElement)

		tree.write(deploymentPomPath)