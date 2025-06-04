# app.py

import streamlit as st
import re
from fpdf import FPDF
import base64

# ─────────────────────────────────────────────────────────────────────────────
#  (A) PAGE CONFIGURATION & GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Creation and Report",
    layout="wide",
    initial_sidebar_state="auto",
)

# Force a light background (even if user’s theme is dark)
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] {
        background-color: #f2f2f2 !important;
    }
    header[data-testid="stHeader"],
    div[data-testid="stToolbar"] {
        background-color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Global CSS (sidebar, cards, posts, profile page tweaks, etc.)
st.markdown(
    """
    <style>
    /* ─── Sidebar Styling ───────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        padding-top: 1rem;
    }
    .sidebar-logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 120px;
    }
    .sidebar-user {
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    .sidebar-user-name {
        font-weight: bold;
        font-size: 1.0rem;
        color: #333333;
        margin: 0;
    }
    .sidebar-user-email {
        font-size: 0.9rem;
        color: #555555;
        margin: 0;
    }
    .sidebar-upgrade button {
        background-color: #003366;
        color: white;
        width: 90%;
        margin: 0.5rem 5% 1rem 5%;
        padding: 0.5rem 0;
        border: none;
        border-radius: 0.25rem;
        font-size: 1rem;
        cursor: pointer;
    }
    .sidebar-upgrade button:hover {
        background-color: #002244;
    }
    .sidebar-menu-heading {
        font-size: 0.9rem;
        color: #333333;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        padding-left: 1rem;
    }
    .sidebar-menu-item {
        background-color: #ffffff;
        border-radius: 0.25rem;
        padding: 0.4rem 0.6rem;
        margin: 0.3rem 1rem;
        display: flex;
        align-items: center;
        cursor: pointer;
    }
    .sidebar-menu-item:hover {
        background-color: #e6e6e6;
    }
    .menu-icon {
        margin-right: 0.5rem;
    }
    .menu-item-text {
        color: #333333;
        font-size: 1rem;
    }

    /* ─── Main Header ────────────────────────────────────────────────────────── */
    .main-header {
        padding: 1rem 0 0 1rem;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
        color: #333333;
    }
    .main-subheader {
        font-size: 0.9rem;
        color: #666666;
        margin-top: 0.25rem;
        margin-left: 1rem;
    }

    /* ─── Metric Cards ───────────────────────────────────────────────────────── */
    .metric-card {
        border-radius: 0.25rem;
        margin-bottom: 1rem;
        padding: 1rem;
        font-weight: bold;
    }
    .metric-card .label {
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }
    .metric-card .value {
        font-size: 2rem;
    }
    .card-students {
        background-color: #005a80;
        color: white;
    }
    .card-teachers {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #d9d9d9;
    }

    /* ─── Post Card Styling ──────────────────────────────────────────────────── */
    .post-card {
        border: 1px solid #cccccc;
        border-radius: 0.25rem;
        margin: 1rem;
        padding: 1rem;
        background-color: #ffffff;
    }
    .post-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .post-header-left {
        display: flex;
        align-items: center;
    }
    .post-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 0.75rem;
        background-color: #e0e0e0; /* placeholder gray */
    }
    .post-author {
        font-weight: bold;
        color: #333333;
        margin: 0;
    }
    .post-school {
        font-size: 0.85rem;
        color: #555555;
        margin: 0;
    }
    .post-timestamp {
        font-size: 0.75rem;
        color: #777777;
    }
    .post-status {
        color: #28a745; /* green */
        font-weight: bold;
        font-size: 0.9rem;
    }
    .post-title {
        font-weight: bold;
        margin: 0.5rem 0 0.25rem 0;
        font-size: 1rem;
        color: #333333;
    }
    .post-body {
        margin: 0 0 0.75rem 0;
        color: #333333;
        font-size: 0.95rem;
    }
    .post-engagement {
        display: flex;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    .engagement-button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 0.25rem;
        padding: 0.3rem 0.75rem;
        font-size: 0.85rem;
        margin-right: 0.5rem;
        cursor: pointer;
    }
    .engagement-button.comment,
    .engagement-button.share {
        background-color: #6c757d;
    }
    .engagement-button:hover {
        opacity: 0.9;
    }
    .comment-input {
        display: flex;
        align-items: center;
        margin-top: 0.5rem;
    }
    .comment-input input {
        flex: 1;
        padding: 0.5rem;
        border: 1px solid #cccccc;
        border-radius: 0.25rem;
        font-size: 0.9rem;
        margin-right: 0.5rem;
    }
    .comment-input button {
        background-color: transparent;
        border: none;
        font-size: 1.2rem;
        color: #007bff;
        cursor: pointer;
    }

    /* ─── Profile Page Styling ──────────────────────────────────────────────── */
    .profile-title {
        margin-top: 1rem;
        margin-left: 1rem;
        font-size: 2rem;
        font-weight: bold;
        color: #000000; /* explicitly black */
    }
    .profile-section {
        margin: 1rem 1rem 0 1rem;
    }
    .bio-container {
        background-color: #f9f9f9;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 1rem;
    }
    .bio-container h3 {
        margin: 0 0 0.5rem 0;
        color: #333333;
    }
    .bio-container p {
        margin: 0;
        color: #555555;
        font-size: 0.95rem;
    }
    .profile-recent-post {
        border: 1px solid #cccccc;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem;
        background-color: #ffffff;
    }
    .edit-avatar-preview {
        border-radius: 50%;
        width: 100px;
        height: 100px;
        object-fit: cover;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
#  (B) FAKE PROFILE & DUMMY POSTS
# ─────────────────────────────────────────────────────────────────────────────
fake_student = {
    "student_id": 1,
    "name": "Akshay",
    "email": "akshay@siliconvalley4u.com",
    "school": "Siliconvalley4u",
}

dummy_posts = [
    {
        "author": "Akshay",
        "school": "Siliconvalley4u",
        "relative_time": "2 days ago",
        "title": "Exploring Pandas DataFrames",
        "body": "🛠 Today I dove into pandas DataFrame operations—filtering, grouping, and merging. Powerful for data analysis! #Pandas #DataScience",
        "likes": 14,
        "comments": 2,
    },
    {
        "author": "Akshay",
        "school": "Siliconvalley4u",
        "relative_time": "1 week ago",
        "title": "Object-Oriented Python",
        "body": "🔄 Practiced OOP in Python: classes, inheritance, and polymorphism. Built a small game demo! #Python #OOP",
        "likes": 10,
        "comments": 3,
    },
    {
        "author": "Akshay",
        "school": "Siliconvalley4u",
        "relative_time": "3 weeks ago",
        "title": "Building a Streamlit App",
        "body": "💻 Developed a Streamlit dashboard to visualize student progress. Added charts and custom CSS! #Streamlit #Dashboard",
        "likes": 12,
        "comments": 4,
    },
    {
        "author": "Priya",
        "school": "Siliconvalley4u",
        "relative_time": "5 days ago",
        "title": "Data Cleaning Tips",
        "body": "🧹 Learned advanced data cleaning techniques—handling missing values and outliers in pandas. #DataCleaning",
        "likes": 8,
        "comments": 2,
    },
    {
        "author": "Sam",
        "school": "India Community Center ICC",
        "relative_time": "2 weeks ago",
        "title": "Test post 250601a",
        "body": "Test post for ICC camp 250601a",
        "likes": 0,
        "comments": 0,
    },
]

# ─────────────────────────────────────────────────────────────────────────────
#  (C) SIDEBAR CONTENT
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<img src="logo.png" class="sidebar-logo" />', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="sidebar-user">
            <p class="sidebar-user-name">Akshay</p>
            <p class="sidebar-user-email">akshay@siliconvalley4u.com</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-upgrade"><button>Upgrade</button></div>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-menu-heading">Main Menu</p>', unsafe_allow_html=True)

    if "selected_menu" not in st.session_state:
        st.session_state["selected_menu"] = "Dashboard"
    if "uploaded_avatar" not in st.session_state:
        st.session_state["uploaded_avatar"] = None
    if "editing_profile" not in st.session_state:
        st.session_state["editing_profile"] = False
    if "profile_bio" not in st.session_state:
        st.session_state["profile_bio"] = (
            "Passionate learner with a love for programming and data science.\n"
            "Enjoys building interactive dashboards and exploring new technologies."
        )
    if "show_profile_report" not in st.session_state:
        st.session_state["show_profile_report"] = False

    def select_menu(item_name):
        st.session_state["selected_menu"] = item_name

    if st.button("🏠  Post", key="btn_post"):
        select_menu("Dashboard")
    if st.button("👤  Profile", key="btn_profile"):
        select_menu("Profile")
    if st.button("⚙️  Settings", key="btn_settings"):
        select_menu("Settings")
    if st.button("🚪  Sign out", key="btn_signout"):
        select_menu("Sign out")

# ─────────────────────────────────────────────────────────────────────────────
#  (D) MAIN AREA: ROUTING BASED ON MENU SELECTION
# ─────────────────────────────────────────────────────────────────────────────
selected_menu = st.session_state["selected_menu"]

if selected_menu == "Dashboard":
    st.markdown('<div class="main-header"><h1>Siliconvalley4u</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subheader">2603 Camino Samon #200, San Ramon, CA 94583</div>', unsafe_allow_html=True)

    cols = st.columns(2, gap="small")
    with cols[0]:
        total_students = 50
        st.markdown(
            f"""
            <div class="metric-card card-students">
                <div class="label">Total Students</div>
                <div class="value">{total_students}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        total_teachers = 5
        st.markdown(
            f"""
            <div class="metric-card card-teachers">
                <div class="label">Total Teachers</div>
                <div class="value">{total_teachers}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    for post in dummy_posts:
        author = post["author"]
        school = post["school"]
        rel_time = post["relative_time"]
        title = post["title"]
        body = post["body"]
        likes = post["likes"]
        comments = post["comments"]

        st.markdown(
            f"""
            <div class="post-card">
              <!-- Post Header -->
              <div class="post-header">
                <div class="post-header-left">
                  <div class="post-avatar"></div>
                  <div>
                    <p class="post-author">{author}</p>
                    <p class="post-school">{school}</p>
                    <p class="post-timestamp">{rel_time}</p>
                  </div>
                </div>
                <div class="post-status">Approved</div>
              </div>

              <!-- Title & Body -->
              <p class="post-title">{title}</p>
              <p class="post-body">{body}</p>

              <!-- Engagement Buttons -->
              <div class="post-engagement">
                <button class="engagement-button">👍 {likes} Likes</button>
                <button class="engagement-button comment">💬 {comments} Comments</button>
                <button class="engagement-button share">↗️ Share</button>
              </div>

              <!-- Comment Input -->
              <div class="comment-input">
                <input type="text" placeholder="Add a comment…" disabled />
                <button>➤</button>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

elif selected_menu == "Profile":
    student = fake_student

    # (1) Profile header in explicit black
    st.markdown(f"<div class='profile-title'>Profile</div>", unsafe_allow_html=True)

    # (2) Buttons: Edit Profile / Generate Progress Report
    col_title, col_buttons = st.columns([3, 1])
    with col_buttons:
        st.write("")  # a little vertical spacing
        edit_clicked = st.button("Edit Profile", key="btn_edit_profile", help="Modify your profile information")
        gen_clicked = st.button(
            "Generate Progress Report", key="btn_generate_profile_report", help="View and download your progress"
        )

    # (3) “Edit Profile” UI
    if edit_clicked:
        st.session_state["editing_profile"] = True

    if st.session_state["editing_profile"]:
        uploaded_file = st.file_uploader("Upload new profile picture:", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.session_state["uploaded_avatar"] = uploaded_file

        new_bio = st.text_area("Bio", value=st.session_state["profile_bio"], height=70)
        if st.button("Save Profile", key="btn_save_profile"):
            st.session_state["profile_bio"] = new_bio
            st.session_state["editing_profile"] = False
            st.success("Profile updated!")

    # (4) Profile Info & Bio
    col1, col2 = st.columns([2, 1], gap="small")

    with col1:
        # Avatar
        if st.session_state["uploaded_avatar"] is not None:
            avatar_bytes = st.session_state["uploaded_avatar"].read()
            st.image(avatar_bytes, width=100, use_column_width=False)
        else:
            st.markdown(
                '<div style="text-align:center"><img src="avatar.png" width="100" style="border-radius:50%" /></div>',
                unsafe_allow_html=True,
            )

        # Name & Email
        st.markdown(
            f"<p style='margin:0; font-weight:bold; font-size:1.1rem; color:#000000;'>{student['name']}</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='margin:0; color:#555555; font-size:0.95rem;'>{student['email']}</p>",
            unsafe_allow_html=True,
        )

        # Bio
        st.markdown(
            f'<div class="bio-container"><h3>Bio</h3><p>{st.session_state["profile_bio"]}</p></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.write("")  # spacing above dropdown
        st.selectbox(
            label="School",
            options=["-- Choose a School --", "Siliconvalley4u", "India Community Center ICC"],
            index=1,
            key="profile_school",
        )

    # (5) Recent Posts by this user
    st.markdown("<div class='profile-section'>2 Weeks Ago</div>", unsafe_allow_html=True)
    user_posts = [p for p in dummy_posts if p["author"] == student["name"]]
    if not user_posts:
        st.info("No recent posts to display.")
    else:
        for post in user_posts[:3]:
            rel_time = post["relative_time"]
            title = post["title"]
            body = post["body"]
            likes = post["likes"]
            comments = post["comments"]
            st.markdown(
                f"""
                <div class="profile-recent-post">
                  <div class="post-header" style="margin-bottom:0.5rem;">
                    <div class="post-header-left">
                      <div class="post-avatar"></div>
                      <div>
                        <p class="post-author" style="margin:0; color:#000000; font-weight:bold;">{student['name']}</p>
                        <p class="post-school" style="margin:0; color:#555555; font-size:0.85rem;">{post['school']}</p>
                        <p class="post-timestamp" style="margin:0; color:#777777; font-size:0.75rem;">{rel_time}</p>
                      </div>
                    </div>
                    <div class="post-status" style="color:#28a745; font-weight:bold; font-size:0.9rem;">Approved</div>
                  </div>
                  <p class="post-title" style="margin:0.3rem 0; font-weight:bold; color:#333333;">{title}</p>
                  <p class="post-body" style="margin:0 0 0.75rem 0; color:#333333;">{body}</p>
                  <div class="post-engagement">
                    <button class="engagement-button">👍 {likes} Likes</button>
                    <button class="engagement-button comment">💬 {comments} Comments</button>
                    <button class="engagement-button share">↗️ Share</button>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ─────────────────────────────────────────────────────────────────────────
    # (6) Generate Progress Report: show as a white “card” with black text
    #     and a Download button, no pink tab / no expander
    # ─────────────────────────────────────────────────────────────────────────
    if gen_clicked:
        st.session_state["show_profile_report"] = True

    if st.session_state["show_profile_report"]:
        # (6a) Original HTML snippet stored in html_block
        html_block = """
<h3>1. Notable Wins</h3>
<p>You’ve mastered Python (pandas, OOP) in real-world settings and shine both as an instructor and CS undergrad—your enthusiasm in demos and projects speaks volumes.</p>

<h3>2. Strategic Growth Areas</h3>
<ul>
  <li>Diversify your toolkit with R or SQL to tackle broader data challenges.</li>
  <li>Hone project leadership by learning Agile fundamentals and Gantt chart planning.</li>
  <li>Strengthen financial know-how: budgeting basics and smart saving strategies.</li>
</ul>

<h3>3. Targeted Learning Plan</h3>
<ul>
  <li><strong>Finance Data 1A:</strong> Decode financial algorithms and risk metrics.</li>
  <li><strong>Gantt Level 1A:</strong> Plan and monitor projects like a pro.</li>
  <li><strong>Python Level 2A:</strong> Master advanced data structures and performance tuning.</li>
</ul>

<h3>4. Action Steps</h3>
<ul>
  <li>Enroll in courses within two weeks and set clear weekly goals (e.g., finish two Finance Data 1A modules by Friday).</li>
  <li>Review progress every Sunday—tweak your plan to stay on track.</li>
</ul>

<h3>5. Leverage Nexclap</h3>
<ul>
  <li>Post key milestones to document growth and inspire peers.</li>
  <li>Upload standout code samples or mini-projects to showcase your skills.</li>
  <li>Share concise insights (e.g., “Optimizing pandas workflows”) to build your personal brand.</li>
</ul>

<h3>6. Quick Finance Hacks</h3>
<ul>
  <li>Use a simple budget app (Mint/YNAB) and automate small savings toward a specific goal.</li>
  <li>Audit spending weekly to identify and cut low-value expenses.</li>
</ul>

<h3>7. Wellness Essentials</h3>
<ul>
  <li>Join a local soccer game or pickup match to boost fitness and teamwork.</li>
  <li>Commit 10–15 minutes daily to stretching or yoga for flexibility and focus.</li>
  <li>Practice 5–10 minutes of mindfulness each morning to sharpen concentration and relieve stress.</li>
</ul>
"""

        # (6b) Strip out all HTML tags → plain text
        plain_text = re.sub(r"<[^>]+>", "", html_block).strip()
        # (6c) Collapse multiple blank lines into a single blank line
        plain_text = re.sub(r"\n\s*\n+", "\n\n", plain_text)

        # (6d) Render the “card” with a white background and black text
        st.markdown(
            f"""
            <div style="
                    background-color: #FFFFFF;
                    border-radius: 8px;
                    padding: 20px 24px;
                    margin: 16px 1rem;
                    color: #000000;
                ">
              <h2 style="margin-top:0; color:#000000;">Your Progress at a Glance 📊</h2>
              <div style="line-height:1.5; font-size:0.95rem;">
                {plain_text.replace('\n', '<br><br>')}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ───────────────────────────────────────────────────────────────────────
        # (6e) Replace curly quotes, em-dashes, en-dashes, etc., so FPDF can encode to Latin-1
        safe_text = (
            plain_text
            .replace("’", "'")   # curly apostrophe → '
            .replace("“", '"')   # left curly quote → "
            .replace("”", '"')   # right curly quote → "
            .replace("—", "-")   # em dash → hyphen
            .replace("–", "-")   # en dash → hyphen
        )

        # Generate the PDF bytes using only Latin-1–compatible characters
        pdf = FPDF(format="letter")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in safe_text.split("\n"):
            pdf.multi_cell(0, 8, line)

        # Now output as Latin-1–encoded bytes
        pdf_bytes = pdf.output(dest="S").encode("latin-1")

        # (6f) Provide a native Streamlit Download button
        st.download_button(
            label="Download Progress Report as PDF",
            data=pdf_bytes,
            file_name=f"profile_progress_report_{student['student_id']}.pdf",
            mime="application/pdf",
            key="download_profile_report",
            help="Click to download your progress report as a PDF",
        )

elif selected_menu == "Settings":
    st.write("⚙️ Settings page (placeholder).")

elif selected_menu == "Sign out":
    st.write("🔒 You have been signed out. (Placeholder for auth.)")
