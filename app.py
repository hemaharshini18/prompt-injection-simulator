import streamlit as st
from simulator import PromptInjectionSimulator
import pandas as pd
import re

# Set page config with a wider layout
st.set_page_config(
    page_title="Prompt Injection & Jailbreak Defense Simulator",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with modern colors and improved tabs
st.markdown("""
    <style>
    :root {
        --primary-color: #1A1F36;
        --primary-hover: #0D1B2A;
        --secondary-color: #2E2E2E;
        --accent-color: #00B8D4;
        --background-light: #F5F5F5;
        --background-dark: #0D1B2A;
        --text-primary: #2E2E2E;
        --text-secondary: #3B3B3B;
        --success-color: #28A745;
        --error-color: #D72638;
        --warning-color: #FFA500;
        --suspicious-color: #FFD700;
        --ai-color: #6F42C1;
        --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        --transition-ease: all 0.25s ease;
    }
    
    .main {
        padding: 2rem;
        background-color: var(--background-light);
        color: var(--text-primary);
    }
    
    /* Improve the overall layout */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1320px;
    }
    
    /* Enhance tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: none;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        min-width: 180px;
        white-space: pre-wrap;
        background: #EAEAEA;
        border-radius: 12px;
        gap: 0.5rem;
        padding: 1rem 1.5rem;
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 1.05rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: none;
        transition: var(--transition-ease);
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        font-weight: 600;
        box-shadow: var(--card-shadow);
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #DADADA;
        color: var(--primary-color);
        transform: translateY(-2px);
    }
    
    /* Improve buttons */
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: var(--transition-ease);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .stButton>button:hover {
        background-color: var(--primary-hover);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        transform: translateY(-1px);
    }
    
    .stButton>button:active {
        transform: translateY(1px);
    }
    
    /* Improve text areas */
    .stTextArea>div>div>textarea {
        background-color: white;
        border: 1px solid #EAEAEA;
        border-radius: 8px;
        padding: 1rem;
        color: var(--text-primary);
        font-size: 1rem;
        transition: var(--transition-ease);
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 3px rgba(0, 184, 212, 0.1);
    }
    
    /* Improve containers and cards */
    .stExpander {
        border: 1px solid #EAEAEA;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--card-shadow);
        margin-bottom: 1rem;
    }
    
    /* Improve alerts */
    .stAlert {
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: var(--card-shadow);
    }
    
    .stSuccess {
        background-color: rgba(40, 167, 69, 0.1);
        color: var(--success-color);
        border-left: 4px solid var(--success-color);
    }
    
    .stError {
        background-color: rgba(215, 38, 56, 0.1);
        color: var(--error-color);
        border-left: 4px solid var(--error-color);
    }
    
    .stWarning {
        background-color: rgba(255, 165, 0, 0.1);
        color: var(--warning-color);
        border-left: 4px solid var(--warning-color);
    }
    
    /* Improve toggle */
    [data-testid="stToggleButton"] {
        color: var(--text-primary);
    }
    
    /* Improve code blocks */
    .stCodeBlock {
        border-radius: 8px;
        box-shadow: var(--card-shadow);
    }
    
    /* Improve metrics */
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: var(--card-shadow);
    }
    
    .stMetricLabel {
        color: var(--text-secondary);
    }
    
    .stMetricValue {
        color: var(--primary-color);
        font-weight: 600;
    }
    
    /* Improve sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--background-light);
        border-right: 1px solid #EAEAEA;
    }
    
    /* Improve spinners */
    .stSpinner > div {
        border-color: var(--primary-color) transparent transparent transparent;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulator' not in st.session_state:
    st.session_state.simulator = PromptInjectionSimulator()

# Title and description with modern styling
st.markdown("""
    <div style='text-align: center; padding: 2.5rem 2rem; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); border-radius: 12px; margin-bottom: 2rem; box-shadow: var(--card-shadow);'>
        <h1 style='color: white; font-size: 2.5rem; margin-bottom: 1rem; font-weight: 700;'>🔐 Prompt Injection & Jailbreak Defense Simulator</h1>
        <p style='color: rgba(255, 255, 255, 0.9); font-size: 1.2rem; max-width: 800px; margin: 0 auto;'>
            Test and understand how AI models can be protected against prompt injection attacks and jailbreak attempts
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with modern styling
with st.sidebar:
    st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); border-radius: 12px; margin-bottom: 1.5rem; box-shadow: var(--card-shadow);'>
            <h2 style='color: white; margin: 0; font-weight: 600;'>⚙️ Settings</h2>
        </div>
    """, unsafe_allow_html=True)
    
    safe_mode = st.toggle(
        "Safe Mode",
        value=st.session_state.simulator.safe_mode,
        help="Enable additional security checks for suspicious patterns"
    )
    
    if safe_mode:
        st.session_state.simulator.enable_safe_mode()
        st.success("✅ Safe Mode Enabled")
    else:
        st.session_state.simulator.disable_safe_mode()
        st.warning("⚠️ Safe Mode Disabled")
    
    st.markdown("---")
    st.markdown("""
        <div style='padding: 1.5rem; background-color: white; border-radius: 12px; box-shadow: var(--card-shadow);'>
            <h3 style='color: var(--primary-color); margin-bottom: 1rem; font-weight: 600;'>🛡️ About Safe Mode</h3>
            <p style='color: var(--text-secondary);'>Safe Mode adds an extra layer of security by checking for suspicious patterns in prompts before they reach the AI model.</p>
        </div>
    """, unsafe_allow_html=True)

# Main content area with modern tabs
tab1, tab2, tab3 = st.tabs(["🔍 Single Attack Test", "🛠️ Attack Suite", "⚠️ Safe Mode Debug"])

with tab1:
    st.markdown("""
        <div style='padding: 1.5rem; background-color: white; border-radius: 12px; box-shadow: var(--card-shadow); margin-bottom: 1.5rem;'>
            <h2 style='color: var(--primary-color); margin-bottom: 0.5rem; font-weight: 600;'>🔍 Test Individual Attack</h2>
            <p style='color: var(--text-secondary);'>Enter a prompt to test how the system handles potential injection attempts.</p>
        </div>
    """, unsafe_allow_html=True)
    
    attack_prompt = st.text_area(
        "Enter your attack prompt:",
        placeholder="Try to make the AI ignore its instructions or reveal sensitive information...",
        height=150
    )
    
    if st.button("Test Attack", type="primary"):
        if attack_prompt:
            with st.spinner("Testing attack..."):
                success, response = st.session_state.simulator.test_attack(attack_prompt)
                
                # Create a container for the status
                status_container = st.container()
                with status_container:
                    col1, col2 = st.columns(2)
                    with col1:
                        if not success:
                            st.error("🛑 ATTACK BLOCKED")
                            st.markdown("""
                            **Blocking Reason:**
                            - The prompt contains suspicious patterns
                            - Safe Mode is preventing potentially harmful instructions
                            """)
                        else:
                            st.success("🎯 ATTACK ATTEMPTED")
                    with col2:
                        st.metric("Safe Mode", "Enabled" if st.session_state.simulator.safe_mode else "Disabled")
                
                st.markdown("---")
                st.subheader("Response")
                st.markdown("""
                    <div style='padding: 1.5rem; background-color: white; border-radius: 12px; box-shadow: var(--card-shadow); margin-bottom: 1rem;'>
                """, unsafe_allow_html=True)
                if not success:
                    st.warning("⚠️ The attack was blocked before reaching the AI model")
                st.write(response)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter an attack prompt first.")

with tab2:
    st.markdown("""
        <div style='padding: 1.5rem; background-color: white; border-radius: 12px; box-shadow: var(--card-shadow); margin-bottom: 1.5rem;'>
            <h2 style='color: var(--primary-color); margin-bottom: 0.5rem; font-weight: 600;'>🛠️ Predefined Attack Suite</h2>
            <p style='color: var(--text-secondary);'>Run a set of predefined attack attempts to test the system's defenses.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Run Attack Suite", type="primary"):
        with st.spinner("Running attack suite..."):
            results = st.session_state.simulator.run_attack_suite()
            
            # Convert results to DataFrame for better display
            df = pd.DataFrame(results)
            df['success'] = df['success'].map({True: '🎯 Attempted', False: '🛑 Blocked'})
            
            # Display results
            for _, row in df.iterrows():
                with st.expander(f"{row['attack_name']} - {row['success']}"):
                    st.markdown("""
                        <div style='padding: 0.5rem; background-color: #F5F5F5; border-radius: 8px; margin-bottom: 1rem;'>
                    """, unsafe_allow_html=True)
                    st.markdown("**Attack Prompt:**")
                    st.code(row['prompt'])
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("""
                        <div style='padding: 0.5rem; background-color: white; border-radius: 8px;'>
                    """, unsafe_allow_html=True)
                    st.markdown("**Response:**")
                    if row['success'] == '🛑 Blocked':
                        st.error("This attack was blocked by Safe Mode")
                    st.write(row['response'])
                    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("""
        <div style='padding: 1.5rem; background-color: white; border-radius: 12px; box-shadow: var(--card-shadow); margin-bottom: 1.5rem;'>
            <h2 style='color: var(--primary-color); margin-bottom: 0.5rem; font-weight: 600;'>⚠️ Safe Mode Debug</h2>
            <p style='color: var(--text-secondary);'>See exactly how Safe Mode works by checking your input against the risky patterns.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create a container for the debug section
    debug_container = st.container()
    
    with debug_container:
        debug_prompt = st.text_area(
            "Enter a prompt to debug:",
            placeholder="Try entering a prompt with words like 'ignore', 'bypass', 'forget'...",
            height=150
        )
        
        if debug_prompt:
            # Show debug results immediately below the input
            st.markdown("---")
            st.markdown("""
                <h3 style='color: var(--primary-color); margin-bottom: 1rem; font-weight: 600;'>🔬 Pattern Analysis</h3>
            """, unsafe_allow_html=True)
            
            # Track matched patterns
            matched_patterns = []
            
            # Create columns for better layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div style='padding: 1.5rem; background-color: white; border-radius: 12px; box-shadow: var(--card-shadow); height: 100%;'>
                        <h4 style='color: var(--primary-color); margin-bottom: 1rem; font-weight: 600;'>Pattern Matches</h4>
                """, unsafe_allow_html=True)
                for pattern in st.session_state.simulator.risky_patterns:
                    match = re.search(pattern, debug_prompt.lower())
                    if match:
                        st.error(f"❌ Matched: `{pattern}`")
                        st.code(f"Found: '{match.group()}'")
                        matched_patterns.append(pattern)
                    else:
                        st.success(f"✅ No match: `{pattern}`")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div style='padding: 1.5rem; background-color: white; border-radius: 12px; box-shadow: var(--card-shadow); height: 100%;'>
                        <h4 style='color: var(--primary-color); margin-bottom: 1rem; font-weight: 600;'>Overall Result</h4>
                """, unsafe_allow_html=True)
                if st.session_state.simulator._validate_input(debug_prompt):
                    st.success("✅ This prompt would be allowed through")
                else:
                    st.error("❌ This prompt would be blocked by Safe Mode")
                    if matched_patterns:
                        st.markdown("**Blocking Reasons:**")
                        for pattern in matched_patterns:
                            st.markdown(f"- Matched pattern: `{pattern}`")
                st.markdown("</div>", unsafe_allow_html=True)

# Footer with modern styling
st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); border-radius: 12px; margin-top: 2.5rem; box-shadow: var(--card-shadow);'>
        <p style='color: white; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 500;'>Built with 🔒 for AI Security Research</p>
        <p style='color: rgba(255, 255, 255, 0.8); font-size: 0.9rem;'>A tool for testing and understanding AI security measures</p>
    </div>
""", unsafe_allow_html=True) 