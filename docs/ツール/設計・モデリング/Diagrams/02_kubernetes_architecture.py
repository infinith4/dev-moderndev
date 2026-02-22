#!/usr/bin/env python3
"""
Kubernetes Architecture
Production namespace with ingress, services, pods, and persistent storage
"""

from diagrams import Diagram, Cluster
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.storage import PV, PVC

with Diagram("Kubernetes Architecture", filename="02_kubernetes_architecture", show=False, direction="TB"):
    ingress = Ingress("ingress")

    with Cluster("Namespace: Production"):
        svc = Service("service")

        with Cluster("Deployment"):
            pods = [
                Pod("pod1"),
                Pod("pod2"),
                Pod("pod3")
            ]

        with Cluster("Storage"):
            pvc = PVC("pvc")
            pv = PV("pv")
            pvc - pv

    ingress >> svc >> pods
    pods >> pvc
