import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import java.io.File;
import java.util.List;

/**
 * AetheriaCity – Main entry point.
 *
 * Parse AetheriaCity.xml, build the required graphs, and call your
 * implementations in sequence.
 *
 * Usage:
 * javac -encoding UTF-8 *.java -d .
 * java AetheriaCity AetheriaCity
 */
public class AetheriaCity {

    public static void main(String[] args) {
        try {
            if (args.length == 0) {
                System.err.println("Usage: java AetheriaCity <xml-file>");
                return;
            }
            Document doc = parseXML(args[0]);

            String[] labels = new String[100];
            Digraph dgf = null;


            // PART A: Power Grid
            NodeList districtsNodes = doc.getElementsByTagName("districts");
            if (districtsNodes != null && districtsNodes.getLength() > 0) {
                Element districts = (Element) districtsNodes.item(0);
                NodeList districtsList = districts.getElementsByTagName("district");
                Graph g = new Graph(districtsList.getLength());

                for (int i = 0; i < districtsList.getLength(); i++) {
                    Element element = (Element) districtsList.item(i);

                    String idStr = getText(element, "id").replace("D", "").trim();
                    if (idStr.isEmpty()) continue;
                    int idInt = Integer.parseInt(idStr);

                    labels[idInt] = getText(element, "name");

                    NodeList links = element.getElementsByTagName("link");
                    for (int j = 0; j < links.getLength(); j++) {
                        Element lElement = (Element) links.item(j);
                        String targetStr = getText(lElement, "target").replace("D", "").trim();
                        String costStr = getText(lElement, "cableCost").trim();

                        if (!targetStr.isEmpty() && !costStr.isEmpty()) {
                            g.addEdge(new Edge(idInt, Integer.parseInt(targetStr), Integer.parseInt(costStr)));
                        }
                    }
                }

                printBanner("PART A  |  Power Grid");
                boolean connected = PowerGrid.isConnected(g);
                System.out.println("City fully connected? " + (connected ? "YES\n" : "NO\n"));

                List<Edge> mst = PowerGrid.kruskalMST(g);
                System.out.println("Minimum Spanning Tree (" + mst.size() + " cables):");

                int totalCost = 0;
                for (Edge e : mst) {
                    int u = e.either();
                    int v = e.other(u);
                    System.out.printf("  %-22s - %-22s cost: %d\n", labels[u], labels[v], (int) e.weight());
                    totalCost += e.weight();
                }
                System.out.println("Total minimum cable cost: " + totalCost + " units");
            }


            // PART B: Master Boot Sequence
            NodeList bootNodes = doc.getElementsByTagName("bootDependencies");
            if (bootNodes != null && bootNodes.getLength() > 0) {
                Element bootDependencies = (Element) bootNodes.item(0);
                NodeList sList = bootDependencies.getElementsByTagName("s");
                Digraph dg = new Digraph(sList.getLength());

                for (int i = 0; i < sList.getLength(); i++) {
                    Element sElement = (Element) sList.item(i);
                    String idStr = getText(sElement, "id").replace("S", "").trim();
                    if (idStr.isEmpty()) continue;
                    int idInt = Integer.parseInt(idStr);

                    labels[idInt] = getText(sElement, "name");

                    NodeList requires = sElement.getElementsByTagName("req");
                    for (int j = 0; j < requires.getLength(); j++) {
                        String reqStr = requires.item(j).getTextContent().replace("S", "").trim();
                        if (!reqStr.isEmpty()) {
                            dg.addEdge(Integer.parseInt(reqStr), idInt);
                        }
                    }
                }

                printBanner("PART B  |  Master Boot Sequence (valid order)");
                List<Integer> top_order = BootSequence.computeBootSequence(dg, labels);

                System.out.println("=== Part B: Master Boot Sequence ===");
                if (top_order == null) {
                    System.out.println("  [Cycle detected] Edge creates a circular dependency..");
                    System.out.println("SYSTEM INFEASIBLE: Circular reference (deadlock) detected!");
                } else {
                    System.out.println("Valid boot sequence found:");
                    for (int i = 0; i < top_order.size(); i++) {
                        int id = top_order.get(i);
                        System.out.printf("  Step %2d: %s (id=%d)\n", (i + 1), labels[id], id);
                    }
                }
            }


            // PART C: Secure Communication Hubs
            NodeList fiberNodes = doc.getElementsByTagName("fiberLinks");
            if (fiberNodes != null && fiberNodes.getLength() > 0) {
                Element fiberLinks = (Element) fiberNodes.item(0);
                NodeList fiberLinksList = fiberLinks.getElementsByTagName("station");
                dgf = new Digraph(fiberLinksList.getLength());

                for (int i = 0; i < fiberLinksList.getLength(); i++) {
                    Element element = (Element) fiberLinksList.item(i);
                    String idStr = getText(element, "id").replace("F", "").trim();
                    if (idStr.isEmpty()) continue;
                    int idInt = Integer.parseInt(idStr);

                    labels[idInt] = getText(element, "name");

                    NodeList links = element.getElementsByTagName("link");
                    for (int j = 0; j < links.getLength(); j++) {
                        Element lElement = (Element) links.item(j);
                        String targetStr = getText(lElement, "target").replace("F", "").trim();
                        if (!targetStr.isEmpty()) {
                            dgf.addEdge(idInt, Integer.parseInt(targetStr));
                        }
                    }
                }

                printBanner("PART C  |  Secure Communication Hubs (SCCs)");
                List<List<Integer>> sccList = CommHubs.findHighInteractionZones(dgf, labels);
                System.out.println("=== Part C: Secure Communication Hubs ===");
                System.out.println("Total SCCs found: " + sccList.size());

                int zoneCount = 0;
                for (int i = 0; i < sccList.size(); i++) {
                    List<Integer> component = sccList.get(i);
                    boolean isHighInteraction = component.size() > 1;
                    if (isHighInteraction) zoneCount++;

                    System.out.print("  SCC-" + i + (isHighInteraction ? " [HIGH-INTERACTION ZONE]: {" : ": {"));

                    for (int j = 0; j < component.size(); j++) {
                        System.out.print(labels[component.get(j)] + (j == component.size() - 1 ? "" : ", "));
                    }
                    System.out.println("}");
                }
                System.out.println("High-Interaction Zones: " + zoneCount);
            }



            // PART D: Bio-Leak Containment Protocol
            NodeList leakNodes = doc.getElementsByTagName("leakScenarios");
            if (leakNodes != null && leakNodes.getLength() > 0 && dgf != null) {
                printBanner("PART D  |  Bio-Leak Containment Protocol");
                Element leakScenarios = (Element) leakNodes.item(0);
                NodeList scenarioList = leakScenarios.getElementsByTagName("scenario");

                for (int i = 0; i < scenarioList.getLength(); i++) {
                    Element scenarioEl = (Element) scenarioList.item(i);
                    String sourceIdStr = getText(scenarioEl, "sourceId").replace("F", "").trim();
                    if (sourceIdStr.isEmpty()) continue;
                    int sId = Integer.parseInt(sourceIdStr);

                    System.out.println("Leak origin: " + labels[sId] + " (id=" + sId + ")\n");

                    // task 1
                    List<Integer> reachable = BioLeakContainment.dfsReachable(dgf, sId, labels);
                    System.out.println("=== Part D, Task 1 " + labels[sId] + "(" + sId + ") ===");
                    System.out.println("Stations at risk (" + reachable.size() + "):");
                    for (int id : reachable) {
                        System.out.println("  " + labels[id] + "(" + id + ")");
                    }

                    //task  2
                    List<List<Integer>> layers = BioLeakContainment.bfsLayers(dgf, sId, labels);
                    System.out.println("\n=== Part D, Task 2 " + labels[sId] + "(" + sId + ") ===");
                    System.out.println("Evacuation priority layers:");

                    for (int d = 0; d < layers.size(); d++) {
                        String prefix = (d == 0) ? "  Layer 0 (source)    : " : "  Layer " + d + " (priority " + d + "): ";
                        System.out.print(prefix);

                        List<Integer> stations = layers.get(d);
                        for (int j = 0; j < stations.size(); j++) {
                            int id = stations.get(j);
                            System.out.print(labels[id] + "(" + id + ")" + (j == stations.size() - 1 ? "" : ", "));
                        }
                        System.out.println();
                    }
                }
            }

        } catch (Exception e) {

            e.printStackTrace();
        }
    }

    // ── XML helpers ──────────────────────────────────────────────────

    private static Document parseXML(String filename) throws Exception {
        File file = new File(filename + ".xml");
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(file);
        doc.getDocumentElement().normalize();
        return doc;
    }

    private static String getText(Element parent, String tag) {
        NodeList nl = parent.getElementsByTagName(tag);
        if (nl.getLength() == 0) return "";
        return nl.item(0).getTextContent().trim();
    }

    static void printBanner(String title) {
        String line = "═".repeat(60);
        System.out.println("\n" + line);
        System.out.println("  " + title);
        System.out.println(line);
    }
}