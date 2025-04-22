# AI-Powered SQL Q&A Agent

**Query your SQL database using natural language!**

This project provides an intelligent agent built with LangChain that allows you to ask questions about your SQL database in plain English and receive answers based on the database's content.

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
*   **Increase Efficiency:** Quickly get insights from your data without needing a database administrator or data analyst for simple queries.
*   **Flexible Integration:** Easily adapt the agent to work with your own database schemas.

## System Architecture

The agent follows a common pattern for LLM-powered database interaction:

1.  **User Input:** The user asks a question in natural language (e.g., "Show me all customers from London").
2.  **LangChain Agent:** LangChain orchestrates the process. It uses an LLM to:
    *   Understand the user's intent.
    *   Determine the necessary information from the database schema.
    *   Generate the appropriate SQL query (e.g., `SELECT * FROM Customers WHERE City = 'London';`).
3.  **SQL Database Toolkit:** LangChain utilizes a SQL toolkit (like `SQLDatabaseChain` or a custom agent setup) that connects to the target database.
4.  **Database Execution:** The generated SQL query is executed against the database (e.g., `northwind.db`).
5.  **Result Processing:** The raw database results are retrieved.
6.  **LLM Response Generation:** The LLM formats the results into a natural language response (e.g., "Here are the customers based in London: [List of customers]").
7.  **Agent Output:** The final answer is presented to the user.

```
+-------------+       +-----------------+      +----------------------+      +---------------+      +-----------------+
| User        | ----> | LangChain Agent | ---> | LLM (Query Gen)      | ---> | SQL Database  | <--- | Schema Info     |
| (Question)  |       | (Orchestration) |      | (Schema Awareness)   |      | (Execution)   |      | (via Toolkit)   |
+-------------+       +-----------------+      +----------------------+      +-------+-------+      +-----------------+
      ^                                                                              |
      |                                                                              v
      +--------------------------------------<---------------------------------------+
                                      | LLM (Response Format) |
                                      +-----------------------+
```
*(Diagram: Simplified text representation of the flow)*

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
    *(Assuming a requirements.txt file exists or will be created)*
    ```bash
    pip install langchain langchain-openai langchain-community sqlalchemy # Add other specific dependencies
    # Example: pip install -r requirements.txt
    ```
    *Note: You might need specific database drivers depending on your database (e.g., `psycopg2-binary` for PostgreSQL, `mysql-connector-python` for MySQL).*

5.  **Database Setup:**
    *   The repository includes a sample SQLite database: `northwind.db`. No further setup is needed to use this sample.
    *   To connect to your own database, see the [Connecting to a Custom Database](#connecting-to-a-custom-database) section.

6.  **API Keys and Environment Variables:**
    *   This agent requires access to an LLM (e.g., OpenAI, Anthropic, Google). You need to obtain an API key from your chosen provider.
    *   Set the following environment variables:
        ```bash
        export OPENAI_API_KEY='your_openai_api_key' # Replace with your actual key
        # Add other necessary keys, e.g., LANGCHAIN_API_KEY for LangSmith tracing
        export LANGCHAIN_TRACING_V2='true'
        export LANGCHAIN_API_KEY='your_langsmith_api_key' # Optional: For LangSmith
        ```
    *   *Security Note:* Avoid hardcoding keys directly in the script. Use environment variables or a secure secrets management system.

## How to Use

*(Assuming the agent is run via a Python script, e.g., `main.py`)*

1.  **Run the Agent:**
    ```bash
    python main.py # Replace main.py with the actual script name
    ```

2.  **Ask Questions:** Once the agent is running, you can interact with it by typing your questions.

**Example Queries (using `northwind.db`):**

*   "How many customers are there?"
*   "Show me the names of all products."
*   "Which employee has the title 'Sales Representative'?"
*   "List all orders placed in 1997."
*   "What are the distinct cities where customers are located?"
*   "Show me the customers from Germany."

**Example Response (for "Show me the customers from Germany"):**

```
> Okay, I found the following customers from Germany:
> - Alfreds Futterkiste
> - Blauer See Delikatessen
> - Drachenblut Delikatessen
> - Frankenversand
> - Königlich Essen
> - Lehmanns Marktstand
> - Morgenstern Gesundkost
> - Ottilies Käseladen
> - QUICK-Stop
> - Toms Spezialitäten
> - Wartian Herkku
```
*(Note: The exact response format may vary based on the LLM and agent configuration.)*

## Connecting to a Custom Database

To connect the agent to your own database:

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

3.  **Schema Awareness:** LangChain's SQL toolkit automatically inspects the schema (tables, columns, relationships) of the connected database. For very large schemas, you might want to specify which tables the agent should consider:
    ```python
    db = SQLDatabase.from_uri(db_uri, include_tables=['users', 'orders'], sample_rows_in_table_info=3)
    ```

4.  **Rerun the Agent:** Start the agent again after making these changes. It will now query your custom database.

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
*   **Database Credentials:** Similarly, secure your database connection strings, especially for production databases. Avoid hardcoding them.
*   **Permissions:** Connect to the database with a user that has the minimum required permissions (e.g., read-only access if the agent only needs to query data). Avoid using root or admin database users.
*   **Input Sanitization:** While LangChain toolkits provide some safety, be aware of the potential for prompt injection attacks if user input is directly incorporated into sensitive parts of the agent's prompts or logic.
*   **Query Inspection:** For sensitive environments, consider logging or monitoring the SQL queries generated by the LLM before execution to prevent unintended data exposure or modification (if write access is granted). LangSmith is excellent for this.
*   **Rate Limiting/Cost Control:** LLM API calls can incur costs. Implement safeguards if necessary to prevent excessive usage.

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

**Q3: How do I limit the tables the agent can access?**
*   **A:** Use the `include_tables` argument when creating the `SQLDatabase` object, as shown in the [Custom Database](#connecting-to-a-custom-database) section. Alternatively, connect with a database user that only has access to specific tables.

**Q4: Can the agent modify the database (INSERT, UPDATE, DELETE)?**
*   **A:** By default, the standard LangChain SQL toolkits are designed for read-only (`SELECT`) queries. Enabling write capabilities is possible but significantly increases security risks and complexity. It's generally not recommended unless absolutely necessary and with strict safeguards.

**Q5: How do I track the agent's performance and costs?**
*   **A:** Integrate with tools like [LangSmith](https://www.langchain.com/langsmith) for tracing, debugging, and monitoring agent runs and LLM calls. This helps understand the agent's internal steps and associated token usage/costs. Remember to set the `LANGCHAIN_TRACING_V2` and `LANGCHAIN_API_KEY` environment variables.
