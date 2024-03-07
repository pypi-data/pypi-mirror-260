from typing import Optional, Any

from aws_cdk import App, aws_sns, IResource
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_events as aws_events
from aws_cdk.aws_ec2 import InterfaceVpcEndpointAwsService
from aws_cdk.aws_iam import IRole, Role, ServicePrincipal, ManagedPolicy, PolicyStatement, Effect
from aws_cdk.aws_stepfunctions import IStateMachine

from infraflow.cdk import ServiceStageStack, EnvConfig
from infraflow.cdk.app_patterns.express_default_dlq_processor import ProcessorConfig, DualPriorityResilientProcessor, \
    PROCESSOR_TYPE
from infraflow.cdk.core.environment import DEFAULT_INTERFACE_SERVICES
from infraflow.cdk.docker import EcsCluster
from infraflow.cdk.events import EventBridgeEvents, InfraflowEventBus, SnsEvents, Event
from infraflow.cdk.iam import PolicyBuilder, IamAction
from infraflow.cdk.lambdas import LambdaContext
from infraflow.cdk.sg.patterns import Tiered
from infraflow.cdk.sg.ports import port_for


class StandardServiceStage(ServiceStageStack):
    # noinspection PyDefaultArgument
    def __init__(self,
                 app: App,
                 service_name: str,
                 stage_name: str,
                 env: EnvConfig,
                 src_path: str = "src",
                 db_ports=[],
                 python_version: aws_lambda.Runtime = aws_lambda.Runtime.PYTHON_3_9,
                 vpc_endpoint_services: list[InterfaceVpcEndpointAwsService] = DEFAULT_INTERFACE_SERVICES,
                 **kwargs):
        super().__init__(app, service_name, stage_name, env, **kwargs)
        self.db_ports = db_ports
        self.vpc_endpoint_services = vpc_endpoint_services
        self._ecs_execution_role = None
        self._app_role = None
        self._event_publish_policy = None
        self.python_version = python_version
        self.src_path = src_path
        self._lambda_context: Optional[LambdaContext] = None
        self._api: Optional[apigateway.IRestApi] = None
        self._event_bridge_bus_cdk: Optional[aws_events.IEventBus] = None
        self._events: Optional[EventBridgeEvents] = None
        self._ecs_cluster: Optional[EcsCluster] = None
        self._sns_bus_cdk: Optional[aws_sns.Topic] = None
        self.security_groups: Tiered = Tiered(self, db_ports=db_ports)
        self._managed_policies = {}

    @property
    def api(self) -> apigateway.IRestApi:
        self.use_api()
        return self._api

    def use_api(self):
        self._api = self._api or apigateway.RestApi(self, "API")

    @property
    def events(self) -> InfraflowEventBus:
        self.use_events()
        return self._events

    def use_events(self):
        if not self._event_bridge_bus_cdk and not self._sns_bus_cdk:
            self.use_event_bridge()

        self._events = self._events or (
            EventBridgeEvents(self, 'Events', self._event_bridge_bus_cdk) if self._event_bridge_bus_cdk else
            SnsEvents(self, 'Events', self._sns_bus_ckd) if self._sns_bus_ckd else
            None
        )

        if self._event_bridge_bus_cdk and self._app_role:
            self._event_bridge_bus_cdk.grant_put_events_to(self._app_role)

    @property
    def event_bridge_bus(self) -> aws_events.IEventBus:
        self.use_event_bridge()
        return self._event_bridge_bus_cdk

    def use_event_bridge(self):
        self._event_bridge_bus_cdk = self._event_bridge_bus_cdk or aws_events.EventBus(self, "Bus")

    @property
    def sns_bus(self) -> aws_sns.ITopic:
        self.use_sns()
        return self._sns_bus_cdk

    def use_sns(self):
        self._sns_bus_cdk = self._sns_bus_cdk or aws_sns.Topic(self, "SnsTopic")

    @property
    def lambda_context(self) -> LambdaContext:
        self.use_lambda()
        return self._lambda_context

    def use_lambda(self):
        ## allow lambda access to build EC2 network interface
        self.app_role.add_managed_policy(
            self.managed_policy("LambdaAllowENIManagement", name="AWSLambdaENIManagementAccess")
        )

        self._lambda_context = self._lambda_context or LambdaContext(
            self,
            path=self.src_path,
            role=self.app_role,
            runtime=self.python_version
        )

    def managed_policy(self, id, *, arn=None, name=None):
        if not arn:
            arn = f"arn:aws:iam::aws:policy/service-role/{name}"
        self._managed_policies[id] = self._managed_policies.get(id) or ManagedPolicy.from_managed_policy_arn(
            scope=self,
            id=id,
            managed_policy_arn=arn
        )
        return self._managed_policies[id]

    @property
    def ecs_cluster(self) -> EcsCluster:
        self.use_ecs()
        return self._ecs_cluster

    def handle_event(self, event: Event, default: ProcessorConfig, express: ProcessorConfig = None):
        uses_docker = express.type == PROCESSOR_TYPE.ECS_DOCKER or default.type == PROCESSOR_TYPE.ECS_DOCKER
        uses_lambda = express.type == PROCESSOR_TYPE.LAMBDA_PYTHON or default.type == PROCESSOR_TYPE.LAMBDA_PYTHON
        processor = DualPriorityResilientProcessor(
            default_processor=default,
            express_processor=express,
            ecs_cluster=self.ecs_cluster if uses_docker else None,
            lambda_context=self.lambda_context if uses_lambda else None,
            event=event,
            construct_id=event.id+"Processor",
            scope=self
        )
        processor.create_resources()

    def use_ecs(self):
        if not self._ecs_execution_role:
            self._ecs_execution_role = Role(self, "EcsExecRole", assumed_by=ServicePrincipal("ecs.amazonaws.com"))
            self._ecs_execution_role.add_managed_policy(
                self.managed_policy("EcsTaskExecutionPolicy", name="AmazonECSTaskExecutionRolePolicy")
            )
            self._ecs_execution_role.add_to_policy(
                PolicyStatement(
                    effect=Effect.ALLOW,
                    resources=['*'],
                    actions=['ecr:GetAuthorizationToken',
                             'ecr:BatchCheckLayerAvailability',
                             'ecr:GetDownloadUrlForLayer',
                             'ecr:BatchGetImage']
                )
            ) ## 03.01 -> allow ecs execution to access ALL ecr resources..
            self._ecs_execution_role.assume_role_policy.add_statements(
                PolicyStatement(
                    effect=Effect.ALLOW,
                    actions=['sts:AssumeRole'],
                    principals=[ServicePrincipal("ecs-tasks.amazonaws.com")]
                )
            )

        self._ecs_cluster = self._ecs_cluster or EcsCluster(
            self,
            "EcsCluster",
            execution_role=self._ecs_execution_role,
            task_role=self.app_role
        )

    def use_monolith_lambda_api(self, handler):
        self._api = apigateway.LambdaRestApi(
            self, "API", handler=self.lambda_context.api_function(handler, "ApiHandler")
        )

    def use_monolith_step_function_api(self, state_machine: IStateMachine):
        self._api = apigateway.StepFunctionsRestApi(
            self, "API", state_machine=state_machine
        )

    def lambda_api_resource_handler(self, handler, name=None, suffix=None):
        return apigateway.LambdaIntegration(
            handler=self.lambda_context.api_function(handler, name=name, suffix=suffix)
        )

    # noinspection PyMethodMayBeStatic
    def step_functions_api_resource_handler(self, state_machine: IStateMachine):
        integration = apigateway.StepFunctionsIntegration()
        integration.start_execution(state_machine)
        return integration

    @property
    def app_group(self):
        return self.security_groups.app

    @property
    def dbs_group(self):
        return self.security_groups.dbs

    @property
    def web_group(self):
        return self.security_groups.web

    def use_external_resource(self, resource: IResource, name: str, actions: list[IamAction] = None):
        db: Any = resource
        self.app_group.connections.allow_to(resource, port_range=port_for(db))
        if actions and len(actions):
            policy = PolicyBuilder()
            policy.allow_resource(resource).for_actions(actions)
            self.app_role.attach_inline_policy(policy.build_cdk_policy(self, f"{name}Policy"))

    @property
    def app_role(self) -> IRole:
        self._app_role = self._app_role or Role(self, 'Role', assumed_by=ServicePrincipal("lambda.amazonaws.com"))
        self._app_role.assume_role_policy.add_statements(
            PolicyStatement(
                effect=Effect.ALLOW,
                actions=['sts:AssumeRole'],
                principals=[ServicePrincipal("ecs.amazonaws.com")]
            )
        )
        self._app_role.assume_role_policy.add_statements(
            PolicyStatement(
                effect=Effect.ALLOW,
                actions=['sts:AssumeRole'],
                principals=[ServicePrincipal("ecs-tasks.amazonaws.com")]
            )
        )
        if self._event_bridge_bus_cdk:
            self._event_bridge_bus_cdk.grant_put_events_to(self._app_role)
        return self._app_role

    def setup_endpoint_access(self):
        interfaces = self.env.service_endpoints(self.vpc_endpoint_services)
        for x in interfaces:
            self.security_groups.app.connections.allow_to(x)
