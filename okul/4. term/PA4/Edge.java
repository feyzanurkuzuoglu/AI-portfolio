import java.io.Serializable;

public class Edge implements Comparable<Edge>, Serializable {
    static final long serialVersionUID = 444L;

    Station to;
    double w;

    public Edge(Station t, double w) {
        to = t;
        this.w = w;
    }

    public int compareTo(Edge o) {
        return Double.compare(this.w, o.w);
    }
}