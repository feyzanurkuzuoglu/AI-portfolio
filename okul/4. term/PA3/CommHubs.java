import java.util.ArrayList;
import java.util.List;
import java.util.Stack;

public class CommHubs {

    public static List<List<Integer>> findHighInteractionZones(Digraph g, String[] labels) {
        Stack<Integer> stack = new Stack<>();
        boolean[] visited = new boolean[labels.length];

        for(int i=0; i<labels.length; i++)
            visited[i] = false;

        for(int v = 0; v<g.V(); v++)
            if(visited[v] == false)
                dfsFirst(v, g, visited, stack);

        Digraph g_rev = g.reverse();

        // reset visited
        visited = new boolean[g.V()];

        List<List<Integer>> scc = new ArrayList<>();

        while(!stack.empty()){
            int u = stack.pop();
            if (!visited[u]){
                List<Integer> current_scc = new ArrayList<>();
                dfsSecond(u, g_rev, visited, current_scc);
                scc.add(current_scc);
            }
        }
        return scc;
    }

    public static void dfsFirst(int u, Digraph g, boolean[] visited, Stack<Integer> stack){
        visited[u] = true;
        for(int v: g.adj(u)){
            if(visited[v] == false)
                dfsFirst(v, g, visited, stack);
        }
        stack.push(u);
    }

    public static void dfsSecond(int u, Digraph g_rev, boolean[] visited, List<Integer> current_scc){
        visited[u] = true;
        current_scc.add(u);

        for(int v: g_rev.adj(u)){
            if(visited[v] == false)
                dfsSecond(v, g_rev, visited, current_scc);
        }
    }
}
