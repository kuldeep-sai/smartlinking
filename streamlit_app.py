# app.py

import streamlit as st
import os
import tempfile
from interlinking_core import run_interlinking

st.set_page_config(page_title="Smart Interlinking Tool", layout="wide")
st.title("🔗 Smart SEO Interlinking Tool")

uploaded_file = st.file_uploader("Upload your CSV file with 'url' and 'keywords' columns", type=["csv"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, "input.csv")
        with open(csv_path, "wb") as f:
            f.write(uploaded_file.read())

        output_excel_path, output_html_dir = run_interlinking(csv_path, tmpdir)

        st.success("✅ Interlinking complete!")

        with open(output_excel_path, "rb") as f:
            st.download_button(
                label="📥 Download Interlinking Excel Report",
                data=f,
                file_name="interlinking_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.markdown("---")
        st.subheader("🔍 Sample Linked HTML Files")
        linked_files = [f for f in os.listdir(output_html_dir) if f.endswith(".html")]
        for file in linked_files[:3]:
            st.markdown(f"✅ {file}")
            with open(os.path.join(output_html_dir, file), "r", encoding="utf-8") as f:
                html_content = f.read()
                st.components.v1.html(html_content, height=400, scrolling=True)
