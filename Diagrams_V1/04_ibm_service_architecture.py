#!/usr/bin/env python3
"""IBM Service Architecture with official IBM custom icons."""

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom


ICON_DIR = Path(__file__).resolve().parent / "icons" / "ibm"

with Diagram(
    "IBM Service Architecture",
    filename="04_ibm_service_architecture",
    show=False,
    direction="LR",
):
    internet = Custom(
        "Internet service",
        str(ICON_DIR / "CloudInternetServices.png"),
    )

    with Cluster("Security"):
        verify = Custom(
            "IBM Verify",
            str(ICON_DIR / "SecurityVerify.png"),
        )

    with Cluster("Application Platform"):
        openshift = Custom(
            "OpenShift",
            str(ICON_DIR / "OpenShiftContainerPlatformVPC.png"),
        )
        code_engine = Custom(
            "Code Engine",
            str(ICON_DIR / "CloudCodeEngine.png"),
        )
        openshift >> Edge(label="deploy") >> code_engine

    with Cluster("Data and Messaging"):
        icos = Custom(
            "ICOS",
            str(ICON_DIR / "CloudObjectStorage.png"),
        )
        postgresql = Custom(
            "PostgreSQL",
            str(ICON_DIR / "CloudDatabasesPostgreSQL.png"),
        )
        sendgrid = Custom(
            "SendGrid",
            str(ICON_DIR / "CloudEmailDeliveryService.png"),
        )

    internet >> verify >> openshift
    code_engine >> Edge(label="object data") >> icos
    code_engine >> Edge(label="transaction data") >> postgresql
    code_engine >> Edge(label="email") >> sendgrid
