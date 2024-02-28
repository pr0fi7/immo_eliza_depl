import streamlit as st

def page_one():
    st.title('Page One')
    # Input fields or widgets for page one
    user_input = st.text_input('Enter something:')
    if st.button('Next'):
        st.session_state.user_input = user_input
        st.session_state.page = 'page_two'

def page_two():
    st.title('Page Two')
    # Access stored input from page one
    st.write('Input from Page One:', st.session_state.user_input)
    # Additional input fields or widgets for page two
    if st.button('Previous'):
        st.session_state.page = 'page_one'
    if st.button('Next'):
        # Store inputs from page two or do further processing
        st.session_state.page = 'page_three'

def page_three():
    st.title('Page Three')
    # Additional pages as needed
    if st.button('Previous'):
        st.session_state.page = 'page_two'

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'page_one'

# Render current page based on session state
if st.session_state.page == 'page_one':
    page_one()
elif st.session_state.page == 'page_two':
    page_two()
elif st.session_state.page == 'page_three':
    page_three()
