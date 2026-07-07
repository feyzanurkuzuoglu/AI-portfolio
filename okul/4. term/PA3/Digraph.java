/**
 * Directed graph with a Bag-based adjacency list.
 *
 * Vertices are labelled 0 … V-1.
 * Each directed edge v → w is stored only in {@code adj[v]}.
 */
public class Digraph {

    private final int V;           // number of vertices
    private int E;                 // number of directed edges
    private final Bag<Integer>[] adj; // adj[v] = vertices reachable from v in one step

    /**
     * Creates an empty digraph with {@code V} vertices.
     *
     * @param V number of vertices (≥ 0)
     */
    @SuppressWarnings("unchecked")
    public Digraph(int V) {
        if (V < 0) throw new IllegalArgumentException("V must be non-negative");
        this.V = V;
        this.E = 0;
        adj = (Bag<Integer>[]) new Bag[V];
        for (int v = 0; v < V; v++) adj[v] = new Bag<>();
    }

    /** Returns the number of vertices. */
    public int V() { return V; }

    /** Returns the number of directed edges. */
    public int E() { return E; }

    /**
     * Adds directed edge v → w.
     *
     * @param v tail vertex
     * @param w head vertex
     */
    public void addEdge(int v, int w) {
        validateVertex(v);
        validateVertex(w);
        adj[v].add(w);
        E++;
    }

    /**
     * Returns the vertices reachable from {@code v} in one directed step.
     *
     * @param v tail vertex
     * @return iterable of head vertices
     */
    public Iterable<Integer> adj(int v) {
        validateVertex(v);
        return adj[v];
    }

    /**
     * Returns the reverse of this digraph (all edges flipped).
     * Used by Kosaraju–Sharir SCC algorithm.
     *
     * @return reversed digraph
     */
    public Digraph reverse() {
        Digraph rev = new Digraph(V);
        for (int v = 0; v < V; v++)
            for (int w : adj[v])
                rev.addEdge(w, v);
        return rev;
    }

    // ---------------------------------------------------------------
    private void validateVertex(int v) {
        if (v < 0 || v >= V)
            throw new IllegalArgumentException("Vertex " + v + " out of range [0," + V + ")");
    }
}
