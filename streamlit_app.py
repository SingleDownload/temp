import streamlit as st
from datetime import datetime, timedelta

# Initial Schedule and Medicine Data
if "MEDICATION_SCHEDULE" not in st.session_state:
    st.session_state.MEDICATION_SCHEDULE = [
        {"time": "08:00 AM", "medicine": "Aspirin", "pill_taken": False},
        {"time": "02:00 PM", "medicine": "Vitamin D", "pill_taken": False},
        {"time": "08:00 PM", "medicine": "Painkiller", "pill_taken": False},
    ]

# Helper Function: Get current time in 12-hour AM/PM
def current_time_ampm():
    return datetime.now().strftime("%I:%M %p")

# Helper Function: Get upcoming reminder within 1 minute
def get_upcoming_reminder():
    current_time = datetime.now()
    for slot in st.session_state.MEDICATION_SCHEDULE:
        reminder_time = datetime.strptime(slot["time"], "%I:%M %p")
        if current_time <= reminder_time <= current_time + timedelta(minutes=1) and not slot["pill_taken"]:
            return slot
    return None

# Streamlit UI
st.title("Smart Pillbox Reminder")

# Display Upcoming Reminder
upcoming_reminder = get_upcoming_reminder()
if upcoming_reminder:
    st.markdown(f"<div style='color: red; font-weight: bold;'>Reminder: It's almost time to take your {upcoming_reminder['medicine']} at {upcoming_reminder['time']}!</div>", unsafe_allow_html=True)

# Add or Modify Reminder
st.header("Add or Modify Reminder")
time_input = st.text_input("Set Time (HH:MM AM/PM)")
medicine_input = st.text_input("Medicine Name")

if st.button("Add/Modify Reminder"):
    if not time_input or not medicine_input:
        st.error("Please enter both time and medicine type.")
    else:
        # Check if the reminder already exists, and update it if so
        for slot in st.session_state.MEDICATION_SCHEDULE:
            if slot["time"] == time_input:
                slot["medicine"] = medicine_input
                slot["pill_taken"] = False
                st.success(f"Updated reminder for {time_input} to {medicine_input}.")
                break
        else:
            # Add new reminder if not found
            st.session_state.MEDICATION_SCHEDULE.append({"time": time_input, "medicine": medicine_input, "pill_taken": False})
            st.success(f"Added new reminder: {medicine_input} at {time_input}.")

# Display Scheduled Reminders
st.header("Scheduled Reminders")
if st.button("Show Reminders"):
    if not st.session_state.MEDICATION_SCHEDULE:
        st.info("No reminders set.")
    else:
        sorted_schedule = sorted(st.session_state.MEDICATION_SCHEDULE, key=lambda x: datetime.strptime(x["time"], "%I:%M %p"))
        for slot in sorted_schedule:
            status = "Taken" if slot["pill_taken"] else "Pending"
            st.write(f"- {slot['time']}: {slot['medicine']} ({status})")

# Simulate Pillbox Actions
st.header("Pillbox Actions")
if st.button("Open Pillbox"):
    st.session_state.pillbox_open = True
    st.success("Pillbox is now open.")

if st.button("Close Pillbox"):
    st.session_state.pillbox_open = False
    st.success("Pillbox is now closed.")

if st.button("Pill Taken"):
    if not st.session_state.get("pillbox_open", False):
        st.error("Open the pillbox to take the pill!")
    else:
        current_time = current_time_ampm()
        for slot in st.session_state.MEDICATION_SCHEDULE:
            if slot["time"] == current_time and not slot["pill_taken"]:
                slot["pill_taken"] = True
                st.success(f"You have taken your {slot['medicine']}.")
                break
        else:
            st.warning("No medication is scheduled for this time.")

# Test Reminder
st.header("Test Reminder")
if st.button("Test Reminder"):
    current_time = current_time_ampm()
    for slot in st.session_state.MEDICATION_SCHEDULE:
        if slot["time"] == current_time and not slot["pill_taken"]:
            st.warning(f"It's time to take your {slot['medicine']} ({slot['time']}).")
            break
    else:
        st.info(f"No reminders are scheduled for now ({current_time}).")
