import streamlit as st

def main():
    st.markdown(
    """
    <style>
    /* Styling for the camera input container */
    [data-testid="stCameraInput"] > div {
        width: 100%;                /* Full width */
        height: 80vh;               /* 80% of viewport height */
        margin: auto;               /* Center the component */
        display: flex;
        flex-direction: column;     /* Ensure the button is below the camera */
        justify-content: center;    /* Center camera and button vertically */
        align-items: center;        /* Center the content horizontally */
        background-color: #f0f0f0;  /* Neutral background */
        border-radius: 10px;        /* Rounded corners */
        padding: 10px;              /* Add padding to prevent content overflow */
        overflow: hidden;           /* Ensure no overflow issues */
    }

    /* Camera frame area */
    [data-testid="stCameraInput"] video {
        width: 100%;                /* Full width of the container */
        height: auto;               /* Maintain aspect ratio */
        max-height: 100%;           /* Ensure video doesn't overflow vertically */
        object-fit: cover;          /* Maintain proper aspect ratio without stretching */
    }

    /* Responsive styling for smaller screens */
    @media (max-width: 768px) {
        [data-testid="stCameraInput"] > div {
            width: 100%;            /* Full width */
            height: 70vh;           /* Adjust height for smaller screens */
        }
    }

    /* Ensure the "Take Photo" button is always visible */
    [data-testid="stCameraInput"] button {
        position: relative;         /* Default positioning */
        bottom: 0;                  /* Align at the bottom of the container */
        margin-top: 10px;           /* Add space above the button */
        z-index: 10;                /* Ensure it stays on top of other elements */
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    
    
