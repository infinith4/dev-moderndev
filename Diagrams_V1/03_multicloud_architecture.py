#!/usr/bin/env python3
"""
Multi-Cloud Architecture
Integration across AWS, Azure, and GCP cloud providers
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
from diagrams.azure.compute import VM
from diagrams.azure.database import SQLDatabases
from diagrams.gcp.compute import GCE
from diagrams.gcp.storage import GCS

with Diagram("Multi-Cloud Architecture", filename="03_multicloud_architecture", show=False, direction="LR"):
    with Cluster("AWS"):
        aws_lb = ELB("AWS LB")
        aws_web = [
            EC2("Web 1"),
            EC2("Web 2")
        ]
        aws_db = RDS("PostgreSQL")
        aws_lb >> aws_web >> aws_db

    with Cluster("Azure"):
        azure_vm = VM("App Server")
        azure_db = SQLDatabases("SQL Database")
        azure_vm >> azure_db

    with Cluster("GCP"):
        gcp_compute = GCE("Analytics")
        gcp_storage = GCS("Data Lake")
        gcp_compute >> gcp_storage

    # Cross-cloud connections
    aws_web >> Edge(label="API", color="blue") >> azure_vm
    azure_vm >> Edge(label="Data Sync", color="green") >> gcp_storage
