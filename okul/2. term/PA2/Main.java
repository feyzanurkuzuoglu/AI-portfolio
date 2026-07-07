import java.io.*;
import java.util.*;

// abstract Animal class
abstract class Animal {
    protected String name;
    protected int age;

    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }
    //Calculates how much food each animal will eat based on the information given
    abstract double getDailyMealSize();
    //Function that gives the animal's cleaning message when visited by personnel
    abstract void cleanHabitat();
}


class Lion extends Animal {
    public Lion(String name, int age) { super(name, age); }
    @Override
    double getDailyMealSize() { return  5.0 + (age - 5) * 0.05; }
    @Override
    void cleanHabitat() {
        Main.writeToOutput("Cleaning " + name + "'s habitat: Removing bones and refreshing sand.");
    }
}

class Elephant extends Animal {
    public Elephant(String name, int age) { super(name, age); }
    @Override
    double getDailyMealSize() { return 10.0 + (age - 20) * 0.015; }
    @Override
    void cleanHabitat() {
        Main.writeToOutput("Cleaning " + name + "'s habitat: Washing the water area.");
    }
}

class Penguin extends Animal {
    public Penguin(String name, int age) { super(name, age); }
    @Override
    double getDailyMealSize() { return 3.0 + (age - 4) * 0.04; }
    @Override
    void cleanHabitat() {
        Main.writeToOutput("Cleaning " + name + "'s habitat: Replenishing ice and scrubbing walls.");
    }
}

class Chimpanzee extends Animal {
    public Chimpanzee(String name, int age) { super(name, age); }
    @Override
    double getDailyMealSize() { return 6.0 + (age - 10) * 0.025; }
    @Override
    void cleanHabitat() {
        Main.writeToOutput("Cleaning " + name + "'s habitat: Sweeping the enclosure and replacing branches.");
    }
}

// abstract Person(for visitors and personnels) class
abstract class Person {
    protected String name;
    protected int id;

    public Person(String name, int id) {
        this.name = name;
        this.id = id;
    }
}

class Visitor extends Person {
    public Visitor(String name, int id) { super(name, id); }
}

class Personnel extends Person {
    public Personnel(String name, int id) { super(name, id); }
}

// FoodStock class to handle "List Food Stock" command
class FoodStock {
    public static double meat = 0;
    public static double fish = 0;
    public static double plant = 0;

    public static void listFoodStock() {
        Main.writeToOutput("Listing available Food Stock:");
        Main.writeToOutput("Plant: " + String.format("%.3f", plant) + " kgs");
        Main.writeToOutput("Fish: " + String.format("%.3f", fish) + " kgs");
        Main.writeToOutput("Meat: " + String.format("%.3f", meat) + " kgs");
    }
}

// Exception Classes 
class NotAuthorizedException extends Exception {
    public NotAuthorizedException(String message) { super(message); }
}

class NotEnoughFoodException extends Exception {
    public NotEnoughFoodException(String message) { super(message); }
}

class PersonNotFoundException extends Exception {
    public PersonNotFoundException(String message) { super(message); }
}

class AnimalNotFoundException extends Exception {
    public AnimalNotFoundException(String message) { super(message); }
}







public class Main {
    //I stored animal and person objects in ArrayList
    public static ArrayList<Animal> animals = new ArrayList<>();
    public static ArrayList<Person> persons = new ArrayList<>();
    public static FoodStock foodStock = new FoodStock();
    public static String outputFile;

    public static void main(String[] args) throws Exception {
        if (args.length != 5) {
            System.out.println("Usage: java Main animals.txt persons.txt foods.txt commands.txt output.txt");
            return;
        }


        String animalsFile = args[0];
        String personsFile = args[1];
        String foodsFile = args[2];
        String commandsFile = args[3];
        outputFile = args[4];

       

        //Take each as a separate file and send it to separate methods for reading
        processAnimals(animalsFile);
        processPersons(personsFile);
        processFoods(foodsFile);
        processCommands(commandsFile);
    }

