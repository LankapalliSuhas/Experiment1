import streamlit as st
import pandas as pd
import json
import time
from sudoku import Sudoku  # Import module for OOP logic

# Custom CSS for professional game look (basic styling via markdown)
st.markdown("""
    <style>
    .main-header {font-size: 4rem; color: #1f77b4; text-align: center; font-weight: bold;}
    .game-grid {background-color: #f0f0f0; padding: 10px; border-radius: 10px;}
    .cell-input {width: 50px; height: 50px; text-align: center; font-size: 1.2rem; border: 2px solid #ccc;}
    .given-cell {background-color: #e0e0e0; color: #333; font-weight: bold;}
    .error-cell {border-color: #ff0000;}
    .success-cell {background-color: #d4edda; border-color: #28a745;}
    .sidebar {background-color: #f8f9fa;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">GridCracker: Ultimate Sudoku Challenge</h1>', unsafe_allow_html=True)
st.markdown("---")

# OOP: Sudoku instance in session state (data structure persistence)
if 'sudoku' not in st.session_state:
    st.session_state.sudoku = Sudoku()
    st.session_state.user_grid = [[0 for _ in range(9)] for _ in range(9)]  # Separate user input grid
    st.session_state.solution_grid = [[0 for _ in range(9)] for _ in range(9)]  # For comparison
    st.session_state.timer_start = None
    st.session_state.elapsed_time = 0
    st.session_state.game_won = False
    st.session_state.difficulty = 'Medium'  # Default difficulty
    st.session_state.hints_used = 0

sudoku = st.session_state.sudoku
user_grid = st.session_state.user_grid
solution_grid = st.session_state.solution_grid

# Function: Start/Reset timer (basic concepts: time handling, conditionals)
def start_timer():
    if st.session_state.timer_start is None:
        st.session_state.timer_start = time.time()

def reset_timer():
    st.session_state.timer_start = None
    st.session_state.elapsed_time = 0

def update_timer():
    if st.session_state.timer_start:
        st.session_state.elapsed_time = time.time() - st.session_state.timer_start

# Function: Generate puzzle based on difficulty (OOP method call, data structures for cells)
def generate_new_puzzle():
    cells_to_remove = {'Easy': 30, 'Medium': 40, 'Hard': 50}[st.session_state.difficulty]
    sudoku.generate_puzzle(cells_to_remove)
    # Copy to user_grid for initial givens (loop to copy data structure)
    for i in range(9):
        for j in range(9):
            user_grid[i][j] = sudoku.grid[i][j] if sudoku.grid[i][j] != 0 else 0
    sudoku.solve()  # Solve once for solution storage
    for i in range(9):
        for j in range(9):
            solution_grid[i][j] = sudoku.grid[i][j]
    sudoku.generate_puzzle(cells_to_remove)  # Reset to puzzle state
    reset_timer()
    st.session_state.game_won = False
    st.session_state.hints_used = 0

# Function: Provide hint (basic loop, conditional check)
def give_hint():
    for i in range(9):
        for j in range(9):
            if user_grid[i][j] == 0 and sudoku.grid[i][j] != 0:  # Find first empty vs solution
                user_grid[i][j] = sudoku.grid[i][j]
                st.session_state.hints_used += 1
                return True
    return False

# Function: Check win condition (data structure comparison, loops)
def check_win():
    for i in range(9):
        for j in range(9):
            if user_grid[i][j] != solution_grid[i][j]:
                return False
    return True

# Function: Validate cell input (OOP call to is_valid, basic conditional)
def validate_cell(row, col, num):
    if num == 0 or sudoku.is_valid(row, col, num):
        return True
    return False

# Sidebar: Settings and Controls (interactive elements)
with st.sidebar:
    st.header("🎮 Game Controls")
    st.session_state.difficulty = st.selectbox("Difficulty", ['Easy', 'Medium', 'Hard'], index=['Easy', 'Medium', 'Hard'].index(st.session_state.difficulty))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Game", use_container_width=True):
            generate_new_puzzle()
            st.rerun()
    with col2:
        if st.button("💡 Hint", use_container_width=True, disabled=st.session_state.game_won):
            if give_hint():
                st.success("Hint applied!")
                st.rerun()
            else:
                st.warning("No hints needed - puzzle solved!")
    
    if st.button("🤖 Auto-Solve", use_container_width=True):
        for i in range(9):
            for j in range(9):
                user_grid[i][j] = solution_grid[i][j]
        st.session_state.game_won = True
        st.rerun()
    
    st.header("📁 File Handling")
    uploaded_file = st.file_uploader("Upload Puzzle (JSON)", type="json")
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            sudoku.load_from_file(io.StringIO(json.dumps(data)))  # Simulate file load
            generate_new_puzzle()  # Regenerate based on loaded
            st.success("Puzzle loaded!")
            st.rerun()
        except Exception as e:
            st.error(f"Invalid file: {e}")
    
    if st.button("💾 Save Progress (JSON)"):
        save_data = {'user_grid': user_grid, 'solution': solution_grid, 'time': st.session_state.elapsed_time}
        json_str = json.dumps(save_data)
        st.download_button("Download", json_str, "gridcracker_progress.json", "application/json")

# Main Area: Timer and Status
col_timer, col_stats = st.columns([3, 1])
with col_timer:
    update_timer()
    st.metric("⏱️ Time Elapsed", f"{int(st.session_state.elapsed_time)}s")
with col_stats:
    st.metric("💡 Hints Used", st.session_state.hints_used)
    win_status = "🏆 Won!" if st.session_state.game_won else "In Progress"
    st.metric("Status", win_status)

if st.session_state.game_won:
    st.balloons()
    st.success("Congratulations! Puzzle solved perfectly.")

st.markdown("---")

# Interactive Grid Rendering (9x9 with st.columns for rows, number_inputs for cells; styling via key/classes)
st.subheader("🧩 Sudoku Grid")
grid_container = st.container()
with grid_container:
    for i in range(9):
        # Basic loop for rows, use columns for 9 cells
        cols = st.columns(9)
        for j in range(9):
            with cols[j]:
                # Determine cell type: given (read-only), user input, or solved
                is_given = sudoku.grid[i][j] != 0
                cell_value = user_grid[i][j]
                input_key = f"cell_{i}_{j}"
                
                # Conditional styling and input
                if is_given:
                    st.markdown(f'<div class="cell-input given-cell">{sudoku.grid[i][j]}</div>', unsafe_allow_html=True)
                else:
                    num = st.number_input("", min_value=0, max_value=9, value=cell_value, key=input_key, 
                                          help="Enter 1-9 or 0 to clear", 
                                          format="%d",
                                          on_change=lambda: update_user_grid(i, j))
                    user_grid[i][j] = num
                    # Real-time validation
                    if num > 0 and not validate_cell(i, j, num):
                        st.markdown('<div class="cell-input error-cell"></div>', unsafe_allow_html=True)
                    elif st.session_state.game_won and num == solution_grid[i][j]:
                        st.markdown(f'<div class="cell-input success-cell">{num}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="cell-input">{num if num > 0 else ""}</div>', unsafe_allow_html=True)
        
        # Add line breaks for 3x3 boxes (visual enhancement)
        if (i + 1) % 3 == 0 and i < 8:
            st.markdown("---")

# Function: Update user grid on input change (called in on_change; basic assignment)
def update_user_grid(row, col):
    # This is a placeholder; Streamlit on_change triggers rerun, so state updates automatically
    pass

# Check win on every rerun (conditional after grid)
if not st.session_state.game_won:
    st.session_state.game_won = check_win()
    if st.session_state.game_won:
        st.rerun()

# Footer: Instructions
with st.expander("ℹ️ How to Play"):
    st.write("""
    - Fill the grid with numbers 1-9 without repeating in rows, columns, or 3x3 boxes.
    - Gray cells are givens; white are for your input.
    - Use Hint for help, Auto-Solve for instant solution.
    - Track time and hints for better scores!
    """)
