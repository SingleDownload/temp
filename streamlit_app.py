import streamlit as st
from datetime import datetime

# Initialize session state for MEDICATION_SCHEDULE
if "medication_schedule" not in st.session_state:
    st.session_state.medication_schedule = [
        {"time": "08:00 AM", "medicine": "Aspirin", "pill_taken": False},
        {"time": "02:00 PM", "medicine": "Vitamin D", "pill_taken": False},
        {"time": "08:00 PM", "medicine": "Painkiller", "pill_taken": False},
    ]

# Helper Function: Get current time in 12-hour AM/PM
def current_time_ampm():
    return datetime.now().strftime("%I:%M %p")

# Streamlit UI
st.title("Smart Pillbox Reminder")

# Add or Modify Reminder
st.header("Add or Modify Reminder")
time_input = st.text_input("Set Time (HH:MM AM/PM)")
medicine_input = st.text_input("Medicine Name")

if st.button("Add/Modify Reminder"):
    if not time_input or not medicine_input:
        st.error("Please enter both time and medicine type.")
    else:
        for slot in st.session_state.medication_schedule:
            if slot["time"] == time_input:
                slot["medicine"] = medicine_input
                slot["pill_taken"] = False
                st.success(f"Updated reminder for {time_input} to {medicine_input}.")
                break
        else:
            st.session_state.medication_schedule.append({"time": time_input, "medicine": medicine_input, "pill_taken": False})
            st.success(f"Added new reminder: {medicine_input} at {time_input}.")

# Display Scheduled Reminders
st.header("Scheduled Reminders")
if st.button("Show Reminders"):
    if not st.session_state.medication_schedule:
        st.info("No reminders set.")
    else:
        sorted_schedule = sorted(st.session_state.medication_schedule, key=lambda x: datetime.strptime(x["time"], "%I:%M %p"))
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
        for slot in st.session_state.medication_schedule:
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
    for slot in st.session_state.medication_schedule:
        if slot["time"] == current_time and not slot["pill_taken"]:
            st.warning(f"It's time to take your {slot['medicine']} ({slot['time']}).")
            break
    else:
        st.info(f"No reminders are scheduled for now ({current_time}).")

# Periodic Reminder Check
def periodic_reminder():
    current_time = current_time_ampm()
    for slot in st.session_state.medication_schedule:
        if slot["time"] == current_time and not slot["pill_taken"]:
            st.warning(f"Reminder: It's time to take your {slot['medicine']} ({slot['time']}).")

if st.button("Check for Reminders"):
    periodic_reminder()
