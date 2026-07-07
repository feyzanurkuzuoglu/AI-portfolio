import org.w3c.dom.*;
import javax.xml.parsers.*;
import java.io.File;
import java.util.*;

public class LaunchOperationsTimeline {

    public List<LaunchPlan> readXML(String file) {
        List<LaunchPlan> list = new ArrayList<>();
        // TODO: Parse XML and populate launch plans

        try {
            File inputFile = new File(file);
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(inputFile);

            doc.getDocumentElement().normalize();

            NodeList planList = doc.getElementsByTagName("LaunchPlan");

            for (int i = 0; i < planList.getLength(); i++) {
                Node planNode = planList.item(i);

                if (planNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element planElement = (Element) planNode;

                    String planName = planElement.getElementsByTagName("PlanName").item(0).getTextContent().trim();

                    List<Operation> operationsList = new ArrayList<>();

                    NodeList opList = planElement.getElementsByTagName("Operation");

                    for (int j = 0; j < opList.getLength(); j++) {
                        Node opNode = opList.item(j);

                        if (opNode.getNodeType() == Node.ELEMENT_NODE) {
                            Element opElement = (Element) opNode;

                            int code = Integer.parseInt(opElement.getElementsByTagName("Code").item(0).getTextContent().trim());
                            String label = opElement.getElementsByTagName("Label").item(0).getTextContent().trim();
                            int execTime = Integer.parseInt(opElement.getElementsByTagName("ExecutionTime").item(0).getTextContent().trim());

                            List<Integer> prereqList = new ArrayList<>();
                            NodeList blockedByList = opElement.getElementsByTagName("RequiresOperation");

                            for (int k = 0; k < blockedByList.getLength(); k++) {
                                int reqCode = Integer.parseInt(blockedByList.item(k).getTextContent().trim());
                                prereqList.add(reqCode);
                            }

                            Operation operation = new Operation(code, label, execTime, prereqList);
                            operationsList.add(operation);
                        }
                    }

                    LaunchPlan launchPlan = new LaunchPlan(planName, operationsList);

                    list.add(launchPlan);
                }
            }
        } catch (Exception e) {
            System.err.println("XML Parsing Hatası (XML Parsing Error): " + e.getMessage());
            e.printStackTrace();
        }

        return list;
    }

    public void printTimeline(List<LaunchPlan> plans) {
        // TODO: Iterate and print each plan
        for (LaunchPlan plan : plans) {
            plan.print();
        }

    }

}