from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.api import APIGateway
from diagrams.gcp.compute import Functions
from diagrams.onprem.client import User
from diagrams.onprem.database import MongoDB, PostgreSQL
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server
from diagrams.programming.framework import Angular, React
from diagrams.onprem.inmemory import Redis
from diagrams.custom import Custom
from diagrams.elastic.elasticsearch import Logstash
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker

# Path to custom icons
icon_path = "./icons/"

# Creating the diagram
with Diagram("Topologia da Solução da Fábrica de Software (LabTech)", show=False):
    # Frontends (Angular and React)
    with Cluster("Clientes / Web Apps"):
        alocacao_frontend = Angular("Alocação Professores")
        eventos_frontend = Angular("Eventos")
        reservas_frontend = React("Reservas")

    # API Gateway
    api_gateway = Nginx("API Gateway")

    # Logstash for logging and auditing
    logstash = Logstash("Logstash")

    # K8s Cluster or Docker Swarm
    with Cluster("Network of Microservices [K8s Cluster or Docker Network]"):
        # Docker(
        #     label="AKS", fontsize="6", loc="t",
        #     fixedsize="true", width="0.5", height="0.8",
        #     pin="true", pos="1,1"
        # )
        with Cluster("Reservas"):
            reservas_api = Custom("API", icon_path + "flask.png")
            mongo_reservas = MongoDB("MongoDB")
        with Cluster("Eventos"):
            eventos_api = Custom("API", icon_path + "spring_boot.png")
            postgres_eventos = PostgreSQL("PostgreSQL")
        with Cluster("Alocação Professores"):
            alocacao_api = Custom("API", icon_path + "nestjs.png")
            postgres_alocacao = PostgreSQL("PostgreSQL")
        with Cluster("Serviços Acessíveis internamente na cluster"):
            with Cluster("Recursos Compartilhados"):
                utils_api = Custom("GraphQL", icon_path + "graphql.png")
                mongo_utils = MongoDB("MongoDB")
            auth_api = Custom("Autenticação API", icon_path + "flask.png")
            # Redis cache for tokens and utils API responses
            redis_cache = Redis("Cache")
        # Kafka for event posting
        kafka = Kafka("Pub/Sub")
        # new_event_topic = Kafka("reservas.evento.aprovado")
        # professor_alocado_topic = Kafka("alocacao.professor.alocado")

    # Authentication Service
    with Cluster("Serviço de Email"):
        email_service = Functions("Enviar Email")
        smtp_service = Server("SMTP GoDaddy")

    # Authentication Server
    auth_server = Custom("Authentication Server (SSO)", icon_path + "authentication_server.png")
    # facebook_auth = Custom("Facebook Auth", icon_path + "facebook.png")
    # google_auth = Custom("Google Auth", icon_path + "google.png")
    # microsoft_auth = Custom("Microsoft Auth", icon_path + "microsoft.png")
    eventos_frontend >> auth_server
    # auth_api >> auth_server
    # auth_server >> facebook_auth
    # auth_server >> google_auth
    # auth_server >> microsoft_auth

    # Connections
    alocacao_frontend >> api_gateway >> alocacao_api
    eventos_frontend >> api_gateway >> eventos_api
    reservas_frontend >> api_gateway >> reservas_api

    # Utils API has no frontend
    reservas_api >> mongo_reservas
    utils_api >> mongo_utils

    eventos_api >> postgres_eventos
    alocacao_api >> postgres_alocacao

    # pub/sub
    reservas_api >> kafka >> eventos_api
    alocacao_api >> kafka >> utils_api
    # reservas_api >> new_event_topic >> eventos_api
    # alocacao_api >> professor_alocado_topic >> utils_api

    # Logging and auditing
    kafka >> logstash
    # email_service >> logstash
    auth_api >> logstash
    api_gateway >> logstash

    # Authentication flow
    auth_api >> email_service >> smtp_service
    auth_api >> redis_cache # Caching tokens and avoid unnecessary sends

    # Caching utils API responses
    utils_api >> redis_cache
