import streamlit as st
import pandas as pd
from streamlit_gps_location import gps_location_button
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus.tables import Table, TableStyle

from datetime import datetime
from PIL import Image as PILImage
import tempfile
import os

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Field Research Report",
    layout="centered"
)

st.title("Scientific Field Report")

# ---------------- USER INPUTS ----------------

st.header("Research Information")

researcher = st.text_input("Researcher Name")
title = st.text_input("Discovery Title")

description = st.text_area(
    "Description / Notes",
    height=150
)

# ---------------- GPS LOCATION ----------------

st.header("GPS Location")

location_data = gps_location_button(buttonText="Get my location")

latitude = None
longitude = None

if location_data is not None:

    latitude = location_data.get("latitude")
    longitude = location_data.get("longitude")

    if latitude is not None and longitude is not None:

        st.success("Location captured successfully")

        st.write(f"Latitude: {latitude}")
        st.write(f"Longitude: {longitude}")

        map_data = pd.DataFrame({
            "lat": [latitude],
            "lon": [longitude]
        })

        st.map(map_data)

else:
    st.info("Click the button to capture your location")

# ---------------- PHOTO ----------------

st.header("Visual Evidence")

photo = st.camera_input("Take a photo")

if photo:
    st.image(photo, caption="Captured Evidence")

# ---------------- PDF FUNCTION ----------------

def generate_pdf():

    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(
        pdf_file.name,
        pagesize=letter
    )

    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_paragraph = Paragraph(
        "<b>FIELD RESEARCH REPORT</b>",
        styles["Title"]
    )

    elements.append(title_paragraph)
    elements.append(Spacer(1, 20))

    # Date
    date_text = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Table with researcher data
    data = [
        ["Researcher", researcher],
        ["Date", date_text],
        ["Discovery", title],
        ["Latitude", str(latitude)],
        ["Longitude", str(longitude)]
    ]

    table = Table(data, colWidths=[120, 320])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Description
    elements.append(
        Paragraph(
            f"<b>Observation Notes:</b><br/>{description}",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 20))

    # Add image if uploaded
    if photo is not None:

        image = PILImage.open(photo)

        temp_img = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png"
        )

        image.save(temp_img.name)

        report_image = Image(
            temp_img.name,
            width=250,
            height=250
        )

        elements.append(report_image)

    # Build PDF
    doc.build(elements)

    return pdf_file.name

# ---------------- VALIDATION ----------------

required_fields = [
    researcher,
    title,
    description,
    latitude,
    longitude,
    photo
]

# ---------------- GENERATE REPORT ----------------

st.header("Generate Report")

if st.button("Generate PDF Report", use_container_width=True):

    if all(required_fields):

        pdf_path = generate_pdf()

        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Download Report",
                data=file,
                file_name="field_report.pdf",
                mime="application/pdf"
            )

        st.success("PDF report generated successfully")

    else:
        st.error("Please complete all fields before generating the report")