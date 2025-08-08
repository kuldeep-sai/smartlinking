# streamlit_app.py

import streamlit as st
import tempfile
import os
from interlinking_core import run_interlinking

st.set_page_config(page_title="SEO Smart Interlinking Tool", layout="centered")
st.title("🔗 Smart Interlinking MVP")

st.markdown("""
Upload a CSV file with columns:  
- **url** (article URL)  
- **keywords** (comma-separated keywords for that article)  
This tool will inject 5–6 contextual links per article using matching keywords from other articles.
""")

uploaded_file = st.file_uploader("📤 Upload CSV (URLs + keywords)", type=["csv"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.csv")
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        st.info("📄 File uploaded. Running smart interlinking...")

        with st.spinner("Processing articles and injecting links..."):
            try:
                output_excel_path, output_dir = run_interlinking(input_path, tmpdir)

                st.success("✅ Done! Download your files below:")

                # Excel report
                with open(output_excel_path, "rb") as excel_file:
                    st.download_button(
                        label="📥 Download Excel Report",
                        data=excel_file,
                        file_name="interlinking_output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                # HTML downloads
                st.markdown("### 📄 Updated HTML Files")
                html_files = [f for f in os.listdir(output_dir) if f.endswith(".html")]
                for file in html_files:
                    path = os.path.join(output_dir, file)
                    with open(path, "rb") as html_file:
                        st.download_button(
                            label=f"Download {file}",
                            data=html_file,
                            file_name=file,
                            mime="text/html"
                        )

            except Exception as e:
                st.error(f"❌ Error: {e}")
