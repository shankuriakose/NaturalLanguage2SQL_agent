# AI-Powered SQL Q&A Agent

**Query your SQL database using natural language!**

This project provides a FastAPI application serving an intelligent agent built with LangChain. It allows you to ask questions about your SQL database in plain English via an API endpoint and receive answers based on the database's content.

## Table of Contents

-   [Project Overview](#project-overview)
-   [System Architecture](#system-architecture)
-   [Setup Instructions](#setup-instructions)
-   [How to Use](#how-to-use)
-   [Connecting to a Custom Database](#connecting-to-a-custom-database)
-   [Multi-Step Query Example](#multi-step-query-example)
-   [Security Notes](#security-notes)
-   [Contribution Guidelines](#contribution-guidelines)
-   [FAQ](#faq)

## Project Overview

This agent leverages the power of Large Language Models (LLMs) and the LangChain framework to understand natural language questions and translate them into SQL queries. It then executes these queries against your specified database (using the provided `northwind.db` SQLite database by default) and returns the results in a user-friendly format.

**Value Proposition:**

*   **Democratize Data Access:** Enable non-technical users to query databases without writing SQL.
*   **Increase Efficiency:** Quickly get insights from your data via API calls without needing a database administrator or data analyst for simple queries.
*   **Flexible Integration:** Easily adapt the agent to work with your own database schemas by modifying the connection settings.
*   **API Accessibility:** Provides a standard HTTP interface for easier integration into other applications or workflows.

## System Architecture

The system combines a FastAPI web server with a LangChain SQL agent:

1.  **API Request:** A client sends a POST request to the `/query` endpoint of the FastAPI server with a JSON payload containing the natural language question (e.g., `{"question": "Show me all customers from London"}`).
2.  **FastAPI Server:** The server receives the request and passes the question to the LangChain agent.
3.  **LangChain Agent:** LangChain orchestrates the process. It uses an LLM (configured via API key) to:
    *   Understand the user's intent from the question.
    *   Determine the necessary information from the database schema (obtained via the `SQLDatabase` connection).
    *   Generate the appropriate SQL query (e.g., `SELECT * FROM Customers WHERE City = 'London';`).
4.  **SQL Database Connection:** LangChain uses the `SQLDatabase` utility to interact with the target database (e.g., `northwind.db`).
5.  **Database Execution:** The generated SQL query is executed against the database.
6.  **Result Processing:** The raw database results are retrieved by the agent.
7.  **LLM Response Generation:** The LLM formats the results into a natural language answer.
8.  **API Response:** The FastAPI server sends a JSON response back to the client containing the answer (e.g., `{"answer": "Here are the customers based in London: ..."}`).

```
+-------------+      +-----------------+      +-----------------+      +----------------------+      +---------------+      +-----------------+
| Client      | ---> | FastAPI Server  | ---> | LangChain Agent | ---> | LLM (Query Gen)      | ---> | SQL Database  | <--- | Schema Info     |
| (POST /query)|      | (main.py)       |      | (Orchestration) |      | (Schema Awareness)   |      | (Execution)   |      | (via SQLDatabase)|
+-------------+      +-------+---------+      +-----------------+      +----------------------+      +-------+-------+      +-----------------+
      ^                      |                                                                               |
      |                      +------------------------------------<------------------------------------------+
      |                                                            | LLM (Response Format) |
      +----------------------<-------------------------------------+-----------------------+
       (JSON Response)
```
*(Diagram: Simplified text representation of the API flow)*

## Setup Instructions

Follow these steps to set up and run the agent:

1.  **Prerequisites:**
    *   Python 3.8+ installed.
    *   Access to a terminal or command prompt.
    *   Git installed (optional, for cloning).

2.  **Clone the Repository (Optional):**
    ```bash
    git clone <repository_url> # Replace with the actual URL if applicable
    cd <repository_directory>
    ```

3.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

4.  **Install Dependencies:**
    Install the required Python packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
    This will install `fastapi`, `uvicorn`, `langchain`, `langchain-google-genai`, `python-dotenv`, and other necessary libraries.
    *Note: If connecting to databases other than SQLite, you might need to manually install additional database drivers (e.g., `psycopg2-binary` for PostgreSQL, `mysql-connector-python` for MySQL).*

5.  **Database Setup:**
    *   The repository includes a sample SQLite database: `northwind.db`. No further setup is needed to use this sample.
    *   To connect to your own database, see the [Connecting to a Custom Database](#connecting-to-a-custom-database) section.

6.  **API Keys and Environment Variables:**
    *   This agent uses Google's Generative AI (Gemini). You need a Google API key.
    *   Create a `.env` file in the project root directory by copying the example file:
        ```bash
        cp .env.example .env
        ```
    *   Edit the `.env` file and add your keys/settings:
        ```dotenv
        # Database URI (optional, defaults to sqlite:///data/northwind.db in main.py)
        # Example for PostgreSQL: DATABASE_URI=postgresql+psycopg2://user:password@host:port/database
        DATABASE_URI=sqlite:///data/northwind.db

        # Google API Key for Gemini model (Required)
        GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"

        # LangChain API Key for tracing (Optional, for LangSmith)
        LANGCHAIN_API_KEY="YOUR_LANGCHAIN_API_KEY"
        LANGCHAIN_TRACING_V2=true # Set to true to enable LangSmith tracing if key is provided
        ```
    *   *Security Note:* The `.env` file is listed in `.gitignore` to prevent accidental commits of your secrets. **Never commit your `.env` file.**

## How to Use

1.  **Ensure Setup is Complete:** Verify you have completed all steps in the [Setup Instructions](#setup-instructions), including installing dependencies and creating/populating your `.env` file.

2.  **Run the FastAPI Server:**
    Start the API server using Uvicorn. The `--reload` flag automatically restarts the server when code changes are detected (useful for development).
    ```bash
    uvicorn main:app --reload
    ```
    The server will typically start on `http://127.0.0.1:8000`. Look for output similar to:
    ```
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [xxxxx] using StatReload
    INFO:     Started server process [xxxxx]
    INFO:     Waiting for application startup.
    INFO:     Successfully connected to database: sqlite:///data/northwind.db
    INFO:     LLM and Agent initialized successfully.
    INFO:     Application startup complete.
    ```
    *(Note: If initialization fails due to missing API keys or DB issues, you'll see error messages here, and the `/query` endpoint might be unavailable.)*

3.  **Send Queries via API:**
    Use a tool like `curl` or any API client (like Postman, Insomnia) to send POST requests to the `/query` endpoint.

    **Example using `curl`:**
    ```bash
    curl -X POST http://127.0.0.1:8000/query \
    -H "Content-Type: application/json" \
    -d '{
      "question": "How many customers are there in Germany?"
    }'
    ```

    **Parameters:**
    *   `-X POST`: Specifies the HTTP method.
    *   `http://127.0.0.1:8000/query`: The URL of the query endpoint.
    *   `-H "Content-Type: application/json"`: Sets the content type header.
    *   `-d '{ "question": "..." }'`: Provides the JSON payload containing the natural language question.

4.  **Receive the Answer:**
    The API will respond with a JSON object containing the answer.

    **Example Response:**
    ```json
    {
      "answer": "There are 11 customers in Germany."
    }
    ```
    *(The exact wording of the answer depends on the LLM.)*

    If an error occurs during processing, you might receive a JSON response with an error detail, like:
    ```json
    {
      "detail": "An internal error occurred while processing your query."
    }
    ```

5.  **Access API Docs (Swagger UI):**
    While the server is running, you can access interactive API documentation by navigating to `http://127.0.0.1:8000/docs` in your web browser. This interface (Swagger UI) allows you to explore and test the API endpoints directly.

## Connecting to a Custom Database

To connect the API agent to your own database:

1.  **Install Database Driver:** Ensure you have the necessary Python driver for your database installed (e.g., `psycopg2-binary` for PostgreSQL).
2.  **Update Database URI:** Modify the part of the agent's code where the database connection is established. This typically involves changing the SQLAlchemy database URI string.

    *   **SQLite (File-based):**
        ```python
        from langchain_community.utilities import SQLDatabase
        db_uri = "sqlite:///path/to/your/database.db"
        db = SQLDatabase.from_uri(db_uri)
        ```
    *   **PostgreSQL:**
        ```python
        # pip install psycopg2-binary
        db_uri = "postgresql+psycopg2://user:password@host:port/database"
        db = SQLDatabase.from_uri(db_uri)
        ```
    *   **MySQL:**
        ```python
        # pip install mysql-connector-python
        db_uri = "mysql+mysqlconnector://user:password@host:port/database"
        db = SQLDatabase.from_uri(db_uri)
        ```
    *   **Other Databases:** Refer to the [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls) for the correct URI format.

3.  **Schema Awareness (Optional):** LangChain's `SQLDatabase` utility automatically inspects the schema. For very large schemas, you can limit the tables the agent sees by modifying the `SQLDatabase` instantiation in `main.py`:
    ```python
    # In main.py, when creating the db object:
    db = SQLDatabase.from_uri(
        db_uri,
        include_tables=['users', 'orders'], # Only include these tables
        sample_rows_in_table_info=3 # Include sample rows in schema info
    )
    ```

4.  **Restart the Server:** If the server is running, stop it (Ctrl+C) and restart it with `uvicorn main:app --reload` to apply the changes. It will now connect to and query your custom database.

## Multi-Step Query Example

Sometimes, answering a question requires multiple steps or intermediate queries. The LangChain agent (especially function-calling models or ReAct-style agents) can handle this.

**Example Scenario:** "Which customer ordered the most 'Chai' product?"

The agent might perform steps like this (simplified):

1.  **Find Product ID:** Ask the DB for the ID of the product named 'Chai'. (e.g., `SELECT ProductID FROM Products WHERE ProductName = 'Chai';`) -> Gets ProductID (e.g., 1)
2.  **Find Orders with Product:** Ask the DB for orders containing that ProductID. (e.g., `SELECT OrderID, Quantity FROM "Order Details" WHERE ProductID = 1;`)
3.  **Aggregate Quantities:** Ask the DB to group the results by customer and sum quantities (might involve joining Orders and Customers tables). (e.g., `SELECT c.CustomerID, c.CompanyName, SUM(od.Quantity) AS TotalQuantity FROM Customers c JOIN Orders o ON c.CustomerID = o.CustomerID JOIN "Order Details" od ON o.OrderID = od.OrderID WHERE od.ProductID = 1 GROUP BY c.CustomerID ORDER BY TotalQuantity DESC LIMIT 1;`)
4.  **Format Response:** Present the customer who ordered the most.

*(Note: The exact internal steps depend heavily on the specific agent implementation and the LLM's reasoning capabilities.)*

## Security Notes

*   **API Keys:** Protect your LLM API keys. Do not commit them directly into your codebase. Use environment variables or a secure secrets manager.
*   **Database Credentials:** Secure your database connection string (`DATABASE_URI`) in the `.env` file. Do not hardcode it in `main.py`.
*   **Permissions:** Ensure the database user specified in the `DATABASE_URI` has the minimum required permissions (e.g., read-only access if the agent only needs to query data). Avoid using root or admin database users.
*   **API Endpoint Security:** Consider adding API authentication/authorization mechanisms to the FastAPI application if deploying it in a production or shared environment (e.g., using API keys, OAuth2). This is not implemented by default.
*   **Input Validation:** The API uses Pydantic for basic request body validation (`QueryRequest`). Further input sanitization might be needed depending on how the question is used internally, although the LangChain agent handles much of the interaction.
*   **Query Inspection:** For sensitive environments, leverage LangSmith (by setting the appropriate environment variables) to monitor the SQL queries generated by the LLM before they are executed. This helps prevent unintended data exposure or modification attempts (though the agent is currently read-only).
*   **Rate Limiting/Cost Control:** LLM API calls incur costs. If deploying publicly, implement rate limiting on the FastAPI endpoint to prevent abuse and control expenses.
*   **Error Handling:** The API returns generic error messages. Ensure detailed internal errors (like specific database errors or LLM exceptions) are logged securely on the server-side and not exposed directly to the client.

## Contribution Guidelines

*(This section is a template. Adjust based on whether the project is open source and your specific contribution process.)*

We welcome contributions! If you'd like to contribute:

1.  **Fork the Repository:** Create your own copy of the repository.
2.  **Create a Branch:** Make a new branch for your feature or bug fix (e.g., `git checkout -b feature/add-new-llm-support`).
3.  **Make Changes:** Implement your changes and additions.
4.  **Add Tests:** Include unit tests or integration tests for your changes if applicable.
5.  **Ensure Code Quality:** Format your code (e.g., using Black, Flake8) and ensure tests pass.
6.  **Update Documentation:** Update this README or other relevant documentation if your changes affect usage, setup, or architecture.
7.  **Submit a Pull Request:** Push your branch to your fork and open a pull request against the main repository branch. Provide a clear description of your changes.

## FAQ

**Q1: The agent gives an error about not finding a table.**
*   **A:** Double-check that the table name exists in your database and that the database user has permission to see it. If you specified `include_tables` during setup, ensure the required table is listed.

**Q2: The agent generates incorrect SQL queries.**
*   **A:** This can happen due to several reasons:
    *   **LLM Limitations:** The LLM might misunderstand the question or the schema. Try rephrasing the question.
    *   **Schema Complexity:** Very complex schemas or ambiguous naming can confuse the LLM. Consider simplifying table/column names or providing more schema context.
    *   **Agent/Prompt Configuration:** The underlying prompts used by the LangChain agent might need tuning.
    *   **Few-Shot Examples:** Providing few-shot examples of question-to-SQL pairs during agent setup can sometimes improve accuracy.

**Q3: How do I limit the tables the API agent can access?**
*   **A:** Modify the `SQLDatabase` instantiation in `main.py` using the `include_tables` argument, as shown in the [Connecting to a Custom Database](#connecting-to-a-custom-database) section. Alternatively, use a database user with restricted table permissions in your `DATABASE_URI`.

**Q4: Can the API agent modify the database (INSERT, UPDATE, DELETE)?**
*   **A:** The current agent configuration using `create_sql_agent` is designed primarily for read-only (`SELECT`) queries. Enabling write capabilities would require significant changes to the agent setup and prompts, and dramatically increases security risks. It is strongly discouraged unless absolutely necessary and implemented with extreme caution and robust safeguards.

**Q5: How do I track the agent's API calls and costs?**
*   **A:** Enable LangSmith integration by setting the `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY` environment variables in your `.env` file. LangSmith allows you to trace, debug, and monitor agent runs, including the underlying LLM calls, which helps understand performance and estimate token usage/costs.

**Q6: How can I deploy this API?**
*   **A:** This FastAPI application can be deployed using various methods suitable for Python web applications, such as:
    *   Containerizing with Docker and deploying to cloud platforms (AWS, GCP, Azure) or container orchestration systems (Kubernetes).
    *   Using Platform-as-a-Service (PaaS) providers like Heroku, Render, or Fly.io.
    *   Running behind a production-grade ASGI server like Uvicorn managed by a process manager (e.g., Gunicorn, systemd).
    Remember to configure environment variables securely in your chosen deployment environment.
