import setuptools

with open("requirements.txt") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="ai_sql_qa_agent",
    version="1.0.0",
    author="Your Name/Team",  # Replace with actual name/team
    description="An API to query a SQL database using natural language via LangChain.",
    packages=setuptools.find_packages(),
    install_requires=required,
    include_package_data=True,
    package_data={'': ['data/northwind.db']},
)
