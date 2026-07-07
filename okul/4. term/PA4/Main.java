import java.util.*;

public class Main {
    public static void main(String[] args) {

        Locale.setDefault(Locale.US);

        // PART I
        System.out.println("=== LAUNCH OPERATIONS REPORT START ===");

        LaunchOperationsTimeline planner = new LaunchOperationsTimeline();
        List<LaunchPlan> plans = planner.readXML(args[0]);
        planner.printTimeline(plans);

        System.out.println("=== LAUNCH OPERATIONS REPORT END ===");
        System.out.println();

        // PART II
        System.out.println("=== TRANSIT PLAN START ===");

        SpaceportTransitNetwork network = new SpaceportTransitNetwork();
        network.readInput(args[1]);

        SpaceportTransitPlanner planner2 = new SpaceportTransitPlanner();
        List<RouteInstruction> route = planner2.solve(network);

        planner2.print(route);

        System.out.println("=== TRANSIT PLAN END ===");
    }
}