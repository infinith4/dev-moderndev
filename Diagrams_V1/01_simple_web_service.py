#!/usr/bin/env python3
"""
Simple Web Service Architecture
AWS 3-tier web application with load balancer, EC2 instances, and RDS database
"""

from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, Route53

with Diagram("Simple Web Service", filename="01_simple_web_service", show=False, direction="LR"):
    dns = Route53("DNS")
    lb = ELB("Load Balancer")

    with Cluster("Web Tier"):
        web_servers = [
            EC2("web1"),
            EC2("web2"),
            EC2("web3")
        ]

    with Cluster("Database Tier"):
        db = RDS("PostgreSQL")

    dns >> lb >> web_servers >> db
