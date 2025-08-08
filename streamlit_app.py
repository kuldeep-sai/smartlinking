import streamlit as st
import os
import tempfile
import zipfile
from interlinking_core import run_interlinking

st.set_page_config(page_title="Smart Interlinking Tool", layout="wide")
st.title("🔗 Smart Internal Interlinking Tool")

st.markdown("""
Upload a CSV with two columns:
- `url`: Article URLs
- `keywords`: Comma-separated keywords to target per URL
""")

uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdirname:
        input_path = os.path.join(tmpdirname, "input.csv")
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        st.info("⏳ Running interlinking logic... Please wait.")
        excel_path, output_dir = run_interlinking(input_path, tmpdirname)

        # ZIP output files
        zip_path = os.path.join(tmpdirname, "interlinked_output.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)

        st.success("✅ Interlinking complete!")

        with open(zip_path, "rb") as f:
            st.download_button("📥 Download All Output (ZIP)", f, file_name="interlinked_output.zip")

        with open(excel_path, "rb") as f:
            st.download_button("📊 Download Excel Summary", f, file_name="interlinking_output.xlsx")
