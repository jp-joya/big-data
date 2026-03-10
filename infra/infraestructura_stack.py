from aws_cdk import CfnOutput, Duration, RemovalPolicy, Stack
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
import aws_cdk.aws_rds as rds


class ParcialStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prefijo = self._contexto_str("prefijo", "bnd-test-")
        nombre_llave = self._contexto_str("keyName")

        crear_vpc = self._contexto_bool("crearVpc", True)
        cidr_vpc = self._contexto_str("vpcCidr", "10.50.0.0/16")
        max_azs = self._contexto_int("maxAzs", 2)
        nat_gateways = self._contexto_int("natGateways", 0)
        version_rds_full = self._contexto_str("rdsVersionFull", "14.22") or "14.22"
        version_rds_major = (
            self._contexto_str("rdsVersionMajor", version_rds_full.split(".")[0])
            or version_rds_full.split(".")[0]
        )

        if crear_vpc:
            vpc = ec2.Vpc(
                self,
                "VpcPrincipal",
                vpc_name=f"{prefijo}vpc",
                ip_addresses=ec2.IpAddresses.cidr(cidr_vpc),
                max_azs=max_azs,
                nat_gateways=nat_gateways,
                subnet_configuration=[
                    ec2.SubnetConfiguration(
                        name="publica",
                        subnet_type=ec2.SubnetType.PUBLIC,
                        cidr_mask=24,
                    ),
                    ec2.SubnetConfiguration(
                        name="privada-aislada",
                        subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                        cidr_mask=24,
                    ),
                ],
            )
        else:
            id_vpc = self._contexto_str("vpcId")
            if not id_vpc:
                raise ValueError("Si crearVpc=false debes enviar -c vpcId=vpc-xxxx.")
            vpc = ec2.Vpc.from_lookup(self, "VpcExistente", vpc_id=id_vpc)

        arn_rol_ec2 = self._contexto_str("ec2RoleArn")
        arn_rol_backend = self._contexto_str("backendRoleArn") or arn_rol_ec2
        arn_rol_frontend = self._contexto_str("frontendRoleArn") or arn_rol_ec2

        sg_rds = ec2.SecurityGroup(
            self,
            "SgRds",
            vpc=vpc,
            description="Seguridad para RDS privada",
            allow_all_outbound=True,
            security_group_name=f"{prefijo}sg-rds",
        )

        sg_backend = ec2.SecurityGroup(
            self,
            "SgBackend",
            vpc=vpc,
            description="Seguridad backend",
            allow_all_outbound=True,
            security_group_name=f"{prefijo}sg-backend",
        )

        sg_frontend = ec2.SecurityGroup(
            self,
            "SgFrontend",
            vpc=vpc,
            description="Seguridad frontend",
            allow_all_outbound=True,
            security_group_name=f"{prefijo}sg-frontend",
        )

        sg_frontend.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP publico")
        sg_backend.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8000), "API publica")
        sg_rds.add_ingress_rule(sg_backend, ec2.Port.tcp(5432), "Backend hacia RDS")

        subredes_rds = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED).subnets
        if len(subredes_rds) == 0:
            subredes_rds = vpc.select_subnets(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ).subnets
        if len(subredes_rds) == 0:
            raise ValueError(
                "No se encontraron subredes privadas para RDS (isolated o private with egress)."
            )

        instancia_rds = rds.DatabaseInstance(
            self,
            "RdsChinook",
            instance_identifier=f"{prefijo}chinook-rds",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.of(
                    postgres_full_version=version_rds_full,
                    postgres_major_version=version_rds_major,
                ),
            ),
            credentials=rds.Credentials.from_generated_secret("chinookadmin"),
            database_name="chinook",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=subredes_rds),
            publicly_accessible=False,
            security_groups=[sg_rds],
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            allocated_storage=20,
            max_allocated_storage=100,
            backup_retention=Duration.days(7),
            multi_az=False,
            deletion_protection=False,
            removal_policy=RemovalPolicy.DESTROY,
        )

        rol_backend = self._crear_o_importar_rol(
            arn_rol_backend,
            "RolBackend",
            f"{prefijo}rol-backend",
        )
        rol_frontend = self._crear_o_importar_rol(
            arn_rol_frontend,
            "RolFrontend",
            f"{prefijo}rol-frontend",
        )

        if instancia_rds.secret is not None:
            instancia_rds.secret.grant_read(rol_backend)

        maquina_linux = ec2.MachineImage.latest_amazon_linux2023()

        backend_user_data = ec2.UserData.for_linux()
        backend_user_data.add_commands(
            "dnf update -y",
            "dnf install -y python3 git",
            "mkdir -p /opt/bnd-test/backend",
            "cat > /etc/systemd/system/bnd-test-backend.service <<'SERVICIO'",
            "[Unit]",
            "Description=backend FastAPI",
            "After=network.target",
            "",
            "[Service]",
            "Type=simple",
            "User=ec2-user",
            "WorkingDirectory=/opt/bnd-test/backend",
            "EnvironmentFile=/etc/bnd-test-backend.env",
            "ExecStart=/opt/bnd-test/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000",
            "Restart=always",
            "RestartSec=5",
            "",
            "[Install]",
            "WantedBy=multi-user.target",
            "SERVICIO",
            "cat > /etc/bnd-test-backend.env <<'ENV'",
            "DATABASE_URL=sqlite:////opt/bnd-test/chinook.db",
            "ENV",
            "chown ec2-user:ec2-user /etc/bnd-test-backend.env",
            "systemctl daemon-reload",
            "systemctl enable bnd-test-backend.service",
        )

        frontend_user_data = ec2.UserData.for_linux()
        frontend_user_data.add_commands(
            "dnf update -y",
            "dnf install -y nginx",
            "mkdir -p /usr/share/nginx/html",
            "cat > /usr/share/nginx/html/index.html <<'HTML'",
            "<html><body><h1>frontend listo para despliegue</h1></body></html>",
            "HTML",
            "systemctl enable nginx",
            "systemctl restart nginx",
        )

        parametros_instancia: dict[str, str] = {}
        if nombre_llave:
            parametros_instancia["key_name"] = nombre_llave

        instancia_backend = ec2.Instance(
            self,
            "Ec2Backend",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=sg_backend,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            machine_image=maquina_linux,
            role=rol_backend,
            user_data=backend_user_data,
            instance_name=f"{prefijo}ec2-backend",
            **parametros_instancia,
        )

        instancia_frontend = ec2.Instance(
            self,
            "Ec2Frontend",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=sg_frontend,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            machine_image=maquina_linux,
            role=rol_frontend,
            user_data=frontend_user_data,
            instance_name=f"{prefijo}ec2-frontend",
            **parametros_instancia,
        )

        CfnOutput(self, "VpcId", value=vpc.vpc_id)
        CfnOutput(self, "EndpointRds", value=instancia_rds.instance_endpoint.hostname)
        CfnOutput(self, "PuertoRds", value=str(instancia_rds.instance_endpoint.port))
        CfnOutput(self, "BackendInstanceId", value=instancia_backend.instance_id)
        CfnOutput(self, "FrontendInstanceId", value=instancia_frontend.instance_id)
        CfnOutput(self, "BackendPublicIp", value=instancia_backend.instance_public_ip)
        CfnOutput(self, "FrontendPublicIp", value=instancia_frontend.instance_public_ip)
        if instancia_rds.secret is not None:
            CfnOutput(self, "RdsSecretArn", value=instancia_rds.secret.secret_arn)

    def _crear_o_importar_rol(
        self,
        arn_rol: str | None,
        id_constructo: str,
        nombre_rol: str,
    ) -> iam.IRole:
        if arn_rol:
            return iam.Role.from_role_arn(self, f"{id_constructo}Importado", arn_rol)

        return iam.Role(
            self,
            id_constructo,
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
            ],
            role_name=nombre_rol,
        )

    def _contexto_str(self, nombre: str, por_defecto: str | None = None) -> str | None:
        valor = self.node.try_get_context(nombre)
        if valor is None:
            return por_defecto

        valor_limpio = str(valor).strip()
        if valor_limpio == "":
            return por_defecto

        return valor_limpio

    def _contexto_int(self, nombre: str, por_defecto: int) -> int:
        valor = self._contexto_str(nombre)
        if valor is None:
            return por_defecto
        return int(valor)

    def _contexto_bool(self, nombre: str, por_defecto: bool) -> bool:
        valor = self._contexto_str(nombre)
        if valor is None:
            return por_defecto

        return valor.lower() in ("1", "true", "yes", "si", "on")
