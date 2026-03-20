import streamlit as st
import datetime
import time

# ==========================================
# 1. CONFIGURATION & CUSTOMIZATION
# ==========================================
BROTHER_NAME = "My Brother" 
TARGET_NAME = "Alex"       
TARGET_BDAY = datetime.date(2005, 5, 10) 

st.set_page_config(page_title=f"Happy Birthday {BROTHER_NAME}!", page_icon="🎂", layout="centered")

# ==========================================
# 2. CUSTOM CSS
# ==========================================
st.markdown("""
<style>
    .block-container { padding-top: 2rem; text-align: center; }
    h1, h2, h3 { text-align: center; }
    div.stButton > button { display: block; margin: 0 auto; }
    .fade-in { animation: fadeIn 2s; -webkit-animation: fadeIn 2s; }
    @keyframes fadeIn { 0% {opacity:0;} 100% {opacity:1;} }
    
    /* Big card reveal styling */
    .big-card {
        font-size: 60px;
        padding: 40px;
        border-radius: 15px;
        border: 2px solid #ccc;
        background-color: white;
        color: black;
        display: inline-block;
        margin-top: 20px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE MANAGEMENT
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'magic_number' not in st.session_state:
    st.session_state.magic_number = None
if 'picked_card' not in st.session_state:
    st.session_state.picked_card = None
if 'shuffle_count' not in st.session_state:
    st.session_state.shuffle_count = 0

def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# ==========================================
# 4. THE APP LOGIC (PAGE ROUTING)
# ==========================================

# --- STEP 1: LOGIN ---
if st.session_state.page == "login":
    st.title("🔐 Verification Required")
    st.subheader("Please confirm your details to proceed.")
    with st.container():
        name = st.text_input("First Name", placeholder="e.g. John")
        nickname = st.text_input("Nickname", placeholder="What do I call you?")
        address = st.text_area("Delivery Address", placeholder="123 Party Ave...")
        birth_date = st.date_input("Date of Birth", value=None, min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        st.markdown("---")
        
        if birth_date is not None:
            if birth_date == TARGET_BDAY:
                st.balloons()
                st.snow()
                time.sleep(1) 
                go_to_page("burst_in")
            else:
                st.error("⚠️ Details do not match our records. Are you sure...?")
                st.button("Sign In (Disabled)", disabled=True)
        else:
            st.button("Sign In", disabled=True)

# --- STEP 2: BURST IN ---
elif st.session_state.page == "burst_in":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title(f"🎉 Hey {TARGET_NAME}! 👋")
    st.header("That's today!!")
    st.subheader("I have a little something for you...")
    st.markdown('</div>', unsafe_allow_html=True)
    time.sleep(3)
    go_to_page("magic_show_intro")

# --- STEP 3: CURTAINS OPEN ---
elif st.session_state.page == "magic_show_intro":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title(" 🎭 ⏪ ⏪ ⏩ ⏩ 🎭")
    st.title("Welcome to the Digital Magic Show!")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Let's go! ✨"):
        go_to_page("think_number")

# --- STEP 4 & 5: THINK OF A NUMBER ---
elif st.session_state.page == "think_number":
    st.header("1️⃣ Think of a number...")
    num_input = st.number_input("Enter it here just so I can 'read' your mind:", value=0, step=1)
    if st.button("Think 🧠"):
        st.session_state.magic_number = num_input
        go_to_page("reveal_number")

elif st.session_state.page == "reveal_number":
    st.markdown("### Was your number...")
    status_text = st.empty()
    bar = st.progress(0)
    drumroll_sounds = ["🥁 Drrr", "🥁 DrrrRr", "🥁 DRRRRRR", "🥁 TRRRRRRRRUM"]
    for i, sound in enumerate(drumroll_sounds):
        status_text.markdown(f"### {sound}")
        bar.progress((i + 1) * 25)
        time.sleep(0.5)
    
    status_text.empty()
    bar.empty()
    st.markdown(f'<h1 style="font-size: 100px; color: #FF4B4B;">{st.session_state.magic_number}</h1>', unsafe_allow_html=True)
    
    if st.button("Yes!! 😱"):
        go_to_page("pick_card") # <-- Link to the new page!

# --- STEP 6: PICK A CARD ---
elif st.session_state.page == "pick_card":
    st.header("🃏 Trick #2: Pick Any Card")
    st.write("Lock in your choice below.")
    
    col1, col2 = st.columns(2)
    with col1:
        card_value = st.selectbox("Value", ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"])
    with col2:
        card_suit = st.selectbox("Suit", ["Hearts ♥️", "Diamonds ♦️", "Clubs ♣️", "Spades ♠️"])
    
    st.markdown(f"### You are picking: **{card_value} of {card_suit}**")
    
    if st.button("Pick this card! 🔒"):
        st.session_state.picked_card = f"{card_value} of {card_suit}"
        go_to_page("shuffle_cards")

# --- STEP 7 & 8: SHUFFLE CARDS ---
elif st.session_state.page == "shuffle_cards":
    st.header("Let's mix them up.")
    st.write("The cards are face down. Click the button below to shuffle them. Do it as many times as you want to make sure I don't know where it is!")
    
    # Mash-to-shuffle mechanic
    if st.button("🔀 Shuffle Cards", use_container_width=True):
        st.session_state.shuffle_count += 1
        st.toast("Shk shk shk... 🎴", icon="💨") # Little pop-up notification
    
    st.write(f"*You have shuffled {st.session_state.shuffle_count} times.*")
    
    st.markdown("---")
    if st.button("I'm done, reveal my card!"):
        go_to_page("reveal_card")

# --- STEP 9: CARD REVEAL ---
elif st.session_state.page == "reveal_card":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.markdown("### Was your card...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Drumroll
    status_text = st.empty()
    bar = st.progress(0)
    for i in range(4):
        status_text.markdown(f"### 🥁 {'...' * (i+1)}")
        bar.progress((i + 1) * 25)
        time.sleep(0.5)
    
    status_text.empty()
    bar.empty()

    # Determine color of text based on suit
    color = "red" if "♥️" in st.session_state.picked_card or "♦️" in st.session_state.picked_card else "black"
    
    # The Reveal using custom CSS class
    st.markdown(f'<div class="big-card" style="color: {color};">{st.session_state.picked_card}</div>', unsafe_allow_html=True)
    
    st.write("") # Spacer
    if st.button("Next Trick... 🪄"):
        st.success("Moving to the next stage...")
        # go_to_page("tablecloth_trick") # Coming up next!
