import streamlit as st
import time

# Set page configuration
st.set_page_config(
    page_title="Water Jug Game",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
.water-jug {
    width: 100px;
    height: 200px;
    border: 4px solid #2c3e50;
    border-radius: 0 0 10px 10px;
    position: relative;
    margin: 20px;
    background: #f8f9fa;
    cursor: move;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    overflow: hidden;
}

.water-jug.dragging {
    transform: scale(1.05);
    opacity: 0.8;
    box-shadow: 0 8px 15px rgba(0,0,0,0.2);
}

.water {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background: linear-gradient(to bottom, #64b5f6, #2196f3);
    transition: height 0.8s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s ease;
    border-radius: 0 0 5px 5px;
    box-shadow: inset 0 2px 5px rgba(255,255,255,0.3);
    transform-origin: bottom;
    animation: waterWave 2s infinite linear;
}

.water-jug.filling .water {
    animation: waterWave 2s infinite linear, waterFill 0.8s ease-out;
}

.water-jug.emptying .water {
    animation: waterWave 2s infinite linear, waterEmpty 0.8s ease-in;
}

@keyframes waterFill {
    from { transform: scaleY(0.1); opacity: 0.7; }
    to { transform: scaleY(1); opacity: 1; }
}

@keyframes waterEmpty {
    from { transform: scaleY(1); opacity: 1; }
    to { transform: scaleY(0.1); opacity: 0.7; }
}

@keyframes waterWave {
    0%, 100% {
        transform: translateX(0);
    }
    50% {
        transform: translateX(-2px);
    }
}

.tap {
    width: 60px;
    height: 60px;
    cursor: pointer;
    margin: 20px;
}

.drain {
    width: 60px;
    height: 60px;
    cursor: pointer;
    margin: 20px;
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'jug1_water' not in st.session_state:
    st.session_state.jug1_water = 0
if 'jug2_water' not in st.session_state:
    st.session_state.jug2_water = 0
if 'target_achieved' not in st.session_state:
    st.session_state.target_achieved = False

# Game configuration
JUG1_CAPACITY = 4
JUG2_CAPACITY = 3
TARGET_AMOUNT = 2  # The target amount of water to measure

# Game title and instructions
st.title('🚰 Water Jug Game')
st.markdown(f'Goal: Measure exactly {TARGET_AMOUNT}L of water using two jugs of {JUG1_CAPACITY}L and {JUG2_CAPACITY}L capacity!')

# Check if target is achieved
if (st.session_state.jug1_water == TARGET_AMOUNT or st.session_state.jug2_water == TARGET_AMOUNT) and not st.session_state.target_achieved:
    st.success('🎉 Congratulations! You have measured the target amount of water!')
    st.session_state.target_achieved = True
elif st.session_state.target_achieved and (st.session_state.jug1_water != TARGET_AMOUNT and st.session_state.jug2_water != TARGET_AMOUNT):
    st.session_state.target_achieved = False

# Create columns for layout
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="tap">🚰</div>', unsafe_allow_html=True)

with col2:
    # Create container for jugs
    st.markdown("""
    <div class="container">
        <div class="water-jug" id="jug1" draggable="true">
            <div class="water" style="height: {}%"></div>
        </div>
        <div class="water-jug" id="jug2" draggable="true">
            <div class="water" style="height: {}%"></div>
        </div>
    </div>
    """.format(
        (st.session_state.jug1_water/JUG1_CAPACITY)*100,
        (st.session_state.jug2_water/JUG2_CAPACITY)*100
    ), unsafe_allow_html=True)

with col3:
    st.markdown('<div class="drain">🚽</div>', unsafe_allow_html=True)

# Add JavaScript for drag and drop functionality
st.markdown("""
<script>
let isDragging = false;
let draggedJug = null;

function updateWaterLevel(jugId, waterAmount, capacity) {
    const jug = document.getElementById(jugId);
    if (jug) {
        const waterElement = jug.querySelector('.water');
        if (waterElement) {
            const heightPercentage = Math.min(100, Math.max(0, (waterAmount / capacity) * 100));
            waterElement.style.height = `${heightPercentage}%`;
            waterElement.style.transition = 'height 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
        }
    }
}

function initializeGame() {
    const jugs = document.querySelectorAll('.water-jug');
    const tap = document.querySelector('.tap');
    const drain = document.querySelector('.drain');

    // Initial water level update
    updateWaterLevel('jug1', window.jug1_water || 0, 4);
    updateWaterLevel('jug2', window.jug2_water || 0, 3);

    // Add click events for tap and drain
    tap.addEventListener('click', function() {
        const nearestJug = findNearestJug(tap);
        if (nearestJug) {
            window.Streamlit.setComponentValue({action: 'fill', jug: nearestJug === 'jug1' ? 1 : 2});
        }
    });

    drain.addEventListener('click', function() {
        const nearestJug = findNearestJug(drain);
        if (nearestJug) {
            window.Streamlit.setComponentValue({action: 'empty', jug: nearestJug === 'jug1' ? 1 : 2});
        }
    });

    // Enhanced drag and drop setup
    jugs.forEach(jug => {
        jug.addEventListener('mousedown', handleMouseDown);
        jug.addEventListener('dragstart', handleDragStart);
        jug.addEventListener('drag', handleDrag);
        jug.addEventListener('dragend', handleDragEnd);
    });

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    tap.addEventListener('dragenter', handleDragEnter);
    tap.addEventListener('dragover', handleDragOver);
    tap.addEventListener('drop', handleTapDrop);

    drain.addEventListener('dragenter', handleDragEnter);
    drain.addEventListener('dragover', handleDragOver);
    drain.addEventListener('drop', handleDrainDrop);

    // Listen for changes from Streamlit
    window.addEventListener('message', function(event) {
        if (event.data.type === 'streamlit:render') {
            const data = event.data;
            if (data.args && data.args.jug1_water !== undefined && data.args.jug2_water !== undefined) {
                updateWaterLevel('jug1', data.args.jug1_water, 4);
                updateWaterLevel('jug2', data.args.jug2_water, 3);
            }
        }
    });
}

function handleMouseDown(e) {
    if (e.button !== 0) return; // Only handle left mouse button
    isDragging = true;
    draggedJug = e.currentTarget;
    draggedJug.classList.add('dragging');
    
    // Calculate offset of mouse position relative to jug
    const rect = draggedJug.getBoundingClientRect();
    draggedJug.dataset.offsetX = e.clientX - rect.left;
    draggedJug.dataset.offsetY = e.clientY - rect.top;
    
    e.preventDefault(); // Prevent text selection
}

function handleMouseMove(e) {
    if (!isDragging || !draggedJug) return;
    
    const x = e.clientX - draggedJug.dataset.offsetX;
    const y = e.clientY - draggedJug.dataset.offsetY;
    
    draggedJug.style.position = 'absolute';
    draggedJug.style.left = `${x}px`;
    draggedJug.style.top = `${y}px`;
    draggedJug.style.zIndex = '1000';
}

function handleMouseUp(e) {
    if (!isDragging || !draggedJug) return;
    
    isDragging = false;
    draggedJug.classList.remove('dragging');
    draggedJug.style.position = '';
    draggedJug.style.left = '';
    draggedJug.style.top = '';
    draggedJug.style.zIndex = '';
    
    // Check if dropped on another jug
    const dropTarget = document.elementFromPoint(e.clientX, e.clientY);
    if (dropTarget) {
        const targetJug = dropTarget.closest('.water-jug');
        if (targetJug && targetJug !== draggedJug) {
            handleJugDrop(draggedJug.id, targetJug.id);
        }
    }
    
    draggedJug = null;
}

function handleDragStart(e) {
    e.dataTransfer.setData('text/plain', e.target.id);
    e.target.classList.add('dragging');
}

function handleDrag(e) {
    e.preventDefault();
    const jug = e.target;
    jug.style.opacity = '0.7';
}

function handleDragEnter(e) {
    e.preventDefault();
    e.target.classList.add('drag-over');
}

function handleDragOver(e) {
    e.preventDefault();
}

function handleDragEnd(e) {
    e.target.classList.remove('dragging');
    e.target.style.opacity = '';
    document.querySelectorAll('.drag-over').forEach(element => {
        element.classList.remove('drag-over');
    });
}

function findNearestJug(element) {
    const jug1 = document.getElementById('jug1');
    const jug2 = document.getElementById('jug2');
    const elementRect = element.getBoundingClientRect();
    const jug1Rect = jug1.getBoundingClientRect();
    const jug2Rect = jug2.getBoundingClientRect();
    
    const distToJug1 = Math.hypot(elementRect.left - jug1Rect.left, elementRect.top - jug1Rect.top);
    const distToJug2 = Math.hypot(elementRect.left - jug2Rect.left, elementRect.top - jug2Rect.top);
    
    return distToJug1 < distToJug2 ? 'jug1' : 'jug2';
}

function handleTapDrop(e) {
    e.preventDefault();
    e.target.classList.remove('drag-over');
    const jugId = e.dataTransfer.getData('text/plain');
    const jug = document.getElementById(jugId);
    
    if (jug) {
        jug.classList.add('filling');
        setTimeout(() => jug.classList.remove('filling'), 800);
        
        window.Streamlit.setComponentValue({action: 'fill', jug: jugId === 'jug1' ? 1 : 2});
    }
}

function handleDrainDrop(e) {
    e.preventDefault();
    e.target.classList.remove('drag-over');
    const jugId = e.dataTransfer.getData('text/plain');
    const jug = document.getElementById(jugId);
    
    if (jug) {
        jug.classList.add('emptying');
        setTimeout(() => jug.classList.remove('emptying'), 800);
        
        window.Streamlit.setComponentValue({action: 'empty', jug: jugId === 'jug1' ? 1 : 2});
    }
}

function handleJugDrop(sourceJugId, targetJugId) {
    if (sourceJugId !== targetJugId) {
        const sourceJug = document.getElementById(sourceJugId);
        const targetJug = document.getElementById(targetJugId);
        
        if (sourceJug && targetJug) {
            sourceJug.classList.add('emptying');
            targetJug.classList.add('filling');
            
            setTimeout(() => {
                sourceJug.classList.remove('emptying');
                targetJug.classList.remove('filling');
            }, 800);
            
            window.Streamlit.setComponentValue({
                action: 'transfer',
                from: sourceJugId === 'jug1' ? 1 : 2,
                to: targetJugId === 'jug1' ? 1 : 2
            });
        }
    }
}

document.addEventListener('DOMContentLoaded', initializeGame);
</script>
""", unsafe_allow_html=True)

# Display current state
st.markdown(f"""\n### Current State:
- Jug 1 ({JUG1_CAPACITY}L): {st.session_state.jug1_water}L
- Jug 2 ({JUG2_CAPACITY}L): {st.session_state.jug2_water}L
""")

# Handle drag and drop actions
if st.session_state.get('component_value'):
    action = st.session_state.component_value.get('action')
    if action == 'fill':
        jug = st.session_state.component_value.get('jug')
        if jug == 1:
            st.session_state.jug1_water = JUG1_CAPACITY
        else:
            st.session_state.jug2_water = JUG2_CAPACITY
    elif action == 'empty':
        jug = st.session_state.component_value.get('jug')
        if jug == 1:
            st.session_state.jug1_water = 0
        else:
            st.session_state.jug2_water = 0
    elif action == 'transfer':
        from_jug = st.session_state.component_value.get('from')
        to_jug = st.session_state.component_value.get('to')
        if from_jug == 1 and to_jug == 2:
            transfer = min(st.session_state.jug1_water, JUG2_CAPACITY - st.session_state.jug2_water)
            st.session_state.jug1_water -= transfer
            st.session_state.jug2_water += transfer
        elif from_jug == 2 and to_jug == 1:
            transfer = min(st.session_state.jug2_water, JUG1_CAPACITY - st.session_state.jug1_water)
            st.session_state.jug2_water -= transfer
            st.session_state.jug1_water += transfer
    
    st.session_state.component_value = None
    st.rerun()