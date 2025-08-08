import streamlit as st
import tempfile
import os
from interlinking_core import run_interlinking

st.set_page_config(page_title="SEO Smart Interlinking Tool", layout="wide")
st.title("🔗 Smart Interlinking MVP")
st.markdown("Upload your input CSV to generate contextual interlinks.")

uploaded_file = st.file_uploader("📤 Upload Input CSV", type=["csv"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.csv")
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("Processing articles and injecting links..."):
            try:
                output_excel_path, output_dir = run_interlinking(input_path, tmpdir)

                st.success("✅ Interlinking completed!")

                # Excel output
                with open(output_excel_path, "rb") as excel_file:
                    st.download_button(
                        label="📥 Download Report (Excel)",
                        data=excel_file,
                        file_name="interlinking_output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                # HTML file downloads
                st.markdown("### 📁 Download Updated HTML Files")
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
                st.error(f"❌ Error during processing: {e}")
