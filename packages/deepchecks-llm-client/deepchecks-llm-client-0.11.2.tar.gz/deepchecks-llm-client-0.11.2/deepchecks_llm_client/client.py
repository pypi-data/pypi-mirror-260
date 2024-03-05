import logging
import typing as t
from datetime import datetime
from io import StringIO

import pandas as pd
import pytz
from deepchecks_llm_client.api import API
from deepchecks_llm_client.data_types import AnnotationType, EnvType, Interaction, LogInteractionType, Step, Tag
from deepchecks_llm_client.exceptions import DeepchecksLLMClientError
from deepchecks_llm_client.openai_instrumentor import OpenAIInstrumentor
from deepchecks_llm_client.utils import HandleExceptions, HandleGeneratorExceptions, get_timestamp

__all__ = ["dc_client", "DeepchecksLLMClient"]


logging.basicConfig()
logger = logging.getLogger(__name__)
init_logger = logging.Logger(__name__ + ".init")

DEFAULT_VERSION_NAME = "0.0.1"
DEFAULT_ENV_TYPE = EnvType.PROD


class DeepchecksLLMClient:
    def __init__(self):
        self._api: API = None
        self.app: t.Dict[str, t.Any] = None
        self.instrumentor: OpenAIInstrumentor = None
        self._initialized: bool = False
        self._log_level: int = logging.WARNING
        self.silent_mode: bool = True

    @HandleExceptions(init_logger)
    def init(
        self,
        host: str,
        api_token: str,
        app_name: str,
        version_name: str = DEFAULT_VERSION_NAME,
        env_type: EnvType = DEFAULT_ENV_TYPE,
        auto_collect: bool = False,
        log_level: int = logging.WARNING,
        silent_mode: bool = False,
    ):
        """
        Connect to Deepchecks LLM Server

        Parameters
        ==========
        host : str
            Deepchecks host to communicate with
        api_token : str
            Deepchecks API Token (can be generated from the UI)
        app_name : str
            Application name to connect to
        version_name : str, default="0.0.1"
            Version name to connect to inside the application,
            if Version name does not exist SDK will create it automatically,
        env_type : EnvType, default=EnvType.PROD
            could be EnvType.PROD (for "Production") or EnvType.EVAL (for "Evaluation")
        auto_collect : bool, default=False
            Auto collect calls to LLM Models
        silent_mode: bool, default=False
            Write log messages during the init phase and non-prod phases such as golden_set()
        log_level: int, default=logging.WARNING
            this parameter will set SDK loggers logging level

        Returns
        =======
        None
        """
        if self._initialized:
            logger.warning(
                "Deepchecks client was initialized already. "
                "We will ignore newly provided parameters"
            )
            return

        logger.setLevel(log_level)
        self._log_level = log_level
        self.silent_mode = silent_mode

        if self._api is None:
            if host is not None and api_token is not None:
                self._api = API.instantiate(host=host, token=api_token)
            else:
                raise DeepchecksLLMClientError("host/token parameters must be provided")

        if app_name is None:
            raise DeepchecksLLMClientError("app_name must be supplied")
        self.app = self._api.get_application(app_name)
        if not self.app:
            raise DeepchecksLLMClientError(f"Application: \"{app_name}\", does not exist, please create it via the UI")

        self.app_name(app_name).version_name(version_name).env_type(env_type)

        self.instrumentor = None
        if auto_collect:
            self.instrumentor = OpenAIInstrumentor(self.api, log_level, auto_collect, silent_mode)
            self.instrumentor.perform_patch()
        self._initialized = True

    @property
    def initialized(self):
        return self._initialized

    @property
    def api(self) -> API:
        if self._api:
            return self._api
        raise DeepchecksLLMClientError("dc_client was not initialized correctly, please re-create it")

    @HandleExceptions(logger, return_self=True)
    def app_name(self, new_app_name: str):
        self.api.app_name(new_app_name)
        return self

    @HandleExceptions(logger, return_self=True)
    def version_name(self, new_version_name: str):
        self.api.version_name(new_version_name)
        return self

    @HandleExceptions(logger, return_self=True)
    def env_type(self, new_env_type: EnvType):
        self.api.env_type(new_env_type)
        return self

    @HandleExceptions(logger, return_self=True)
    def auto_collect(self, enabled: bool):
        if not self.instrumentor:
            self.instrumentor = OpenAIInstrumentor(
                api=self.api, log_level=self._log_level, auto_collect=enabled, silent_mode=self.silent_mode
            )
            self.instrumentor.perform_patch()
        else:
            self.instrumentor.auto_collect(auto_collect=enabled)
        return self

    @HandleExceptions(logger, return_self=True)
    def set_tags(self, tags: t.Dict[Tag, str]):
        self.api.set_tags(tags)
        return self

    @HandleExceptions(logger)
    def annotate(self, user_interaction_id: str, version_name: str,
                 annotation: AnnotationType = None, reason: t.Optional[str] = None):
        """
        Annotate a specific interaction by its user_interaction_id
        Parameters
        ----------
        user_interaction_id
            Unique id of the interaction, can be set by the user or automatically generated by deepchecks
        version_name
            Version name to annotate
        annotation
            Could be one of AnnotationType.GOOD, AnnotationType.BAD, AnnotationType.UNKNOWN
            or None to remove annotation
        reason
            String that explains the reason for the annotation

        Returns
        -------
            None

        """

        version_id = self._get_version_id(version_name)
        self.api.annotate(user_interaction_id, version_id, annotation, reason=reason)

    # pylint: disable=redefined-builtin
    @HandleExceptions(logger)
    def log_interaction(self,
                        input: str,
                        output: str,
                        full_prompt: str = None,
                        information_retrieval: str = None,
                        annotation: AnnotationType = None,
                        annotation_reason: str = None,
                        user_interaction_id: str = None,
                        started_at: t.Union[datetime, None] = None,
                        finished_at: t.Union[datetime, None] = None,
                        steps: t.List[Step] = None,
                        custom_props: t.Dict[str, t.Any] = None) -> str:
        # pylint: disable=redefined-builtin
        result = self.api.log_interaction(
            input=input,
            output=output,
            full_prompt=full_prompt,
            information_retrieval=information_retrieval,
            annotation=annotation,
            annotation_reason=annotation_reason,
            user_interaction_id=user_interaction_id,
            started_at=started_at.isoformat() if started_at else datetime.now(tz=pytz.UTC).isoformat(),
            finished_at=finished_at.isoformat() if finished_at else None,
            steps=steps,
            custom_props=custom_props,
        )
        return result.json()[0]

    @HandleExceptions(logger)
    def log_batch_interactions(self, interactions: t.List[LogInteractionType]) -> t.List[str]:
        result = self.api.log_batch(interactions=interactions)
        return result.json()

    @HandleExceptions(logger)
    def update_interaction(
        self,
        user_interaction_id: str,
        version_name: str,
        annotation: AnnotationType = None,
        annotation_reason: t.Optional[str] = None,
        custom_props: t.Union[t.Dict[str, t.Any], None] = None,
    ):
        """
        Update a specific interaction by its user_interaction_id
        Parameters
        ----------
        user_interaction_id
            Unique id of the interaction, can be set by the user or automatically generated by deepchecks
        version_name
            Version name to annotate
        annotation
            Could be one of AnnotationType.GOOD, AnnotationType.BAD, AnnotationType.UNKNOWN
        annotation_reason
            String that explains the reason for the annotation
        custom_props:
            Dictionary of custom properties for interaction
        Returns
        -------
            None

        """

        version_id = self._get_version_id(version_name)
        self.api.update_interaction(
            user_interaction_id=user_interaction_id,
            app_version_id=version_id,
            annotation=annotation,
            annotation_reason=annotation_reason,
            custom_props=custom_props,
        )

    @HandleExceptions(logger)
    def update_application_config(self, file):
        self.api.update_application_config(application_id=self.app["id"], file=file)

    @HandleExceptions(logger)
    def get_application_config(self, file_save_path: t.Union[str, None] = None) -> str:
        return self.api.get_application_config(application_id=self.app["id"], file_save_path=file_save_path)

    @HandleGeneratorExceptions(init_logger)
    def data_iterator(self,
                      environment: t.Union[EnvType, str],
                      version_name: t.Union[str, None] = None,
                      start_time: t.Union[datetime, int, None] = None,
                      end_time: t.Union[datetime, int, None] = None) -> t.Iterable[Interaction]:
        """
        Fetch all interactions from the specified environment type (PROD/EVAL) as an iterable.
        Supports pagination, so this API is suitable for iterating over large amounts of data.

        Parameters
        ----------
        environment : EnvType | str
            The environment type from which to fetch interactions. This can be either "PROD" or "EVAL".

        version_name : str, optional
            The version name to fetch interactions from. If no version name is provided,
            the latest created version in the application will be used. This is mostly useful
            when integrating the golden set and rerunning it in the CI.

        start_time : datetime | int | None, optional
            The start time from which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched from the beginning.

        end_time : datetime | int | None, optional
            The end time until which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched up to the most recent.

        Returns
        -------
        Iterable[Interaction]
            An iterable collection of interactions.

        """
        version_id = self._get_version_id(version_name)

        offset = 0
        limit = 20

        while True:
            interactions = \
                self.api.get_interactions(version_id,
                                          environment=environment,
                                          start_time_epoch=get_timestamp(start_time),
                                          end_time_epoch=get_timestamp(end_time),
                                          limit=limit, offset=offset)
            for interaction in interactions:
                yield Interaction(
                    user_interaction_id=interaction["user_interaction_id"],
                    input=interaction["input"]["data"] if interaction.get("input") else None,
                    information_retrieval=interaction["information_retrieval"]["data"] if interaction.get(
                        "information_retrieval") else None,
                    full_prompt=interaction["prompt"]["data"] if interaction.get("prompt") else None,
                    output=interaction["output"]["data"] if interaction.get("output") else None,
                    created_at=interaction["created_at"],
                    topic=interaction["topic"],
                    output_properties=interaction.get("output_properties", {}) or {},
                    input_properties=interaction.get("input_properties", {}) or {},
                    custom_properties=interaction.get("custom_properties", {}) or {},
                    llm_properties=interaction.get("llm_properties", {}) or {},
                    llm_properties_reasons=interaction.get("llm_properties_reasons", {}) or {},
                )

            # If the size of the data is less than the limit, we"ve reached the end
            if len(interactions) < limit:
                break

            offset += limit

    @HandleExceptions(init_logger)
    def get_data(self, environment: t.Union[EnvType, str],
                 version_name: t.Union[str, None] = None,
                 return_topics: bool = False, return_annotation_data: bool = False,
                 return_input_props: bool = False, return_output_props: bool = False,
                 return_custom_props: bool = False, return_llm_props: bool = False,
                 start_time: t.Union[datetime, int, None] = None,
                 end_time: t.Union[datetime, int, None] = None,
                 return_similarities: bool = False) -> t.Union[pd.DataFrame, None]:
        """
        Fetch all the interactions from the specified environment (PROD/EVAL) as a pandas DataFrame.

        Parameters
        ----------
        environment : EnvType | str
            The environment type from which to fetch interactions. This can be either "PROD" or "EVAL".

        version_name : str, optional
            The version name to fetch interactions from. If no version name is provided,
            the latest created version in the application will be used. This is mostly useful
            when integrating the golden set and rerunning it in the CI.

        return_annotation_data : bool, optional
            Whether to include annotation info in the data.

        return_topics : bool, optional
            Whether to include the topic in the data.

        return_input_props : bool, optional
            Whether to include input properties in the data.

        return_output_props : bool, optional
            Whether to include the output properties in the data.

        return_custom_props : bool, optional
            Whether to include custom properties in the data.

        return_llm_props : bool, optional
            Whether to include LLM properties in the data.

        start_time : datetime | int | None, optional
            The start time from which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched from the beginning.

        end_time : datetime | int | None, optional
            The end time until which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched up to the most recent.

        Returns
        -------
        pd.DataFrame | None
            A pandas DataFrame containing the interactions, or None in case of a problem retrieving the data.

        """
        golden_set_version_id = self._get_version_id(version_name)
        csv_as_text = self.api.get_interactions_csv(
            golden_set_version_id,
            environment=environment,
            start_time_epoch=get_timestamp(start_time),
            end_time_epoch=get_timestamp(end_time),
            return_topics=return_topics,
            return_annotation_data=return_annotation_data,
            return_output_props=return_output_props,
            return_custom_props=return_custom_props,
            return_input_props=return_input_props,
            return_llm_props=return_llm_props,
            return_similarities=return_similarities,
            )
        data = StringIO(csv_as_text)
        return pd.read_csv(data)

    def _get_version_id(self, version_name, create_if_not_exist=True):

        app = self.api.get_application(self.api.get_app_name())
        if not app:
            raise DeepchecksLLMClientError(f"Application: \"{self.api.get_app_name()}\", does not exist")
        if version_name:
            golden_set_version = next((ver for ver in app["versions"] if ver["name"] == version_name), None)
            if not golden_set_version:
                if not create_if_not_exist:
                    raise DeepchecksLLMClientError(
                        f"Could not find version \"{version_name}\", in application \"{self.api.get_app_name()}\"",
                    )
                else:
                    return self.api.create_application_version(
                        application_id=app["id"], version_name=version_name,
                    )["id"]

        else:
            golden_set_version = max(app["versions"], key=lambda x: x["created_at"])
            if not golden_set_version:
                raise DeepchecksLLMClientError(
                    f"Could not find versions to select from in application \"{self.api.get_app_name()}\"")
        return golden_set_version["id"]


# LLM Client publicly accessed singleton
dc_client: DeepchecksLLMClient = DeepchecksLLMClient()
