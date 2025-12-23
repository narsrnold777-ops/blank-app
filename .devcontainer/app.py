import streamlit as st
import sqlite3
from datetime import date

conn = sqlite3.connect("immunization_emr.db", check_same_thread=False)
cursor = conn.cursor()

st.set_page_config(page_title="Immunization EMR", layout="wide")
st.title("🩺 RHU Immunization EMR (Offline)")

menu = st.sidebar.radio(
    "Navigation",
    ["Register Child", "Add Immunization", "View Records"]
)

# ---------------- REGISTER CHILD ----------------
if menu == "Register Child":
    st.subheader("Register Child")

    client_id = st.text_input("Client ID (e.g. IMMU-001)")
    child_name = st.text_input("Child Full Name")
    dob = st.date_input("Date of Birth")
    sex = st.selectbox("Sex", ["Male", "Female"])
    mother = st.text_input("Mother's Name")
    address = st.text_input("Address")
    barangay = st.text_input("Barangay")
    contact = st.text_input("Contact Number")

    if st.button("Save Child"):
        try:
            cursor.execute("""
                INSERT INTO patients
                (client_id, child_name, dob, sex, mother_name, address, barangay, contact)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (client_id, child_name, dob, sex, mother, address, barangay, contact))
            conn.commit()
            st.success("✅ Child registered successfully")
        except:
            st.error("⚠ Client ID already exists")

# ---------------- ADD IMMUNIZATION ----------------
elif menu == "Add Immunization":
    st.subheader("Add Immunization")

    cursor.execute("SELECT client_id, child_name FROM patients")
    patients = cursor.fetchall()

    patient = st.selectbox(
        "Select Child",
        patients,
        format_func=lambda x: f"{x[0]} - {x[1]}"
    )

    vaccine = st.selectbox(
        "Vaccine",
        ["BCG","Hepa B (Birth)","PENTA1","PENTA2","PENTA3",
         "OPV1","OPV2","OPV3","IPV","MCV1","MCV2"]
    )

    dose = st.text_input("Dose (e.g. 1st, 2nd)")
    date_given = st.date_input("Date Given", value=date.today())
    given_by = st.text_input("Given By")
    remarks = st.text_area("Remarks")

    if st.button("Save Immunization"):
        cursor.execute("""
            INSERT INTO immunizations
            (client_id, vaccine, dose, date_given, given_by, remarks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (patient[0], vaccine, dose, date_given, given_by, remarks))
        conn.commit()
        st.success("💉 Immunization saved")

# ---------------- VIEW RECORDS ----------------
elif menu == "View Records":
    st.subheader("Immunization Records")

    cursor.execute("""
        SELECT p.client_id, p.child_name, i.vaccine, i.date_given, i.given_by
        FROM immunizations i
        JOIN patients p ON i.client_id = p.client_id
        ORDER BY i.date_given DESC
    """)
    records = cursor.fetchall()

    st.dataframe(
        records,
        use_container_width=True,
        columns=["Client ID","Child Name","Vaccine","Date Given","Given By"]
    )