    // I used the file reading and writing methods that were given to us in the previous assignment.
    public static void writeToOutput(String message) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile, true))) {
            writer.write(message);
            writer.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Reading animalsFile and creating new animal objects and adding them to animals ArrayList
    public static void processAnimals(String filename) throws IOException {
        writeToOutput("***********************************");
        writeToOutput("***Initializing Animal information***");
        BufferedReader br = new BufferedReader(new FileReader(filename));
        String line;
        while ((line = br.readLine()) != null) {
            String[] parts = line.split(",");
            String type = parts[0];
            String name = parts[1];
            int age = Integer.parseInt(parts[2]);  //type conversion
            switch (type) {
                case "Lion": animals.add(new Lion(name, age)); break;
                case "Elephant": animals.add(new Elephant(name, age)); break;
                case "Penguin": animals.add(new Penguin(name, age)); break;
                case "Chimpanzee": animals.add(new Chimpanzee(name, age)); break;
            }
            writeToOutput("Added new " + type + " with name " + name + " aged " + age + ".");
        }
        br.close();
    }

    // does the same for persons
    public static void processPersons(String filename) throws IOException {
        writeToOutput("***********************************");
        writeToOutput("***Initializing Visitor and Personnel information***");
        BufferedReader br = new BufferedReader(new FileReader(filename));
        String line;
        while ((line = br.readLine()) != null) {
            String[] parts = line.split(",");
            String type = parts[0];
            String name = parts[1];
            int id = Integer.parseInt(parts[2]);
            if (type.equals("Visitor")) {
                persons.add(new Visitor(name, id));
            } else if (type.equals("Personnel")) {
                persons.add(new Personnel(name, id));
            }
            writeToOutput("Added new " + type + " with id " + id + " and name " + name + ".");
        }
        br.close();
    }

    // Read food quantities from foods file and update foodStock object
    public static void processFoods(String filename) throws IOException {
        writeToOutput("***********************************");
        writeToOutput("***Initializing Food Stock***");
        BufferedReader br = new BufferedReader(new FileReader(filename));
        String line;
        while ((line = br.readLine()) != null) {
            String[] parts = line.split(",");
            String type = parts[0];
            double amount = Double.parseDouble(parts[1]); //type conversion
            switch (type) {
                case "Meat": foodStock.meat = amount; break;
                case "Fish": foodStock.fish = amount; break;
                case "Plant": foodStock.plant = amount; break;
            }
        }
        writeToOutput("There are " + String.format("%.3f", foodStock.meat) + " kg of Meat in stock");
        writeToOutput("There are " + String.format("%.3f", foodStock.fish) + " kg of Fish in stock");
        writeToOutput("There are " + String.format("%.3f", foodStock.plant) + " kg of Plant in stock");
        br.close();
    }

    //Reads the commands file and calls the required method according to the command.
    public static void processCommands(String filename) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(filename));
        String line;
        while ((line = br.readLine()) != null) {
            writeToOutput("***********************************");
            writeToOutput("***Processing new Command***");
            try {
                String[] parts = line.split(",");
                String operation = parts[0];

                if (operation.equals("List Food Stock")) {
                    foodStock.listFoodStock();
                } else if (operation.equals("Animal Visitation")) {
                    int id = Integer.parseInt(parts[1]);
                    String animalName = parts[2];
                    visitAnimal(id, animalName);
                } else if (operation.equals("Feed Animal")) {
                    int id = Integer.parseInt(parts[1]);
                    String animalName = parts[2];
                    int mealCount = Integer.parseInt(parts[3]);
                    feedAnimal(id, animalName, mealCount);
                }
            } catch (Exception e) {
                
                writeToOutput("Error: " + e.getMessage());
            }
        }
        br.close();
    }



    public static void visitAnimal(int id, String animalName) throws PersonNotFoundException, AnimalNotFoundException {
        Person person = null;
        Animal animal = null;

        //Checks the ArrayList content if the name matches
        for (Animal a : animals) {
            if (a.name.equals(animalName)) {
                animal = a;
                break;
            }
        }
        if (animal == null) {
            throw new AnimalNotFoundException("There is no animal with the name: " + animalName);
        }
    
        //Checks the ArrayList content if the id matches
        for (Person p : persons) {
            if (p.id == id) {
                person = p;
                break;
            }
        }

        if (person == null) {
            throw new PersonNotFoundException("There are no visitors or personnel with the id: " + id);
        }


        if (person instanceof Visitor) {
            writeToOutput(person.name + " tried  to register for a visit to " + animal.name );
            writeToOutput(person.name + " successfully visited " + animal.name + ".");
        } else if (person instanceof Personnel) {
            writeToOutput(person.name + " attempts to clean " + animal.name + "'s habitat.");
            writeToOutput(person.name + " started cleaning " + animal.name  + "'s habitat.");
            animal.cleanHabitat();  //method of Animal Class
        }
    }



    public static void feedAnimal(int id, String animalName, int mealCount) throws Exception {
        Person person = null;
        Animal animal = null;

        for (Animal a : animals) {
            if (a.name.equals(animalName)) {
                animal = a;
                break;
            }
        }
        if (animal == null) {
            throw new AnimalNotFoundException("There is no animal with the name: " + animalName);
        }
    
        for (Person p : persons) {
            if (p.id == id) {
                person = p;
                break;
            }
        }
        if (person == null) {
            throw new PersonNotFoundException("There are no visitors or personnel with the id: " + id);
        }


        if (person instanceof Visitor) {
            writeToOutput(person.name + " tried to feed " + animal.name + ".");
            throw new NotAuthorizedException("Visitors do not have the authority to feed animals.");
        }

        writeToOutput(person.name + " attempts to feed " + animal.name + ".");

        //Calculates the required amount of food with getDailyMealSize() in the Animal class.
        double requiredFood = animal.getDailyMealSize() * mealCount ;

        if (animal instanceof Lion) {
            if (foodStock.meat >= requiredFood) {  //If there is enough in foodStock
                foodStock.meat -= requiredFood;
                writeToOutput(animal.name + " has been given " + String.format("%.3f", requiredFood) + " kgs of meat");
            } else {
                throw new NotEnoughFoodException("Not enough Meat");
            }
        } else if (animal instanceof Elephant) {
            if (foodStock.plant >= requiredFood) {
                foodStock.plant -= requiredFood;
                writeToOutput(animal.name + " has been given " + String.format("%.3f", requiredFood) + " kgs of plants");
            } else {
                throw new NotEnoughFoodException("Not enough Plant");
            }
        } else if (animal instanceof Penguin) {
            if (foodStock.fish >= requiredFood) {
                foodStock.fish -= requiredFood;
                writeToOutput(animal.name + " has been given " + String.format("%.3f", requiredFood) + " kgs of fish");
            } else {
                throw new NotEnoughFoodException("Not enough Fish");
            }
        } else if (animal instanceof Chimpanzee) {
            double half = requiredFood / 2;
            if (foodStock.meat >= half && foodStock.plant >= half) {
                foodStock.meat -= half;
                foodStock.plant -= half;
                writeToOutput(animal.name + " has been given " + String.format("%.3f", half) + " kgs of meat and " + String.format("%.3f", half) + " kgs of plants");
            } else {
                throw new NotEnoughFoodException("Not enough Meat or Plant");
            }
        }
    }
}
