# streamlit_app.py

import streamlit as st
import os
import tempfile
from interlinking_core import run_interlinking

st.set_page_config(page_title="Smart Interlinking MVP", layout="wide")

st.title("🔗 Smart SEO Interlinking Tool")
st.markdown("Upload a CSV with your article URLs and target keywords to auto-generate contextual internal links.")

uploaded_file = st.file_uploader("📤 Upload input CSV", type=["csv"])

if uploaded_file is not None:
    st.success("✅ File uploaded successfully.")

    with st.spinner("Processing..."):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.csv")
            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            try:
                output_excel_path, output_dir = run_interlinking(input_path, tmpdir)

                # Download Excel report
                with open(output_excel_path, "rb") as excel_file:
                    st.download_button(
                        label="📥 Download Interlinking Report (Excel)",
                        data=excel_file,
                        file_name="interlinking_output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                # Download updated HTML files
                st.markdown("📁 **Download Updated HTML Articles**:")
                for file in os.listdir(output_dir):
                    if file.endswith(".html"):
                        file_path = os.path.join(output_dir, file)
                        with open(file_path, "rb") as html_file:
                            st.download_button(
                                label=f"Download {file}",
                                data=html_file,
                                file_name=file,
                                mime="text/html"
                            )
            except Exception as e:
                st.error(f"🚫 Error during processing: {e}")
