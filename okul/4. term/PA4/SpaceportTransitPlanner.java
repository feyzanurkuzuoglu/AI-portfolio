import java.util.*;

public class SpaceportTransitPlanner {

    Map<Station, Station> prev = new HashMap<>();
    Map<String, Double> cost = new HashMap<>();

    double dist(Station a, Station b) {
        double dx = a.p.x - b.p.x;
        double dy = a.p.y - b.p.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    void addUndirected(Station a, Station b, double speed) {
        // TODO: Add bidirectional walking edge
        double timeInMinutes = dist(a, b) / speed;
        a.edges.add(new Edge(b, timeInMinutes));
        b.edges.add(new Edge(a, timeInMinutes));
    }

    void addDirected(Station a, Station b, double speed) {
        // TODO: Add directed shuttle edge
        double timeInMinutes = dist(a, b) / speed;
        a.edges.add(new Edge(b, timeInMinutes));
    }

    public List<RouteInstruction> solve(SpaceportTransitNetwork net) {
        List<RouteInstruction> route = new ArrayList<>();

        // TODO:
        // 1. Build graph
        // 2. Add walking edges
        // 3. Add directed shuttle edges
        // 4. Run Dijkstra
        // 5. Reconstruct path

        // 1. Build graph
        List<Station> allStations = new ArrayList<>();
        allStations.add(net.start);
        allStations.add(net.end);
        for (ShuttleCorridor corridor : net.corridors) {
            allStations.addAll(corridor.stations);
        }

        // 2. Add walking edges
        for (Station s : allStations) {
            if (s.edges != null) s.edges.clear();
        }
        for (int i = 0; i < allStations.size(); i++) {
            for (int j = i + 1; j < allStations.size(); j++) {
                addUndirected(allStations.get(i), allStations.get(j), net.walkSpeed);
            }
        }

        // 3. Add directed shuttle edges
        double shuttleSpeedPerMin = net.shuttleSpeed;
        for (ShuttleCorridor corridor : net.corridors) {
            for (int i = 0; i < corridor.stations.size() - 1; i++) {
                addDirected(corridor.stations.get(i), corridor.stations.get(i + 1), shuttleSpeedPerMin);
            }
        }
        // 4. Run Dijkstra
        for (Station s : allStations) {
            cost.put(s.name, Double.MAX_VALUE);
        }
        cost.put(net.start.name, 0.0);


        PriorityQueue<Edge> pq = new PriorityQueue<>();
        pq.add(new Edge(net.start, 0.0));

        while (!pq.isEmpty()) {
            Edge current = pq.poll();
            Station u = current.to;

            if (current.w > cost.get(u.name)) continue;

            if (u == net.end) break;

            for (Edge edge : u.edges) {
                Station v = edge.to;
                double newCost = cost.get(u.name) + edge.w;

                if (newCost < cost.get(v.name)) {
                    cost.put(v.name, newCost);
                    prev.put(v, u);
                    pq.add(new Edge(v, newCost));
                }
            }
        }

        // 5. Reconstruct path
        List<Station> path = new ArrayList<>();
        Station curr = net.end;
        while (curr != null) {
            path.add(curr);
            curr = prev.get(curr);
        }
        Collections.reverse(path);

        for (int i = 0; i < path.size() - 1; i++) {
            Station a = path.get(i);
            Station b = path.get(i + 1);

            double timeTaken = cost.get(b.name) - cost.get(a.name);
            double expectedShuttleTime = dist(a, b) / shuttleSpeedPerMin;

            boolean isShuttle = Math.abs(timeTaken - expectedShuttleTime) < 1e-5;

            route.add(new RouteInstruction(a.name, b.name, timeTaken, isShuttle));
        }

        return route;
    }

    public void print(List<RouteInstruction> r) {
        // TODO: Print route exactly in required format
        double totalTime = 0;
        for (RouteInstruction inst : r) {
            totalTime += inst.t; // duration yerine t
        }

        System.out.println("Fastest route takes " + Math.round(totalTime) + " minute(s).");
        System.out.println("Route Instructions");
        System.out.println("------------------");

        for (int i = 0; i < r.size(); i++) {
            RouteInstruction inst = r.get(i);

            if (!inst.shuttle) { // type == "Walk" yerine boolean kontrolü
                System.out.printf(Locale.US, "%d. Walk from \"%s\" to \"%s\" for %.2f minutes.\n",
                        i + 1, inst.a, inst.b, inst.t);
            } else {
                System.out.printf(Locale.US, "%d. Take the shuttle from \"%s\" to \"%s\" for %.2f minutes.\n",
                        i + 1, inst.a, inst.b, inst.t);
            }
        }
    }
}