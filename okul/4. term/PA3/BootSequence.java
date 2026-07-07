import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class BootSequence {


    public static List<Integer> computeBootSequence(Digraph g, String[] labels) {
        int[] state = new int[labels.length];
        List<Integer> top_order = new ArrayList<>();

        for(int v = 0; v < g.V(); v++){
            if (state[v] == 0)
                if (dfs(g, v, state, top_order) == false)
                    return null;
        }

        Collections.reverse(top_order);
        return top_order;
    }

    public static boolean dfs(Digraph g, int u, int[] state, List<Integer> top_order){
        state[u] = 1;

        for (int v : g.adj(u)) {
            if (state[v] == 1) return false;
            if (state[v] == 0)
                if (dfs(g, v, state, top_order) == false) return  false;
        }

        state[u] = 2;
        top_order.add(u);
        return true;
    }
}


