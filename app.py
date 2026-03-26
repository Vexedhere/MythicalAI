import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Database & API Setup (Replace with your actual keys)
SUPABASE_URL = "https://mtczyuzbcunsflvcnatf.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Page Configuration
st.set_page_config(page_title="Mythical Network | Founder Portal", page_icon="💎", layout="wide")

# 3. Sidebar - Branding & Navigation
with st.sidebar:
    st.title("Mythical Studios")
    st.image("https://via.placeholder.com/150", caption="Owner: U. Chethan") # Replace with your logo
    menu = st.radio("Navigation", ["Home", "Store", "Staff Portal", "Support"])
    st.info("Launch Date: April 20, 2026")

# 4. Main Pages
if menu == "Home":
    st.header("Welcome to the Mythical Network 🛡️")
    st.write("The ultimate Minecraft experience is coming soon.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Server Status", value="Development", delta="75% Complete")
    with col2:
        st.metric(label="Registered Players", value="142", delta="+12 today")

elif menu == "Store":
    st.header("Mythical Store 💎")
    st.subheader("Support the server and get rewards")
    
    items = [
        {"name": "VIP Rank", "price": "₹500", "features": "Fly, Color Chat, Kits"},
        {"name": "MVP Rank", "price": "₹1000", "features": "All VIP + Custom Prefix"},
        {"name": "Unban Pass", "price": "₹200", "features": "One-time Second Chance"}
    ]
    
    for item in items:
        with st.expander(f"{item['name']} - {item['price']}"):
            st.write(f"**Features:** {item['features']}")
            if st.button(f"Buy {item['name']}", key=item['name']):
                # UPI QR Code Generation Logic
                upi_id = "yourname@upi" # Replace with your UPI
                upi_url = f"upi://pay?pa={upi_id}&pn=U.Chethan&am={item['price'].replace('₹','')}&cu=INR"
                st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={upi_url}", caption="Scan to Pay via UPI")
                st.warning("Please upload a screenshot of your payment below.")
                st.file_uploader("Upload Receipt")

elif menu == "Staff Portal":
    st.header("Staff Management 🛠️")
    st.write("Login required to access player logs.")
    # Add your Supabase Auth logic here

# 5. Footer
st.markdown("---")
st.caption("© 2026 Mythical Studios | Built by U. Chethan")