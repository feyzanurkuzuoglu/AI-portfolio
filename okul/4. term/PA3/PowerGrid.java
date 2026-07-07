import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class PowerGrid {

    public static boolean isConnected(Graph g) {

        boolean visited[] = new boolean[g.V()];
        int stack[] = new int[g.V()];
        int top = -1;
        int count = 0;

        top += 1;
        stack[top] = 0;
        visited[0] = true;
        count = 1;

        while(top >= 0){
            int current = stack[top];
            boolean found = false;

            for(Edge neighbor: g.adj(current)){
                int v = neighbor.other(current);
                if(!visited[v]){
                    top += 1;
                    stack[top] = v;
                    visited[v] = true;
                    count += 1;
                    found = true;
                    break;
                }
            }
            if(found == false) top -= 1;
        }
        return (count == g.V());
    }

    public static List<Edge> kruskalMST(Graph g) {
        List<Edge> mst = new ArrayList<>();

        Edge[] edges = new Edge[g.E()];
        int index = 0;
        for(int v = 0; v < g.V(); v++){
            for(Edge e: g.adj(v)){
                if(e.either() == v)
                    edges[index++] = e;
            }
        }
        Arrays.sort(edges);

        // union find
        int[] parent = new int[g.V()];
        int[] rank =  new int[g.V()];
        for(int i = 0; i < g.V(); i++){
            parent[i] = i;
            rank[i] = 0;
        }
        for(Edge e : edges){
            int u = e.either();
            int v = e.other(u);

            int rootU = u;
            while (parent[rootU] != rootU) {
                parent[rootU] = parent[parent[rootU]];
                rootU = parent[rootU];
            }

            int rootV = v;
            while (parent[rootV] != rootV) {
                parent[rootV] = parent[parent[rootV]];
                rootV = parent[rootV];
            }

            if (rootU != rootV) {
                mst.add(e);


                if (rank[rootU] < rank[rootV]) {
                    parent[rootU] = rootV;
                } else if (rank[rootU] > rank[rootV]) {
                    parent[rootV] = rootU;
                } else {
                    parent[rootU] = rootV;
                    rank[rootV]++;
                }
            }

            if (mst.size() == g.V() - 1) break;
        }
        return mst;
    }

}


