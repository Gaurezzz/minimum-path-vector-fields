# Minimum Distance Path on Vector Fields

**InspiraSTEM 2026 Internship**

*   **Author:** Gabriela Rodriguez
*   **Mentor:** Dr. Manuel Diaz

## Description

This project implements an A* algorithm to find the minimum distance path across a vector field. It calculates the optimal route by taking into account the constant velocity of a particle and the underlying flow velocities of the vector field. It includes mathematical formulations and visualizations using the Manim engine to demonstrate the pathfinding across different flow scenarios.

## Project Structure

*   `main.py`: Main entry point containing the Manim animation scenes for different vector field simulations.
*   `src/`: Core package containing the A* pathfinding algorithm (`minimum_path_algorithm.py`), simulation base logic (`track_simulation.py`), and vector field definitions (`vector_field_functions/`).

## Execution

This project uses `uv` for dependency management. Ensure your dependencies are installed by running:

```bash
uv sync
```

### Run the Animations

The project uses Manim to visualize the minimum distance paths on different vector fields. You can render these animations by executing the following commands from the project root:

**Shear Flow Simulation:**
```bash
uv run manim -pql main.py Shear_Simulation
```

**Windy Field Simulation:**
```bash
uv run manim -pql main.py Windy_Simulation
```

**Double-Gyre Flow Simulation:**
```bash
uv run manim -pql main.py Gire_Simulation
```

**Channel Flow Simulation:**
```bash
uv run manim -pql main.py Channel_Flow_Simulation
```

**Cavity Flow Simulation:**
```bash
uv run manim -pql main.py Cavity_Flow_Simulation
```
