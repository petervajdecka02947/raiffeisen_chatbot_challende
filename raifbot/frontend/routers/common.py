# common.py
import streamlit as st
import bson
import ast
import re


def reset_conversation(selected_option, session_state):
    """
    Resets the conversation in the Streamlit session. It clears existing messages, generates a new session ID, and initializes the conversation with a greeting message.

    Args:
        selected_option: The selected option or category for the new conversation.
        session_state: The Streamlit session state object used to store session-specific data.

    No return value; the function updates the session state in place.
    """
    session_state.messages = []
    session_state.session_id = str(bson.ObjectId())
    session_state.messages.append({"role": "user", "content": "Hey! 👋"})
    session_state.messages.append(
        {
            "role": "assistant",
            "content": f"Hello! Ask me anything related to {selected_option} 🤗",
        }
    )


def parse_response(full_response):
    """
    Parses the full response text to format and clean it for display.
    It tries to replace specific characters and handle Python literal structures to ensure the response text is cleanly formatted.

    Args:
        full_response: The raw response text that needs to be parsed and cleaned.

    Returns:
        str: The parsed and cleaned response text.

    Note:
        This function attempts multiple parsing strategies and falls back to returning the raw response if parsing fails.
    """
    try:
        current_message = full_response.replace("```", "~~~").replace("``", "~~")
        parsed_message_strip = current_message.strip("'\"\n ")
        parsed_message = ast.literal_eval(f'"{parsed_message_strip}"')
        return parsed_message
    except:
        try:
            full_response = full_response.replace("\\n", "\n")
            parsed_message = re.sub(r'`|"|}|{', " ", str(full_response))
            return parsed_message
        except:
            return full_response


def on_select_change():
    """
    Handler function for selection changes in the Streamlit app.
    It updates the conversation based on the new selection made by the user.

    This function retrieves the currently selected option from the session state, then calls `reset_conversation` to initialize a new conversation context based on this selection.

    No return value; the function acts on the session state and updates the conversation in place.
    """
    selected_option = st.session_state["selectbox_key"]
    reset_conversation(selected_option, st.session_state)


def set_history_prompt(query, history, level=1):
    """
    Formats a prompt that includes the chat history and the current query.
    It generates a prompt string that combines the recent chat history with a new query for the conversational agent.

    Args:
        query: The current query or question to be answered.
        history: The chat history list containing past message exchanges.
        level (int, optional): The number of recent chat messages to include from the history. Defaults to 2.

    Returns:
        str: A formatted prompt string combining the chat history and the current query.
    """
    # TODO:calculate max number of tokens dynamically
    return "Chat history: {}.\nKeep in mind the above chat history to answer following input question: {}".format(
        str(history[-level::]), query
    )
