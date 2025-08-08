# streamlit_app.py

import streamlit as st
import os
from interlinking_core import run_interlinking

st.set_page_config(page_title="Smart Interlinking Tool", layout="centered")
st.title("🔗 Smart Interlinking MVP")

uploaded_file = st.file_uploader("Upload your input CSV with URLs and keywords", type=["csv"])

if uploaded_file:
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    with open("temp_input.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Run Interlinking"):
        with st.spinner("Processing..."):
            excel_path, output_html_dir = run_interlinking("temp_input.csv", output_dir)

        st.success("✅ Interlinking complete!")

        with open(excel_path, "rb") as f:
            st.download_button(
                label="📥 Download Interlinking Report (Excel)",
                data=f,
                file_name="interlinking_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.markdown("### 💡 Linked Articles:")
        for file in os.listdir(output_html_dir):
            if file.endswith(".html"):
                with open(os.path.join(output_html_dir, file), "r", encoding="utf-8") as f:
                    st.download_button(
                        label=f"Download {file}",
                        data=f.read(),
                        file_name=file,
                        mime="text/html"
                    )
