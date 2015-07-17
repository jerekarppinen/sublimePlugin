import xml.etree.ElementTree as ET


def addChild(artifactPath, artifactType, artifactName, projectName, version):

	groupId = "fi.mystes." + str(projectName) + ".endpoint"
	artifactType = "synapse/" + str(artifactType)


	# parse whole artifact path
	tree = ET.parse(artifactPath)
	# get root element
	root = tree.getroot()
	# create a new artifact
	artifactElement = ET.Element("artifact", groupId=groupId, name=artifactName, serverRole="EnterpriseServiceBus", type=artifactType, version=version)

	fileElement = ET.Element("file")
	fileElement.text = "src/main/synapse-config/endpoints/" + artifactName +".xml"

	root.append(artifactElement)
	artifactElement.append(fileElement)
	tree.write('/home/jere/ESBProjects/Korppikotka/Integrations/Mediations/Common/artifact.xml')

addChild('/home/jere/ESBProjects/Korppikotka/Integrations/Mediations/Common/artifact.xml', 'Endpoint', 'endpoint', 'korppikotka', '1.0.0')