import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * A generic Bag (multiset) backed by a singly-linked list.
 * Iteration order is LIFO (last added, first visited).
 *
 * Used as the adjacency-list container for Graph and Digraph.
 */
public class Bag<Item> implements Iterable<Item> {

    private Node<Item> first; // head of the list
    private int size;

    private static class Node<Item> {
        Item item;
        Node<Item> next;
    }

    /** Creates an empty bag. */
    public Bag() {
        first = null;
        size  = 0;
    }

    /** Returns {@code true} if the bag is empty. */
    public boolean isEmpty() {
        return first == null;
    }

    /** Returns the number of items in the bag. */
    public int size() {
        return size;
    }

    /** Adds {@code item} to the bag in O(1). */
    public void add(Item item) {
        Node<Item> oldFirst = first;
        first      = new Node<>();
        first.item = item;
        first.next = oldFirst;
        size++;
    }

    /** Returns an iterator that visits every item (no guaranteed order). */
    @Override
    public Iterator<Item> iterator() {
        return new LinkedIterator(first);
    }

    private class LinkedIterator implements Iterator<Item> {
        private Node<Item> current;

        LinkedIterator(Node<Item> first) {
            this.current = first;
        }

        @Override public boolean hasNext() { return current != null; }

        @Override
        public Item next() {
            if (!hasNext()) throw new NoSuchElementException();
            Item item = current.item;
            current   = current.next;
            return item;
        }
    }
}
