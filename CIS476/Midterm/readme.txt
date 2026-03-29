README – Design Patterns Overview
1. Factory Method

Definition:
A creational pattern that defines an interface for creating objects but lets subclasses decide which class to instantiate.

When to use:

When a class cannot anticipate the type of objects it needs to create.

When you want to delegate object creation to subclasses.

Pros:

Promotes loose coupling between client and concrete classes.

Easy to introduce new product types without changing client code.

Cons:

Can introduce additional complexity with many small subclasses.

Slight overhead for creating multiple factory classes.

Singleton use:

Often combined to ensure only one factory instance exists.

Example: GoldenPizza factory where only one special pizza can be created.

2. Abstract Factory

Definition:
A creational pattern that provides an interface for creating families of related objects without specifying their concrete classes.

When to use:

When your system needs to support multiple families of products (e.g., UI elements for different platforms).

When you want to ensure consistency among products in a family.

Pros:

Promotes consistency across related products.

Abstracts away the details of concrete classes.

Cons:

Adding a new product type requires updating all factories.

More complex than Factory Method.

Singleton use:

Factories can be Singleton to prevent multiple instances of the same product family.

Example: Only one WindowsFactory or MacFactory exists to enforce consistent UI objects.

3. Builder

Definition:
A creational pattern that separates the construction of a complex object from its representation so that the same construction process can create different representations.

When to use:

When you need to create complex objects step by step.

When objects have many optional attributes.

Pros:

Clear separation between construction and representation.

Easy to create different variations of an object.

Cons:

More classes/code for the builder and director.

May introduce unnecessary complexity for simple objects.

Singleton use:

Builders can be Singleton if only one construction manager is needed.

Example: FighterJetBuilder as a Singleton to ensure only one fighter jet is built.

4. Decorator

Definition:
A structural pattern that allows behavior to be added to individual objects dynamically without affecting other objects of the same class.

When to use:

When you want to add features dynamically at runtime.

When subclassing would create a combinatorial explosion of classes.

Pros:

Flexible alternative to subclassing.

Can add multiple independent features to an object.

Cons:

Can lead to many small objects that are hard to track.

Debugging can be more difficult due to many layers of decorators.

Singleton use:

Can be combined for unique decorators, e.g., a single free gift in a ticket order (Gift decorator).

5. Adapter

Definition:
A structural pattern that allows incompatible interfaces to work together. It wraps an existing class with a new interface expected by the client.

When to use:

When you want to reuse existing classes that have incompatible interfaces.

When integrating third-party APIs or legacy code.

Pros:

Promotes code reuse.

Keeps client code unchanged.

Cons:

Can introduce extra layers.

May add minor runtime overhead.

Singleton use:

Can enforce one instance of an adapter if a resource must be unique.

Example: TS3AdapterSingleton ensures only one hardware sensor is used in the system.

6. Singleton

Definition:
A creational pattern that ensures a class has only one instance and provides a global point of access to it.

When to use:

When exactly one object is needed to coordinate actions (e.g., configuration, logging, factories).

Pros:

Provides controlled access to a single instance.

Can coordinate shared resources across a system.

Cons:

Can be abused as a global variable, reducing modularity.

Harder to test because of global state.

Use with other patterns:

Often combined with Factory, Abstract Factory, Builder, Decorator, or Adapter to enforce a single instance of a factory, director, unique decorator, or adapter.

class GoldenPizza(Pizza):
    _instances = []  # store up to 2 instances

    def __new__(cls, *args, **kwargs):
        if len(cls._instances) < 2:
            instance = super().__new__(cls)
            cls._instances.append(instance)
            return instance
        else:
            print("Sorry, only two Golden Pizzas allowed! Cannot create another.")
            return None  # Block creation

    def prepare(self):
        # Identify which pizza instance is being prepared
        index = GoldenPizza._instances.index(self) + 1
        print(f"Preparing Golden Pizza #{index}!")