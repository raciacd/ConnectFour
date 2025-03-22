# Connect Four – MCTS & Decision Trees

Artificial Intelligence project for the classic game **Connect Four**, developed for the AI 2024/2025 course.

## 🧠 Features
- Fully playable game supporting:
  - Human vs. Human  
  - Human vs. AI  
  - AI vs. AI  
- Implementation of **Monte Carlo Tree Search (MCTS)** using UCT
- Random AI as a baseline opponent
- Dataset generation using MCTS to train **Decision Trees** via ID3

## 🚧 In Progress
- Implementation of the ID3 algorithm
- Training a decision tree based on MCTS-generated data
- Building an AI player that uses the trained decision tree

## 📁 Project Structure
- `game.py` – command-line game interface
- `ConnectState.py` – board logic and rules
- `mcts.py` – Monte Carlo Tree Search AI
- `random_ai.py` – Random move AI
- `meta.py` – global constants

## 📌 Goal
To explore adversarial search strategies and supervised learning techniques applied to games.

---
