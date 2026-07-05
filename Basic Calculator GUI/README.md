# Basic Calculator GUI

A simple and modern graphical calculator application built using Python and the `customtkinter` library. This project not only provides a functional calculator but also serves as a great example of core Object-Oriented Programming (OOP) principles in practice.

## 📂 File Structure

*   **`main.py`**: The starting point of the application. Running this file launches the calculator window.
*   **`calculator.py`**: The "brain" of the calculator. It handles all the math logic and is structured using strong OOP concepts.
*   **`ui.py`**: The visual part of the application. It uses `customtkinter` to draw the buttons, screen, and layout, and it connects those buttons to the logic in `calculator.py`.
*   **`requirements.txt`**: A list of the external Python libraries needed to run this project (like `customtkinter`).

## 🏛️ The Four Pillars of OOP in This Code

This project was built to clearly demonstrate the four fundamental concepts of Object-Oriented Programming. Here is how they appear in the code, explained simply:

### 1. Abstraction
*What it means:* Hiding complex background details and showing only the essential parts. Think of a TV remote: you press a button to change the channel without needing to know how the remote's internal circuitry works.
*Where it is in the code:* In `calculator.py`, we have a class called `Operation`. This is an "Abstract Base Class" (ABC). It defines a rule that any operation *must* have an `execute()` method, but it doesn't actually do any math itself. It provides a simple, standard way to talk about operations without getting bogged down in the details of addition versus division.

### 2. Inheritance
*What it means:* Creating new classes that are based on an existing class. The new class "inherits" properties and behaviors from the parent class, allowing you to reuse code.
*Where it is in the code:* In `calculator.py`, the `Addition`, `Subtraction`, `Multiplication`, and `Division` classes all inherit from the parent `Operation` class. Because they inherit from `Operation`, they agree to follow its rules (having an `execute()` method) and provide their specific mathematical logic.

### 3. Encapsulation
*What it means:* Keeping an object's internal data safe and hidden from the outside world. It bundles the data and the functions that use that data into one secure package. You can only interact with the object through specific, allowed methods.
*Where it is in the code:* In `calculator.py`, the `Calculator` class holds variables like `self._val` (the current number on the screen) and `self._op` (the current math operation). The underscore `_` at the beginning of these names is a signal in Python that these are "private" and shouldn't be touched directly from the outside (like from `ui.py`). Instead, `ui.py` interacts with the calculator using safe, public methods like `input_digit()`, `calculate()`, and `clear()`.

### 4. Polymorphism
*What it means:* "Many forms." It's the ability to use a single type of command or method on different types of objects, and each object will know exactly how to handle it in its own way.
*Where it is in the code:* Inside the `Calculator` class (in `calculator.py`), there is a dictionary called `self._ops` that holds all the different operation objects (Addition, Subtraction, etc.). When the user hits the "=" button, the calculator simply calls `self._op.execute(...)`. The calculator doesn't need to write a bunch of `if/else` statements to check what kind of operation it is. Because of polymorphism, it just calls `execute()`, and whether the object is `Addition` or `Division`, that object knows the right math to perform!
