import streamlit as st
import datetime
import time

# ==========================================
# 1. CONFIGURATION & CUSTOMIZATION
# Change these values for your brother!
# ==========================================
BROTHER_NAME = "My Brother" # Used in page title
TARGET_NAME = "Alex"       # What he should type in the name box
TARGET_BDAY = datetime.date(2005, 5, 10) # YYYY, MM, DD

# Page config sets the browser tab title
st.set_page_config(page_title=f"Happy Birthday {BROTHER_NAME}!", page_icon="🎂", layout="centered")

# ==========================================
# 2. CUSTOM CSS (To make it look nicer)
# ==========================================
st.markdown("""
<style>
    /* Center all content */
    .block-container {
        padding-top: 2rem;
        text-align: center;
    }
    /* Style headers */
    h1, h2, h3 {
        text-align: center;
    }
    /* Centered buttons */
    div.stButton > button {
        display: block;
        margin: 0 auto;
    }
    /* Custom fade-in animation class */
    .fade-in {
        animation: fadeIn 2s;
        -webkit-animation: fadeIn 2s;
    }
    @keyframes fadeIn {
        0% {opacity:0;}
        100% {opacity:1;}
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE MANAGEMENT
# This keeps track of where we are in the story
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = "login" # Start at login
if 'magic_number' not in st.session_state:
    st.session_state.magic_number = None

# Helper function to change pages
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# ==========================================
# 4. THE APP LOGIC (PAGE ROUTING)
# ==========================================

# --- STEP 1: LOGIN LOOKING PAGE ---
if st.session_state.page == "login":
    st.title("🔐 Verification Required")
    st.subheader("Please confirm your details to proceed.")
    
    with st.container():
        name = st.text_input("First Name", placeholder="e.g. John")
        nickname = st.text_input("Nickname", placeholder="What do I call you?")
        
        # Address - standard text input
        address = st.text_area("Delivery Address", placeholder="123 Party Ave...")

        # Birthday Input - THIS IS THE TRIGGER
        birth_date = st.date_input(
            "Date of Birth",
            value=None, # Starts empty
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today(),
            help="Type or select your birthday"
        )

        st.markdown("---")
        
        # Logic to check the birthday immediately when entered
        if birth_date is not None:
            if birth_date == TARGET_BDAY:
                # Correct Birthday! Triggers visual effects and moves to next page
                st.balloons()
                st.snow()
                # A brief pause to let them see the effects
                time.sleep(1) 
                go_to_page("burst_in")
            else:
                # Incorrect Birthday
                st.error("⚠️ Details do not match our records. Are you sure...?")
                # Disabled looking button (it does nothing)
                st.button("Sign In (Disabled)", disabled=True)
        else:
            # Button is shown but disabled until date is entered
            st.button("Sign In", disabled=True, help="Enter your birthday first")


# --- STEP 2: THE BURST IN ---
elif st.session_state.page == "burst_in":
    # Wrap content in a div with 'fade-in' CSS class
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    st.title(f"🎉 Hey {TARGET_NAME}! 👋")
    st.header("That's today!!")
    st.subheader("I have a little something for you...")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Simple delay before automatic transition, or a button
    time.sleep(3)
    go_to_page("magic_show_intro")


# --- STEP 3: CURTAINS OPEN / INTRO ---
elif st.session_state.page == "magic_show_intro":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Visualizing 'Curtains Open' with text emojis
    st.title(" 🎭 ⏪ ⏪ ⏩ ⏩ 🎭")
    st.title("Welcome to the Digital Magic Show!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Let's go! ✨"):
        go_to_page("think_number")


# --- STEP 4: THINK OF A NUMBER ---
elif st.session_state.page == "think_number":
    st.header("1️⃣ Think of a number...")
    st.subheader("Any whole number. Keep it in your head.")
    
    # number_input only accepts numbers. value=0 ensures it's not empty.
    num_input = st.number_input("Enter it here just so I can 'read' your mind:", value=0, step=1)
    
    if st.button("Think"):
        st.session_state.magic_number = num_input
        go_to_page("reveal_number")


# --- STEP 5: DRUMROLL & REVEAL ---
elif st.session_state.page == "reveal_number":
    st.markdown("### Was your number...")
    
    # Simulate Slow Animation Drumroll
    status_text = st.empty() # Create a placeholder
    bar = st.progress(0)
    
    # Simple 'drumroll' simulation using progress bar and changing text
    drumroll_sounds = ["🥁 Drrr", "🥁 DrrrRr", "🥁 DRRRRRR", "🥁 TRRRRRRRRUM"]
    for i, sound in enumerate(drumroll_sounds):
        status_text.markdown(f"### {sound}")
        bar.progress((i + 1) * 25)
        time.sleep(0.5)
    
    status_text.empty() # Clear drumroll text
    bar.empty()        # Clear progress bar

    # The Reveal
    st.markdown(f'<h1 style="font-size: 100px; color: #FF4B4B;">{st.session_state.magic_number}</h1>', unsafe_allow_html=True)
    
    if st.button("Yes!! 😱"):
        # This will be where we start Part 2
        st.success("Told you I'm a magician. Let's move to the next trick...")
        # Commented out until code for next page exists:
        # go_to_page("pick_card")
