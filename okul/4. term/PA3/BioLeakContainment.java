import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class BioLeakContainment {

    public static List<Integer> dfsReachable(Digraph g, int source, String[] labels) {
        List<Integer> reachable = new ArrayList<>();
        boolean[] visited = new boolean[g.V()];
        dfs(g, source, visited, reachable);
        return reachable;
    }

    private static void dfs(Digraph g, int v, boolean[] visited, List<Integer> reachable) {
        visited[v] = true;
        reachable.add(v);
        for (int w : g.adj(v)) {
            if (!visited[w]) {
                dfs(g, w, visited, reachable);
            }
        }
    }

    public static List<List<Integer>> bfsLayers(Digraph g, int source, String[] labels) {
        boolean[] visited = new boolean[g.V()];
        int[] distTo = new int[g.V()];
        Queue<Integer> q = new LinkedList<>();
        List<List<Integer>> layers = new ArrayList<>();

        visited[source] = true;
        distTo[source] = 0;
        q.add(source);

        while (!q.isEmpty()) {
            int v = q.poll();
            int d = distTo[v];


            while (layers.size() <= d) {
                layers.add(new ArrayList<>());
            }
            layers.get(d).add(v);

            for (int w : g.adj(v)) {
                if (!visited[w]) {
                    visited[w] = true;
                    distTo[w] = d + 1;
                    q.add(w);
                }
            }
        }
        return layers;
    }
}
