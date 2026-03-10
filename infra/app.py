#!/usr/bin/env python3
import json
import os
import subprocess
import aws_cdk as cdk

from infraestructura_stack import ParcialStack


def obtener_cuenta(aplicacion: cdk.App) -> str | None:
    cuenta_contexto = aplicacion.node.try_get_context("account")
    if cuenta_contexto:
        return str(cuenta_contexto).strip()

    cuenta_entorno = os.getenv("CDK_DEFAULT_ACCOUNT") or os.getenv("AWS_ACCOUNT_ID")
    if cuenta_entorno:
        return cuenta_entorno.strip()

    try:
        salida = subprocess.check_output(
            ["aws", "sts", "get-caller-identity", "--output", "json"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        data = json.loads(salida)
        return str(data.get("Account", "")).strip() or None
    except Exception:
        return None


def obtener_region(aplicacion: cdk.App) -> str:
    region_contexto = aplicacion.node.try_get_context("region")
    if region_contexto:
        return str(region_contexto).strip()

    region_entorno = os.getenv("CDK_DEFAULT_REGION") or os.getenv("AWS_REGION")
    if region_entorno:
        return region_entorno.strip()

    return "us-east-1"


aplicacion = cdk.App()

cuenta = obtener_cuenta(aplicacion)
region = obtener_region(aplicacion)

if not cuenta:
    raise RuntimeError(
        "No fue posible detectar la cuenta AWS. "
        "Configura AWS CLI (`aws configure`) o define CDK_DEFAULT_ACCOUNT."
    )

ParcialStack(
    aplicacion,
    "bnd-test-big-data-stack",
    env=cdk.Environment(account=cuenta, region=region),
)
aplicacion.synth()
