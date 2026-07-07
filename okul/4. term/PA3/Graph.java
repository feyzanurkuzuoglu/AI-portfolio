/**
 * Undirected weighted graph with a Bag-based adjacency list.
 *
 * Vertices are labelled 0 … V-1.
 * Each edge is stored TWICE (once per endpoint), which is correct for
 * an undirected graph.
 */
public class Graph {

    private final int V;          // number of vertices
    private int E;                // number of edges
    private final Bag<Edge>[] adj; // adj[v] = edges incident to v

    /**
     * Creates an empty graph with {@code V} vertices.
     *
     * @param V number of vertices (must be ≥ 0)
     */
    @SuppressWarnings("unchecked")
    public Graph(int V) {
        if (V < 0) throw new IllegalArgumentException("V must be non-negative");
        this.V  = V;
        this.E  = 0;
        adj = (Bag<Edge>[]) new Bag[V];
        for (int v = 0; v < V; v++) adj[v] = new Bag<>();
    }

    /** Returns the number of vertices. */
    public int V() { return V; }

    /** Returns the number of edges. */
    public int E() { return E; }

    /**
     * Adds undirected edge {@code e} to the graph.
     *
     * @param e the edge to add
     */
    public void addEdge(Edge e) {
        int v = e.either();
        int w = e.other(v);
        validateVertex(v);
        validateVertex(w);
        adj[v].add(e);
        adj[w].add(e);
        E++;
    }

    /**
     * Returns the edges incident to vertex {@code v}.
     *
     * @param v the vertex
     * @return edges incident to {@code v}
     */
    public Iterable<Edge> adj(int v) {
        validateVertex(v);
        return adj[v];
    }

    // ---------------------------------------------------------------
    private void validateVertex(int v) {
        if (v < 0 || v >= V)
            throw new IllegalArgumentException("Vertex " + v + " out of range [0," + V + ")");
    }
}
