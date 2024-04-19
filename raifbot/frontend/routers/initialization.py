from routers.common import reset_conversation
import bson


def initialize_session_state(session_state: dict):
    """
    Initializes the session state variables for the Streamlit app.

    Args:
        session_state (dict): A dictionary representing the session state.

    Returns:
        dict: The updated session state with initialized values.

    This function ensures all necessary session state variables are initialized with default values or based on the selected option.
    """

    # Initialize other session state variables with default values
    default_values = {
        "messages": [],
        "session_id": str(bson.ObjectId()),  #
        "current_message": "",
        "parsed_message": "",
        "parsed_message_strip": "",
        "full_response": "",
        "part": "",
        "prompt": "",
        "full_response": "",
        "parsed_message": "",
        "text_data": "",
        "chat_index": 0,
        "source": "",
        "history": "",
    }

    for key, value in default_values.items():
        if key not in session_state:
            session_state[key] = value

    return session_state
