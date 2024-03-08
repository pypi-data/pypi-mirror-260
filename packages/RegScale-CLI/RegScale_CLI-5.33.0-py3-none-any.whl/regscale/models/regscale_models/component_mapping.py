""" This module contains the ComponentMapping model. """

from functools import lru_cache
from typing import Optional, List, cast
from pydantic import Field, ConfigDict
from requests import Response

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models.regscale_models import RegScaleModel, T
import logging

logger = logging.getLogger(__name__)


class ComponentMapping(RegScaleModel):
    _module_slug = "componentmapping"
    id: Optional[int] = None
    uuid: Optional[str] = None
    securityPlanId: int
    componentId: int
    createdById: str
    dateCreated: str = Field(default_factory=get_current_datetime)
    lastUpdatedById: str
    dateLastUpdated: str = Field(default_factory=get_current_datetime)
    tenantsId: int = 1
    isPublic: bool = True

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the ComponentMapping model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            filter_component_mappings="/api/{model_slug}/filterComponentMappings/{intComponent}/{intSP}/{strSearch}/{intPage}/{intPageSize}",
            delete_component_mapping_delete="/api/{model_slug}/{id}",
            find_mappings="/api/{model_slug}/findMappings/{intID}",
            get_mappings_as_components="/api/{model_slug}/getMappingsAsComponents/{intID}",
            get_mappings_as_security_plans="/api/{model_slug}/getMappingsAsSecurityPlans/{intID}",
        )

    def find_by_unique(self) -> Optional["ComponentMapping"]:  # type: ignore
        """
        Find a ComponentMapping by its unique fields

        :return: ComponentMapping object
        :rtype: Optional[T]
        """

        if not self.componentId or not self.securityPlanId:
            raise ValueError("Component ID and Security Plan ID are required")
        mappings: list[ComponentMapping] = self.find_mappings(self.securityPlanId)
        for mapping in mappings:
            if mapping.securityPlanId == self.securityPlanId:
                return mapping
        return None

    @classmethod
    @lru_cache(maxsize=None)  # Decorate with lru_cache
    def find_mappings(cls, security_plan_id: int) -> list[T]:
        """
        Find mappings for a given component

        :param int security_plan_id: Security Plan ID
        :return: List of mappings
        :rtype: list[dict]
        """
        return cls._handle_list_response(
            cls._api_handler.get(
                cls.get_endpoint("get_mappings_as_components").format(
                    intID=security_plan_id,
                )
            ),
            security_plan_id=security_plan_id,
        )

    @classmethod
    def _handle_list_response(
        cls, response: Response, security_plan_id: int
    ) -> List["ComponentMapping"]:
        """
        Handle list response

        :param response: Response from API
        :param int security_plan_id: Security Plan ID
        :type response: Response
        :return: List of ComponentMappings
        :rtype: List[ComponentMapping]
        """
        if not response or response.status_code in [204, 404]:
            return []
        if response.ok:
            json_response = response.json()
            if isinstance(json_response, dict):
                json_response = json_response.get("items", [])
            return cast(
                List[T],
                [cls(securityPlanId=security_plan_id, **o) for o in json_response],
            )
        else:
            logger.error(f"Failed to get {cls.get_module_slug()} for {cls.__name__}")
            return []
