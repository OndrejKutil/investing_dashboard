import streamlit as st

# Configure the page for full-screen layout
st.set_page_config(
    page_title="Investment Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Main title
    st.title("Investment Dashboard")
    st.write('Hello')
    


if __name__ == "__main__":
    main()