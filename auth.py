import hashlib
import streamlit as st
from database import init_db, get_user, is_expired, extend_expiry

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_page():
    init_db()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""

    if st.session_state.logged_in:
        email = st.session_state.user_email
        if is_expired(email):
            user = get_user(email)
            if user and user[5] == 0:
                st.warning("Trial expired — Submit feedback to extend 15 more days")
                feedback = st.text_area("Your Feedback")
                if st.button("Submit Feedback"):
                    if feedback.strip():
                        extend_expiry(email)
                        st.success("Thank you! Access extended by 15 days.")
                        st.rerun()
                    else:
                        st.error("Please enter your feedback before submitting.")
            else:
                st.error("Trial period has ended.")
                st.info("Contact us: triplebot.official@gmail.com")
            return False
        return True

    st.title("Triple Bot V5")
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user(email)
        if user and user[2] == hash_password(password):
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
        else:
            st.error("Invalid email or password.")
            st.info("Request access: triplebot.official@gmail.com")

    return False