import streamlit as st
from config import settings
from routers.initialization import initialize_session_state
from routers.ibm_generative_sdk import handle_ibm_sdk
from utils.chat_history_api_client import save_chat_history
from routers.intro import (
    set_page_configuration,
    display_author_info,
    display_main_title,
    display_description,
    display_sources_info,
    display_technical_architecture,
)
from routers.common import (
    reset_conversation,
    parse_response,
    on_select_change,
)

ENDPOINT = settings.ENDPOINT

set_page_configuration()
display_author_info()


# Source Selection
options = [
    "About App",
    "Technical Infrastructure",
    "RaifBot: Pinterest + DuckGo",
]

initialize_session_state(st.session_state)

selected_option = st.sidebar.selectbox(
    "Choose a section:", options, key="selectbox_key", on_change=on_select_change
)

if selected_option == "About App":
    display_main_title()
    display_description()
    display_sources_info()

elif selected_option == "Technical Infrastructure":
    display_technical_architecture()

elif selected_option == "RaifBot: Pinterest + DuckGo":
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.sidebar.write(f" ")
    if st.sidebar.button("Reset Conversation"):
        reset_conversation(selected_option, st.session_state)

    if prompt := st.chat_input("Write input to chatbot"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        (response, source_init, source_name, products_description) = handle_ibm_sdk(
            prompt, ENDPOINT
        )
        parsed_message = parse_response(response)

        with st.chat_message("assistant"):
            try:
                st.markdown(parsed_message)
                save_chat_history(
                    str(st.session_state.session_id),
                    [[prompt, parsed_message]],
                    ENDPOINT,
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": parsed_message}
                )
            except:
                st.markdown(response)
                save_chat_history(
                    str(st.session_state.session_id),
                    [[prompt, response]],
                    ENDPOINT,
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            if "xxx" not in source_init:
                st.markdown("**Related products:**")
                for i, v in enumerate(source_init):
                    st.markdown(source_name[i])
                    st.image(v, width=150)
                    st.markdown(
                        f'<span style="font-size: smaller;">{products_description[i]}.</span>',
                        unsafe_allow_html=True,
                    )
                    st.markdown("")
