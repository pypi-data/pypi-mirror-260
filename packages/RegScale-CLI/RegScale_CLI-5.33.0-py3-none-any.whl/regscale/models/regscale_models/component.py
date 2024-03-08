#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Model for a RegScale Component """
import logging
from enum import Enum
from typing import Optional, Any, Union, Dict, List
from pydantic import ConfigDict, Field
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models.regscale_models.regscale_model import RegScaleModel, T

logger = logging.getLogger(__name__)


class ComponentType(str, Enum):
    """Component Type Enum"""

    Hardware = "hardware"
    Software = "software"
    Service = "service"
    Policy = "policy"
    Process = "process"
    Procedure = "procedure"
    ComplianceArtifact = "compliance artifact"


class ComponentStatus(str, Enum):
    """Component Status Enum"""

    DraftPending = "Draft/Pending"
    Active = "Active"
    InactiveRetired = "Inactive/Retired"
    Cancelled = "Cancelled"
    UndergoingMajorModification = "Undergoing Major Modification"
    Other = "Other"


class ComponentList(RegScaleModel):
    id: Optional[int]
    title: Optional[str]
    status: Optional[str]
    exclude: Optional[bool]
    componentType: Optional[str]


class Component(RegScaleModel):
    """Component Model"""

    _module_slug = "components"
    _unique_fields = ["title", "securityPlansId"]

    title: str
    description: str
    componentType: Union[ComponentType, str]
    status: Union[ComponentStatus, str] = ComponentStatus.Active
    id: int = 0
    securityPlansId: Optional[int] = None
    defaultAssessmentDays: int = 0
    purpose: Optional[str] = None
    cmmcAssetType: Optional[str] = None
    createdById: str = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: str = Field(default_factory=get_current_datetime)
    lastUpdatedById: str = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateLastUpdated: str = Field(default_factory=get_current_datetime)
    uuid: Optional[str] = None
    componentOwnerId: str = Field(
        default_factory=RegScaleModel._api_handler.get_user_id
    )
    cmmcExclusion: bool = False
    externalId: Optional[str] = None
    isPublic: bool = True
    externalId: Optional[str] = None

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the Components model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(  # type: ignore
            get_list="/api/{model_slug}/getList",
            get_all_by_parent="/api/{model_slug}/getAllByParent/{intParentID}",
            get_count="/api/{model_slug}/getCount",
            graph="/api/{model_slug}/graph",
            graph_by_date="/api/{model_slug}/graphByDate/{strGroupBy}",
            report="/api/{model_slug}/report/{strReport}",
            filter_components="/api/{model_slug}/filterComponents",
            filter_component_dashboard="/api/{model_slug}/filterComponentDashboard",
            query_by_custom_field="/api/{model_slug}/queryByCustomField/{strFieldName}/{strValue}",
            get="/api/{model_slug}/find/{id}",
            evidence="/api/{model_slug}/evidence/{intID}",
            find_by_guid="/api/{model_slug}/findByGUID/{strGUID}",
            find_by_external_id="/api/{model_slug}/findByExternalId/{strID}",
            get_titles="/api/{model_slug}/getTitles",
            main_dashboard="/api/{model_slug}/mainDashboard/{intYear}",
            component_dashboard="/api/{model_slug}/componentDashboard/{intYear}",
            oscal="/api/{model_slug}/oscal/{intID}",
            statusboard="/api/{model_slug}/statusboard/{intID}/{strSearch}/{intPage}/{pageSize}",
            emass_export="/api/{model_slug}/emassExport/{intID}",
            mega_api="/api/{model_slug}/megaAPI/{intId}",
        )

    def __eq__(self, other) -> bool:
        """
        Check if two Component objects are equal

        :param other: Component object to compare
        :return: True if equal, False if not
        :rtype: bool
        """
        return (
            self.title == other.title
            and self.description == other.description
            and self.componentType == other.componentType
        )

    def __hash__(self) -> int:
        """
        Hash a Component object

        :return: Hashed Component object
        :rtype: int
        """
        return hash((self.title, self.description, self.componentType))

    def __getitem__(self, key: Any) -> Any:
        """
        Get attribute from Pipeline

        :param Any key: Key to get value for
        :return: value of provided key
        :rtype: Any
        """
        if getattr(self, key) == "None":
            return None
        return getattr(self, key)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set attribute in Pipeline with provided key

        :param Any key: Key to change to provided value
        :param Any value: New value for provided Key
        :return: None
        """
        return setattr(self, key, value)

    @staticmethod
    def get_components_from_ssp(app: Application, ssp_id: int) -> list[dict]:
        """
        Get all components for a given SSP

        :param Application app: Application instance
        :param int ssp_id: RegScale SSP
        :return: List of component dictionaries
        :rtype: list[dict]
        """
        api = Api()
        existing_res = api.get(
            app.config["domain"] + f"/api/components/getAllByParent/{ssp_id}"
        )
        existing_res.raise_for_status()
        return existing_res.json()

    @classmethod
    def get_list(cls) -> List[ComponentList]:
        """
        Retrieves a list of items for the model.
        :return: A list of items or None
        """
        response = cls._model_api_handler.get(
            endpoint=cls.get_endpoint("get_list").format(model_slug=cls._model_slug)
        )
        if not response or response.status_code in [204, 404]:
            return []
        if response and response.ok:
            return [ComponentList(**item) for item in response.json()]
        return []

    @classmethod
    def filter_components(cls, params: Dict) -> List["Component"]:
        """
        Retrieves a list of items for the model.
        :param Dict params: The parameters to filter the components
        :return: A list of Components or None
        """
        response = cls._model_api_handler.post(
            endpoint=cls.get_endpoint("filter_components").format(
                model_slug=cls._model_slug
            ),
            data=params,
        )
        if not response or response.status_code in [204, 404]:
            return []
        if response and response.ok:
            items = response.json().get("items")
            return [cls.get_object(object_id=item.get("id")) for item in items]
        return []
