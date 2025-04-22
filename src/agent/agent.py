from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langgraph.prebuilt import create_react_agent

from src.database.connection import DatabaseConnection
from src.config.settings import get_settings
from src.utils.logger import logger


def run_sql_query_agent(query: str):
    # Get DB connection
    try:
        db = DatabaseConnection.get_connection()
        logger.info(f"Database loaded successfully. Dialect: {db.dialect}")
        logger.info(f"Available tables: {db.get_usable_table_names()}")

        # Load settings
        settings = get_settings()
        logger.info(f"Using model: {settings.MODEL_NAME}")

        # Initialize the LLM
        llm = ChatGoogleGenerativeAI(model=settings.MODEL_NAME)
        logger.info("LLM initialized successfully")

        # Initialize toolkit
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        logger.info("SQL Database toolkit initialized successfully")
        tools = toolkit.get_tools()

        # Load prompt template
        prompt_template = hub.pull('langchain-ai/sql-agent-system-prompt')
        system_message = prompt_template.format(dialect="SQLite", top_k=5)
        logger.info("Prompt template loaded and formatted")

        # Create the agent
        sql_agent = create_react_agent(
            llm,
            tools,
            prompt=system_message,
        )
        logger.info("SQL agent created successfully")

        # Stream and collect final response
        logger.info(f"Processing query: {query}")
        final_output = ""
        for event in sql_agent.stream(
            {"messages": ("user", query)},
            stream_mode="values"
        ):
            last_message = event["messages"][-1]
            last_message.pretty_print()
            final_output = last_message.content

        logger.info("Query processing completed successfully")
        return final_output
        
    except Exception as e:
        logger.error(f"Error in SQL query agent: {str(e)}", exc_info=True)
        raise
