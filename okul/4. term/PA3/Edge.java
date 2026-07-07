/**
 * A weighted, undirected edge for use with {@link Graph}.
 *
 * The two endpoints are stored; {@link #either()} returns one and
 * {@link #other(int)} returns the other.
 */
public class Edge implements Comparable<Edge> {

    private final int    v;
    private final int    w;
    private final double weight;

    /**
     * Creates an edge between {@code v} and {@code w} with the given weight.
     *
     * @param v      one endpoint (≥ 0)
     * @param w      other endpoint (≥ 0)
     * @param weight edge weight
     */
    public Edge(int v, int w, double weight) {
        if (v < 0 || w < 0) throw new IllegalArgumentException("Vertex index must be non-negative");
        this.v      = v;
        this.w      = w;
        this.weight = weight;
    }

    /** Returns the weight of this edge. */
    public double weight() { return weight; }

    /**
     * Returns one of the two endpoints (arbitrarily {@code v}).
     *
     * @return one endpoint
     */
    public int either() { return v; }

    /**
     * Returns the endpoint of this edge that is not {@code vertex}.
     *
     * @param vertex one endpoint
     * @return the other endpoint
     * @throws IllegalArgumentException if {@code vertex} is not an endpoint
     */
    public int other(int vertex) {
        if      (vertex == v) return w;
        else if (vertex == w) return v;
        else throw new IllegalArgumentException("Vertex " + vertex + " is not an endpoint of this edge");
    }

    /**
     * Compares this edge to another by weight (natural ordering for min-heap).
     *
     * @param that the other edge
     * @return negative / zero / positive if this weight is less / equal / greater
     */
    @Override
    public int compareTo(Edge that) {
        return Double.compare(this.weight, that.weight);
    }

    @Override
    public String toString() {
        return String.format("%d-%d (%.2f)", v, w, weight);
    }
}
