# AI/ML Interactive Games Collection

A collection of interactive AI and ML games implemented using Flask and Pygame. This project includes classic AI problems and algorithms presented in both web-based and standalone Pygame interfaces.

## Games Included

1. **Tic Tac Toe**
   - Classic game implementation with AI opponent
   - Web-based interface

2. **Water Jug Puzzle**
   - Implementation of the classic water jug problem
   - Available in both web-based and Pygame versions
   - Demonstrates state space search in AI

3. **8 Puzzle**
   - Sliding puzzle game
   - Web-based implementation
   - Showcases pathfinding algorithms

4. **Travelling Salesman Problem**
   - Visualization of the TSP algorithm
   - Web-based interface
   - Demonstrates optimization in AI

5. **Find-S Algorithm**
   - Machine Learning concept demonstration
   - Available in both web-based and Pygame versions
   - Shows concept learning in ML

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, Web Templates
- **Game Engine**: Pygame (for standalone versions)

## Setup Instructions

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```bash
   python app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Game Access

- Web versions of all games are accessible through the main menu
- For Pygame versions (Water Jug and Find-S):
  - Access through dedicated routes in the web interface
  - Will launch as separate window applications

## Project Structure

- `app.py` - Main Flask application
- `waterjug_game.py` - Pygame implementation of Water Jug puzzle
- `finds_game.py` - Pygame implementation of Find-S algorithm
- `templates/` - Contains HTML templates for web interfaces
- `requirements.txt` - Project dependencies

## Development Mode

The application runs in debug mode by default, making it suitable for development and testing.

## Note

Ensure you have Python and pip installed on your system before setting up the project. The web interface provides a unified way to access all games, while some games have additional Pygame implementations for enhanced interactivity.