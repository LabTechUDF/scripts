from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import Flask, React
from diagrams.programming.language import Python
from diagrams.onprem.database import MongoDB
from diagrams.onprem.vcs import Github

with Diagram("Arquitetura da Solução Proposta", show=False):
    user = User("Usuário")
    db = MongoDB("MongoDB")
    
    with Cluster("Firebase Hosting"):
        dashboard = React("Dashboard (React)")
    
    with Cluster("AWS EC2"):
        api = Flask("API (Flask)")
        etl = Python("ETL (Python)")
    
    # Flow:
    # 1. The user accesses the React dashboard.
    # 2. The dashboard communicates with the API.
    # 3. The API interacts with the MongoDB database.
    # 4. The ETL process retrieves data from the GitHub API and updates MongoDB.
    user >> dashboard
    dashboard >> api
    api << db

    github = Github("GitHub API")
    github << etl
    etl >> db
