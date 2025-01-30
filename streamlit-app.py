# knights-tour-visualizer_v6
import streamlit as st
import numpy as np
import time
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Knight's Tour Visualizer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the chessboard
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }
    .chess-board {
        border: 2px solid #4a4a4a;
        border-radius: 5px;
        padding: 10px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px auto;
        width: fit-content;
    }
    .board-row {
        display: flex;
        justify-content: center;
    }
    .board-cell {
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        font-weight: bold;
        position: relative;
    }
    .cell-light {
        background-color: #f0d9b5;
    }
    .cell-dark {
        background-color: #b58863;
    }
    .number {
        color: #2c3e50;
    }
    .removed-corner {
        background-color: #e74c3c !important;
        color: white;
        font-size: 24px;
    }
    .current-position {
        background-color: #27ae60 !important;
        color: white;
    }
    .title {
        text-align: center;
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #34495e;
        font-family: 'Arial', sans-serif;
        margin-bottom: 30px;
        font-size: 1.2em;
    }
    .controls {
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        width: 300px;
    }
    .coordinate-label {
        color: #666;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

def is_valid_move(x, y, board):
    """Check if the move is valid on our modified board."""
    if x < 0 or x >= 8 or y < 0 or y >= 8:
        return False
    # Check if it's one of the removed corner squares
    if (x, y) in {(0, 0), (0, 7), (7, 0), (7, 7)}:
        return False
    return board[x][y] == -1

def get_valid_moves(x, y, board):
    """Get all valid moves from current position."""
    moves = [
        (x + 2, y + 1), (x + 2, y - 1),
        (x - 2, y + 1), (x - 2, y - 1),
        (x + 1, y + 2), (x + 1, y - 2),
        (x - 1, y + 2), (x - 1, y - 2)
    ]
    return [(x, y) for x, y in moves if is_valid_move(x, y, board)]

def solve_knights_tour(start_x, start_y):
    """Solve Knight's Tour using Warnsdorff's algorithm."""
    board = np.full((8, 8), -1)
    # Mark corner squares as visited
    board[0, 0] = board[0, 7] = board[7, 0] = board[7, 7] = -2
    
    move_x = start_x
    move_y = start_y
    board[move_x][move_y] = 0
    
    path = [(move_x, move_y)]
    total_squares = 60  # 64 - 4 (corners removed)
    
    for move_count in range(1, total_squares):
        valid_moves = get_valid_moves(move_x, move_y, board)
        
        if not valid_moves:
            return None
        
        # Warnsdorff's heuristic: choose the move with fewest onward moves
        next_move = min(valid_moves, 
                       key=lambda move: len(get_valid_moves(move[0], move[1], board)))
        
        move_x, move_y = next_move
        board[move_x][move_y] = move_count
        path.append((move_x, move_y))
    
    return path

def create_board_html(board, current_pos=None):
    """Create HTML representation of the chessboard."""
    html = '<div class="chess-board">'
    
    # Add column labels (0-7)
    html += '<div class="board-row">'
    html += '<div class="board-cell"></div>'  # Empty corner
    for col in range(8):
        html += f'<div class="board-cell">{col}</div>'
    html += '</div>'
    
    for row in range(8):
        html += '<div class="board-row">'
        # Add row labels (0-7)
        html += f'<div class="board-cell">{row}</div>'
        
        for col in range(8):
            is_light = (row + col) % 2 == 0
            cell_class = 'cell-light' if is_light else 'cell-dark'
            
            # Check if it's a removed corner
            if (row, col) in {(0, 0), (0, 7), (7, 0), (7, 7)}:
                cell_class += ' removed-corner'
                cell_content = '×'
            else:
                value = board[row][col]
                if value >= 0:
                    cell_content = str(value)
                    if (row, col) == current_pos:
                        cell_class += ' current-position'
                else:
                    cell_content = ''
            
            html += f'<div class="board-cell {cell_class}">{cell_content}</div>'
        html += '</div>'
    html += '</div>'
    return html

def create_initial_board():
    """Create the initial empty board with removed corners."""
    board = np.full((8, 8), -1)
    # Mark corners as removed
    board[0, 0] = board[0, 7] = board[7, 0] = board[7, 7] = -2
    return board

def main():
    # Add responsive CSS with blinking animation
    st.markdown("""
        <style>
        /* Container styles */
        .container {
            max-width: 100%;
            margin: 0 auto;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        /* Title styles */
        .title {
            text-align: center;
            color: #1f1f1f;
            font-size: min(1.6em, 4.5vw);
            margin-bottom: 0.3em;
            width: 100%;
        }
        
        .subtitle {
            text-align: center;
            color: #4f4f4f;
            font-size: min(1.2em, 4vw);
            margin-bottom: 1.5em;
            width: 100%;
        }
        
        /* Chess board styles */
        .chess-board-container {
            width: min(80vh, 90vw);
            aspect-ratio: 1;
            margin: 0 auto;
            padding: 0;
            display: flex;
            flex-direction: column;
        }
        
        .chess-board {
            width: 100%;
            height: 100%;
            border: 2px solid #333;
            background: #fff;
            display: flex;
            flex-direction: column;
        }
        
        .board-row {
            display: flex;
            flex: 1;
            width: 100%;
        }
        
        .board-cell {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: min(1em, 2.5vw);
            font-weight: bold;
            position: relative;
        }
        
        /* Cell colors */
        .cell-light {
            background-color: #f0d9b5;
        }
        
        .cell-dark {
            background-color: #b58863;
            color: #f0d9b5;
        }
        
        .removed-corner {
            background-color: #cc0000;
            color: #ffffff;
        }
        
        .current-position {
            background-color: #76b041;
            color: #ffffff;
        }
        
        /* Controls section */
        .controls {
            width: min(80vh, 90vw);
            margin: 1.5em auto;
            padding: 1em;
            background: #f8f9fa;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .chess-board-container {
                width: 95vw;
            }
            .controls {
                width: 95vw;
            }
            .board-cell {
                font-size: 3vw;
            }
        }
        
        @media (max-height: 800px) {
            .title {
                margin-bottom: 0.3em;
            }
            .subtitle {
                margin-bottom: 0.8em;
            }
            .controls {
                margin: 0.8em auto;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">Knight\'s Tour Visualization</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Modified 8x8 chessboard with corners removed</p>', unsafe_allow_html=True)
    
    # Create a placeholder for the board and show initial empty board
    board_placeholder = st.empty()
    initial_board = create_initial_board()
    board_html = create_board_html(initial_board)
    board_placeholder.markdown('<div class="chess-board-container">' + board_html + '</div>', unsafe_allow_html=True)
    
    # Create the controls section
    with st.container():
        st.markdown('<div class="controls">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            start_x = st.number_input("Start X (0-7)", min_value=0, max_value=7, value=2)
        with col2:
            start_y = st.number_input("Start Y (0-7)", min_value=0, max_value=7, value=2)
        
        if st.button("Find Tour", type="primary", use_container_width=True):
            if (start_x, start_y) in {(0, 0), (0, 7), (7, 0), (7, 7)}:
                st.error("Cannot start from a removed corner!")
            else:
                path = solve_knights_tour(start_x, start_y)
                if path:
                    board = np.full((8, 8), -1)
                    # Mark corners as removed
                    board[0, 0] = board[0, 7] = board[7, 0] = board[7, 7] = -2
                    
                    # Animate the knight's tour
                    for i, (x, y) in enumerate(path):
                        board[x, y] = i
                        # Display the current state with the current position highlighted
                        if i == len(path) - 1:  # Last move
                            # Show green
                            board_html = create_board_html(board, current_pos=(x, y))
                            board_placeholder.markdown('<div class="chess-board-container">' + board_html + '</div>', unsafe_allow_html=True)
                            time.sleep(0.3)
                            
                            # Blink 2 times
                            for _ in range(2):
                                # Remove highlight
                                board_html = create_board_html(board)
                                board_placeholder.markdown('<div class="chess-board-container">' + board_html + '</div>', unsafe_allow_html=True)
                                time.sleep(0.3)
                                
                                # Show highlight
                                board_html = create_board_html(board, current_pos=(x, y))
                                board_placeholder.markdown('<div class="chess-board-container">' + board_html + '</div>', unsafe_allow_html=True)
                                time.sleep(0.3)
                            
                            # Finally show without highlight
                            board_html = create_board_html(board)
                            board_placeholder.markdown('<div class="chess-board-container">' + board_html + '</div>', unsafe_allow_html=True)
                        else:
                            board_html = create_board_html(board, current_pos=(x, y))
                            board_placeholder.markdown('<div class="chess-board-container">' + board_html + '</div>', unsafe_allow_html=True)
                            time.sleep(0.5)
                    
                    st.success("Tour completed!")
                else:
                    st.error("No valid tour found from this starting position. Try a different starting point!")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
