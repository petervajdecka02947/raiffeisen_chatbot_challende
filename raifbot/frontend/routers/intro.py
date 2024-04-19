from config import settings
from PIL import Image
import streamlit as st

# Accessing the variables
PAGE_ICON = settings.PAGE_ICON
PAGE_TITLE = settings.PAGE_TITLE
RAIF_IMAGE_PATH = settings.RAIF_IMAGE_PATH
PROFILE_IMAGE_PATH = settings.PROFILE_IMAGE_PATH
AUTHOR_NAME = settings.AUTHOR_NAME
AUTHOR_EMAIL = settings.AUTHOR_EMAIL


def set_page_configuration():
    """
    Configures the Streamlit page settings such as layout, page icon, and title.
    """
    st.set_page_config(layout="wide", page_icon=PAGE_ICON, page_title=PAGE_TITLE)


def display_author_info():
    """
    Displays the author's information in a sidebar expander on the Streamlit page.
    This includes an image, the author's name, and contact email.
    """
    with st.sidebar:
        st.sidebar.title("RaifBot (demo)")
        st.write(f"  ")
        image = Image.open(RAIF_IMAGE_PATH)
        st.image(image, width=150)
        st.write(f"  ")
        st.write(f"  ")
        st.write(f"  ")

        with st.expander("📬 Author"):
            image = Image.open(PROFILE_IMAGE_PATH)
            st.image(image)
            st.write(f"**Created by {AUTHOR_NAME}**")
            st.write(f"**Mail**: {AUTHOR_EMAIL}")
        st.write(f"  ")


def display_main_title():
    """
    Displays the main title of the Streamlit page using HTML formatting.
    """
    st.markdown(
        """
        <h2 style='text-align: center;'>RaifBot, your versatile fashion and information advisor 🌟👔</h2>
        """,
        unsafe_allow_html=True,
    )


def display_description():
    """
    Displays a description of the application on the Streamlit page, including its purpose and usage, with HTML formatting.
    """
    st.markdown("---")
    st.markdown(
        """ 
        <h5 style='text-align:center;'>Meet RaifBot, designed to enhance your understanding of fashion and more, powered by advanced AI!</h5>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")


def display_sources_info():
    """
    Displays information about the sources and usage instructions for the Streamlit application.
    """
    st.header("Getting Started")
    st.markdown(
        """
            #### Features of RaifBot
            - **Personalized Recommendations**: Leveraging conversation history for personalized style advice.
            - **Transparency in Responses**: Each response is followed by images with names of relevant sources ensuring clarity and enrichment of information.
            - **History and Personalization**: RaifBot remembers each user interaction, tailoring its advice to your preferences, stored safely with MongoDB by session id.
            - **Comprehensive Search Capabilities**: Provides answers beyond fashion, utilizing DuckGo search for varied inquiries.
            - **Asynchronous Interaction**: Multiple users can interact with RaifBot simultaneously, thanks to its fully asynchronous design.
            - **API Streaming**: Backend and frontend communicate via API streaming. Streamlit's interface ensures smooth interaction without needing to reload all messages upon updates.
            - **Flexible Model Configuration**: Users can modify the LLM model, embedding model, and API key as needed through Swagger documentation, enhancing adaptability and control.
                """
    )

    st.header("How to Use RaifBot")
    st.markdown(
        """
    - **Interactive Chat**: Start by asking RaifBot about fashion trends, style advice, or even general knowledge questions. It’s here to help with a wide range of topics.
    - **Visual Insights**: Responses are accompanied by thematic images, enriching your interaction.
    - **History and Reset**: Access your conversation history anytime and use the reset feature to start a new query series if needed.
    - **Adapt and Configure**: Make adjustments to the AI model and settings through the provided Swagger documentation to suit your specific needs.
    """
    )

    st.markdown("---")


def display_technical_architecture():
    """
    Displays the technical architecture of the RaifBot application, emphasizing the use of advanced cloud technologies, microservices architecture, and state-of-the-art AI models.
    """
    st.header("Technical Infrastructure of RaifBot")
    st.markdown("---")
    st.markdown(
        """
        <h4 style='text-align:center;'>Architectural Overview</h4>
        <p>RaifBot leverages AWS cloud infrastructure with EC2 instances for scalable and efficient computing. The backend is implemented using FastAPI, a high-performance web framework ideal for building APIs with Python 3.7+ based on standard Python type hints.</p>
        <p>The frontend is designed with Streamlit, allowing for dynamic and interactive web applications powered directly by Python scripts. RaifBot employs a microservices architecture, orchestrated with Docker Compose, to ensure a modular and maintainable codebase.</p>
        <p>The four key microservices are:</p>
        <ul>
            <li><strong>API Service:</strong> Manages all backend logic, incorporating the Whole Langchain agent deployed within FastAPI.</li>
            <li><strong>CLI Service:</strong> Provides command-line interactions with the API for streamlined operations.</li>
            <li><strong>Streamlit Frontend:</strong> Facilitates user interactions and communicates with the API, enabling real-time updates without page reloads.</li>
            <li><strong>Nginx:</strong> Serves the entire application securely using HTTPS with CertBot certificates, ensuring robust security and reliability.</li>
        </ul>
        <p>This architecture supports high concurrency and asynchronicity while ensuring the application is fully scalable, allowing multiple users to operate their own instances of RaifBot simultaneously. Conversations are stored in MongoDB by session ID, and the source dataset is managed within a Pinecone Vector database for optimized data retrieval.</p>
        <p>At the core of our generative AI capabilities, RaifBot uses the GPT-4 model for generating responses and leverages the "text-embedding-3-large" embeddings for the retrieval process. This combination ensures accurate, contextually relevant, and engaging user interactions.</p>
        <p>These technical decisions highlight my ability to design and deploy scalable, secure, and effective AI solutions that address modern business needs and technological challenges.</p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")


# Main script execution
if __name__ == "__main__":
    set_page_configuration()
    display_author_info()
    display_main_title()
    display_description()
    display_sources_info()
