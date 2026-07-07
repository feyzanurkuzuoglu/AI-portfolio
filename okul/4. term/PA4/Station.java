import java.io.Serializable;
import java.util.*;

public class Station implements Serializable {
    static final long serialVersionUID = 222L;

    Point p;
    String name;
    List<Edge> edges = new ArrayList<>();

    public Station(Point p, String n) {
        this.p = p;
        name = n;
    }
}