# ... (Keep all your previous setup code) ...

# --- SUBMIT BUTTON ---
st.write("")
if is_open:
    if st.button("Submit Selections", type="primary", use_container_width=True):
        
        # Double check time on server side at moment of click (Safety Net)
        if not global_config["is_active"] or (global_config["end_time"] and time.time() > global_config["end_time"]):
            st.error("⚠️ Submission window closed just now.")
            time.sleep(2)
            st.rerun()
            
        elif user_name == "Select identity..." or not user_email:
            st.error("Name and Email required.")
        elif not final_selections:
            st.error("Select at least one target.")
        else:
            t_mail = user_email.strip().lower()
            if not re.match(r"^[a-z0-9_.+-]+@svarappstech\.com$", t_mail):
                 st.error("Invalid email. Only @svarappstech.com emails are allowed.")
            else:
                is_dup = False
                if t_mail in st.session_state.submitted_emails: is_dup = True
                
                if not is_dup:
                    try:
                        # Added headers to prevent blocking
                        headers = {"User-Agent": "Mozilla/5.0"}
                        df = pd.read_csv(f"{GOOGLE_SHEET_CSV_URL}&t={int(time.time())}", on_bad_lines='skip')
                        if (df.astype(str).apply(lambda x: x.str.strip().str.lower()) == t_mail).any().any():
                            is_dup = True
                    except: pass 
                
                if is_dup:
                    st.error("Already submitted.")
                else:
                    try:
                        payload = {ENTRY_EMAIL: user_email, ENTRY_NAME: user_name, ENTRY_MAGIC: final_selections}
                        
                        # --- FIX: Added Headers and Increased Timeout ---
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                        }
                        
                        response = requests.post(GOOGLE_FORM_URL, data=payload, headers=headers, timeout=10)
                        
                        # Raise error if status is 4xx or 5xx
                        response.raise_for_status() 
                        
                        st.session_state.submitted_emails.add(t_mail)
                        st.session_state.recent_submissions.extend(final_selections)
                        st.session_state.team_select = []
                        st.session_state.success_flag = True 
                        st.rerun() 
                    except requests.exceptions.HTTPError as e:
                        st.error(f"Google rejected the request: {e}")
                    except requests.exceptions.Timeout:
                        st.error("Request timed out. Google Forms is slow, please try again.")
                    except requests.exceptions.ConnectionError:
                        st.error("Connection failed. Check your internet.")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {e}")
else:
    # Disabled State (Visible when Watchdog disables the app)
    st.button("⛔ Submission Closed", disabled=True, use_container_width=True)

# ... (Keep the rest of your dashboard code) ...
