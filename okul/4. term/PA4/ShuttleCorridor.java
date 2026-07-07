import java.io.Serializable;
import java.util.*;

public class ShuttleCorridor implements Serializable {
    static final long serialVersionUID = 333L;

    String name;
    List<Station> stations;

    public ShuttleCorridor(String n, List<Station> s) {
        name = n;
        stations = s;
    }
}