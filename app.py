import streamlit as st
import pandas as pd
import datetime
import os

# === Your contact info (edit these) ===
LINKEDIN_URL = "https://www.linkedin.com/in/mohamed-mahmoud"
EMAIL = "mohamed.mahmoud@email.com"

# --- Page Config ---
st.set_page_config(page_title="🎓 Data Analysis Final Projects Showcase", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    .hero {
        text-align:center; padding: 3rem 1rem;
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        border-radius: 0 0 24px 24px;
        color: white; margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .hero h1 { font-size: 2.8rem; font-weight: 800; margin-bottom: 0.5rem; }
    .hero p { font-size: 1.2rem; opacity: 0.9; }
    .card {
        background:white; border-radius:16px; padding:1rem;
        margin-bottom:1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.25s ease-in-out;
        min-height: 460px; display: flex; flex-direction: column;
    }
    .card:hover { transform: translateY(-6px); box-shadow: 0 8px 18px rgba(0,0,0,0.15); }
    .card img.project-img {
        width:100%; border-radius:12px; height:180px; object-fit:cover;
    }
    .card h3 { margin-top:0.8rem; font-size:1.25rem; font-weight:600; color:#222; }
    .card p { color:#444; font-size:0.95rem; line-height:1.4; flex-grow: 1; }
    .project-btn {
        display:inline-block; padding:0.6rem 1rem; background:#2575fc; color:white !important;
        border-radius:10px; text-decoration:none; font-size:0.95rem;
        transition: background 0.2s ease; margin-top:auto; text-align:center;
    }
    .project-btn:hover { background:#1a5ed8; }
    .avatars { display:flex; align-items:center; margin:0.6rem 0; gap:6px; }
    .avatars img {
        width:40px; height:40px; border-radius:50%; object-fit:cover; border:2px solid #eee;
    }
    .footer {
        margin-top: 50px; padding: 20px; text-align: center;
        font-family: 'Inter', sans-serif; color: #555; font-size: 14px;
        border-top: 1px solid #eaeaea;
    }
    .footer h4 { margin: 5px 0; font-size: 18px; font-weight: 600; color: #333; }
    .footer p { margin: 5px 0 15px; font-size: 14px; color: #777; }
    .footer-links a {
        margin: 0 10px; text-decoration: none; font-size: 14px;
        color: #0077b5; font-weight: 500;
    }
    .footer-links a:hover { text-decoration: underline; }
    .footer-meta { margin-top: 15px; font-size: 12px; color: #999; }
    </style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown(
    """
    <div class="hero">
        <h1>🎓 Data Analysis Final Projects Showcase</h1>
        <p>Explore the amazing work of our talented students.</p>
        <p style="margin-top:1rem; font-size:1rem; font-weight:500; opacity:0.95;">
            Supervised by <b>Mohamed Mahmoud</b> (Instructor)
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("projects.csv")

df = load_data()

# --- Search Bar ---
query = st.text_input("🔍 Search by team name, member, or keywords").lower()
if query:
    filtered_df = df[df.apply(lambda row: query in str(row.Team).lower() 
                                         or query in str(row.Member).lower() 
                                         or query in str(row.Description).lower(), axis=1)]
else:
    filtered_df = df

# --- Display Projects (3 per row) ---
cols_per_row = 3
for i in range(0, len(filtered_df), cols_per_row):
    row_data = filtered_df.iloc[i:i+cols_per_row]
    cols = st.columns(cols_per_row)
    for col, (_, row) in zip(cols, row_data.iterrows()):
        with col:
            proj_img_path = str(row["Image"])
            print(proj_img_path)
            # Member Avatars HTML
            member_imgs_html = ""
            member_images = str(row.get("MemberImages", "")).split(",")
            if member_images and member_images[0] != "nan":
                for img in member_images:
                    img_path = img
                    member_imgs_html += f'<img src="{img_path}" alt="member"/>'

            # Card HTML
            card_html = f"""
            <div class="card">
                <img src="{proj_img_path}" class="project-img" alt="{row['Team']}">
                <h3>{row['Team']}</h3>
                <p><b>Members:</b> {row['Member']}</p>
                <div class="avatars">{member_imgs_html}</div>
                <p>{row['Description']}</p>
                <a href="{row['Link']}" target="_blank" class="project-btn">🔗 View Project</a>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

# --- Footer ---
footer_html = f"""
<div class="footer">
    <h4>Mohamed Mahmoud</h4>
    <p>Instructor & Mentor • Data Engineering & AI Specialist</p>
    <p>
        <a href="{LINKEDIN_URL}" target="_blank">🔗 LinkedIn</a>
        <a href="mailto:{EMAIL}">✉️ Email</a>
    </p>
    <div class="footer-meta">
        © {datetime.datetime.now().year} Mohamed Mahmoud. All rights reserved. | 
        Academic Year {datetime.datetime.now().year}-{datetime.datetime.now().year+1} | 
        Generated on {datetime.datetime.now().strftime("%d/%m/%Y")}
    </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
