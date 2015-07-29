# import lxml.etree
# import lxml.builder

# projectXml = """
# <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
#    <parent>
#       <artifactId>Project-Integrations</artifactId>
#       <groupId>fi.company.project</groupId>
#       <version>1.0.0</version>
#    </parent>
#    <dependencies>
#       <dependency>
#          <groupId>fi.company.project.sequence</groupId>
#          <artifactId>MySequence</artifactId>
#          <type>xml</type>
#          <version>1.0.0</version>
#       </dependency>
#       <dependency>
#          <groupId>fi.company.project.endpoint</groupId>
#          <artifactId>MyEndpoint</artifactId>
#          <type>xml</type>
#          <version>1.0.0</version>
#       </dependency>
#       <dependency>
#          <groupId>fi.company.project.api</groupId>
#          <artifactId>MyApi</artifactId>
#          <type>xml</type>
#          <version>1.0.0</version>
#       </dependency>
#       <dependency>
#          <groupId>fi.company.project.proxy-service</groupId>
#          <artifactId>MyProxy</artifactId>
#          <type>xml</type>
#          <version>1.0.0</version>
#       </dependency>
#       <dependency>
#          <groupId>fi.company.project.task</groupId>
#          <artifactId>MyTask</artifactId>
#          <type>xml</type>
#          <version>1.0.0</version>
#       </dependency>
# </dependencies>
#    <properties>
#       <fi.company.project.sequence_._MySequence>capp/EnterpriseServiceBus</fi.company.project.sequence_._MySequence>
#       <fi.company.project.endpoint_._MyEndpoint>capp/EnterpriseServiceBus</fi.company.project.endpoint_._MyEndpoint>
#       <fi.company.project.api_._MyApi>capp/EnterpriseServiceBus</fi.company.project.api_._MyApi>
#       <fi.company.project.proxy-service_._MyProxy>capp/EnterpriseServiceBus</fi.company.project.proxy-service_._MyProxy>
#       <fi.company.project.task._MyTask>capp/EnterpriseServiceBus</fi.company.project.task._MyTask>
#     </properties>
# </project>
# """

# xml =  lxml.etree.fromstring(projectXml)



# with open("pom.xml", "w") as f:
# 	f.write(lxml.etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8"))




# #print lxml.etree.tostring(xml, pretty_print=True)
# import os
# if not os.path.exists("testfolders/deployment"):
#     os.makedirs("testfolders/deployment")