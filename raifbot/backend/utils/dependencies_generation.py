from backend.config import settings
import pinecone
import openai
from backend.utils.error_handler import UpdateError
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Pinecone
from langchain_community.tools import DuckDuckGoSearchRun, Tool
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# Add your utility functions here. This is a placeholder.
def update_openai_api_key(new_key: str, model: str):
    """
    Updates the OpenAI API key and model in the application settings.

    Args:
        new_key (str): The new OpenAI API key.
        model (str): The model to be used with the new API key.

    Returns:
        object: The updated application settings.

    This function updates the OpenAI API key and model, and performs a test call to OpenAI's chat API to verify the new key.
    If the test call fails, it raises an UpdateError.

    Raises:
        UpdateError: If the test call to OpenAI's API fails.
    """

    try:
        openai.api_key = new_key

        # Making a simple test call to OpenAI's chat API
        openai.ChatCompletion.create(
            model=model,  # Specify the chat model here
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, who are you?"},
            ],
        )

        settings.OPENAI_API_KEY = new_key
        settings.LLM_NAME = model

        # If the call is successful, the key is working
        return settings

    except openai.error.OpenAIError as e:
        raise UpdateError(
            f"Failed to update API key and model due to OpenAI API error: {e}", 400
        )


def setup_conversational_chain(settings: object):
    """
    Initializes the conversational chain with various tools and configurations.

    Args:
        settings (object): Application settings containing configuration details.

    Returns:
        tuple: A tuple containing the agent, retriever, and language model chain.

    This function sets up the conversational agent with various tools (like retrievers and search functions)
    and configures the language model chain. It handles the initialization of the database, vector database,
    language model, and other components required for the conversational chain.

    Raises:
        UpdateError: If there is an error during the initialization of any component.
    """
    global agent
    global retriever
    global llm

    tools = []

    # Initialize database

    try:
        pinecone.init(
            api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENV
        )

        embeddings_model = OpenAIEmbeddings(
            model=settings.EMBEDDING_NAME, openai_api_key=settings.OPENAI_API_KEY
        )

        vectordb = Pinecone.from_existing_index(settings.INDEX_NAME, embeddings_model)

    except Exception as e:
        raise UpdateError(f"Error during initialization of vector database: {e}", 401)

    # Initialize database LLM model

    try:
        llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name=settings.LLM_NAME,
            temperature=0,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
    except Exception as e:
        raise UpdateError(f"Error during initialization of LLM: {e}", 402)
    # Prepare retriever

    try:
        retriever = vectordb.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.05},  # , "k": 1
        )
    except Exception as e:
        raise UpdateError(f"Error during initialization of retriever: {e}", 403)

    # Initialize tools

    try:
        tool_retrieve = create_retriever_tool(
            retriever,
            "product_search",
            "Searches and returns products regarding the pinterest fashion that meets all requirements (if provided) such as age, gender, location, brand, price, availability. Focus on high rating of products first and click_rate second!",
        )

        search = DuckDuckGoSearchRun()
        search_tool = Tool(
            name="DuckDuckGo",
            func=search,  # .run
            description="This tool is used when you need to do a search on the internet to find information that another tool product_search can't find.",
        )

        tools.append(tool_retrieve)
        tools.append(search_tool)

        #        Initialize tools
        agent = initialize_agent(
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            tools=tools,
            llm=llm,
            verbose=True,
            max_iterations=10,
            early_stopping_method="generate",
            # memory=memory,
            return_intermediate_steps=False,
        )

    except Exception as e:
        raise UpdateError(f"Error during initialization of toolls an agent: {e}", 404)
    # Set template for history input

    try:
        template = (
            """The system should generate a natural language response recommending products with justifications"""
            """(e.g., ”Based on your [requirements], we recommend product X from brand Y because it"""
            """has a high rating and is within your budget”), ensuring it is fully"""
            """supported by the provided context and make sure each product from context must be"""
            """mentioned! If any product doesnt meet any requirement, mention it and explain. For example, if outputed product """
            """is a bit more expensive then your budget limit but it fits your other requirements perfectly, describe it!
        Context: {context}
        Question:{input}
        Answer: """
        )

        prompt = PromptTemplate(template=template, input_variables=["input", "context"])

        llm_chain = LLMChain(prompt=prompt, llm=llm)

    except Exception as e:
        raise UpdateError(f"Unable to set OpenAI chain: {e}", 406)
    return agent, retriever, llm_chain


# Retrieve the relevant document


async def get_source(retriever_obj: object, query: str):
    """
    Retrieves the relevant document source based on a given query.

    Args:
        retriever_obj (object): The retriever object to be used for document retrieval.
        query (str): The query string for which relevant document source is needed.

    Returns:
        str: The source of the relevant document if found, otherwise a default value.

    This function queries the retriever object for relevant documents based on the input query.
    It returns the source of the first relevant document if found, or a default value ('DuckDuckGo' or 'No ibm related source found') otherwise.

    Note:
        The function returns 'DuckDuckGo' if no documents are found or if an exception occurs.
    """
    try:
        docs = await retriever_obj.aget_relevant_documents(query)
    except Exception as e:
        return "Not retrieved"
    if docs == []:
        return "Not retrieved"
    else:
        try:
            doc_sources = [doc.metadata["source"] for doc in docs]
            doc_names = [
                doc.page_content.split("priced")[0].split("Product")[-1].strip()
                for doc in docs
            ]
            doc_description = [doc.page_content for doc in docs]
            return doc_sources, doc_names, doc_description
        except Exception as e:
            return "Not retrieved"
