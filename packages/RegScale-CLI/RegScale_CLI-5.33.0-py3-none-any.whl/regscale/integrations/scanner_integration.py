#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Scanner Integration Class """

import concurrent.futures
import dataclasses
import logging
import threading
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Dict, Any, Iterator

from rich.progress import Progress

from regscale.core.app.utils.api_handler import APIHandler
from regscale.core.app.utils.app_utils import (
    get_current_datetime,
    create_progress_object,
)
from regscale.models import regscale_models

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class IntegrationAsset:
    """
    Dataclass for integration assets.

    Represents an asset to be integrated, including its metadata and associated components.
    If a component does not exist, it will be created based on the names provided in ``component_names``.

    :param name: The name of the asset.
    :param identifier: A unique identifier for the asset.
    :param asset_type: The type of the asset.
    :param asset_category: The category of the asset.
    :param component_type: The type of the component, defaults to ``ComponentType.Hardware``.
    :param parent_id: The ID of the parent asset, defaults to None.
    :param parent_module: The module of the parent asset, defaults to None.
    :param status: The status of the asset, defaults to "Active (On Network)".
    :param date_last_updated: The last update date of the asset, defaults to the current datetime.
    :param asset_owner_id: The ID of the asset owner, defaults to None.
    :param mac_address: The MAC address of the asset, defaults to None.
    :param fqdn: The Fully Qualified Domain Name of the asset, defaults to None.
    :param ip_address: The IP address of the asset, defaults to None.
    :param component_names: A list of strings that represent the names of the components associated with the asset, components will be created if they do not exist.
    """

    name: str
    identifier: str
    asset_type: str
    asset_category: str
    component_type: str = regscale_models.ComponentType.Hardware
    parent_id: Optional[int] = None
    parent_module: Optional[str] = None
    status: str = "Active (On Network)"
    date_last_updated: str = dataclasses.field(default_factory=get_current_datetime)
    asset_owner_id: Optional[str] = None
    mac_address: Optional[str] = None
    fqdn: Optional[str] = None
    ip_address: Optional[str] = None
    component_names: List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class IntegrationFinding:
    """
    Dataclass for integration findings.

    :param control_ids: A list of control IDs associated with the finding.
    :param title: The title of the finding.
    :param category: The category of the finding.
    :param severity: The severity of the finding, based on regscale_models.IssueSeverity.
    :param description: A description of the finding.
    :param status: The status of the finding, based on regscale_models.ControlTestResultStatus.
    :param priority: The priority of the finding, defaults to "Medium".
    :param issue_type: The type of issue, defaults to "Risk".
    :param date_created: The creation date of the finding, defaults to the current datetime.
    :param date_last_updated: The last update date of the finding, defaults to the current datetime.
    :param external_id: An external identifier for the finding, defaults to an empty string.
    :param gaps: A description of any gaps identified, defaults to an empty string.
    :param observations: Observations related to the finding, defaults to an empty string.
    :param evidence: Evidence supporting the finding, defaults to an empty string.
    :param identified_risk: The risk identified by the finding, defaults to an empty string.
    :param impact: The impact of the finding, defaults to an empty string.
    :param recommendation_for_mitigation: Recommendations for mitigating the finding, defaults to an empty string.
    """

    control_ids: List[int]
    title: str
    category: str
    severity: regscale_models.IssueSeverity
    description: str
    status: regscale_models.ControlTestResultStatus
    priority: str = "Medium"
    issue_type: str = "Risk"
    date_created: str = dataclasses.field(default_factory=get_current_datetime)
    date_last_updated: str = dataclasses.field(default_factory=get_current_datetime)
    external_id: str = ""
    gaps: str = ""
    observations: str = ""
    evidence: str = ""
    identified_risk: str = ""
    impact: str = ""
    recommendation_for_mitigation: str = ""


class ScannerIntegration(ABC):
    """
    Abstract class for scanner integrations.

    :param int plan_id: The ID of the security plan
    """

    title = "Scanner Integration"
    asset_identifier_field = ""
    severity_map = {
        0: regscale_models.IssueSeverity.Low,
        1: regscale_models.IssueSeverity.High,
        2: regscale_models.IssueSeverity.High,
        3: regscale_models.IssueSeverity.Moderate,
        4: regscale_models.IssueSeverity.Low,
    }
    component_map: dict[Any, Any] = {}
    components: list[Any] = []
    asset_map: dict[Any, Any] = {}
    asset_progress: Progress
    num_assets_to_process: Optional[int] = None

    def __init__(self, plan_id):
        """
        Initializes the scanner integration

        :param int plan_id: The ID of the security plan
        """
        self.plan_id = plan_id
        self.ci_map = regscale_models.ControlImplementation.get_control_map_by_plan(
            plan_id=plan_id
        )
        self.control_map = {v: k for k, v in self.ci_map.items()}
        self.assessment_map = {}
        self.assessor_id = self.get_assessor_id()
        self.asset_progress = create_progress_object()

    @staticmethod
    def get_assessor_id() -> str:
        """
        Gets the ID of the assessor

        :return: The ID of the assessor
        :rtype: str
        """

        api_handler = APIHandler()
        return api_handler.get_user_id()

    @abstractmethod
    def fetch_findings(self, *args, **kwargs) -> List[IntegrationFinding]:
        """
        Fetches findings from the integration

        :return: A list of findings
        :rtype: List[IntegrationFinding]
        """
        pass

    @abstractmethod
    def fetch_assets(self, *args, **kwargs) -> Iterator[IntegrationAsset]:
        """
        Fetches assets from the integration

        :return: A list of assets
        :rtype: List[IntegrationAsset]
        """
        pass

    def get_or_create_assessment(
        self, control_implementation_id: int
    ) -> regscale_models.Assessment:
        """
        Gets or creates a RegScale assessment

        :param int control_implementation_id: The ID of the control implementation
        :return: The assessment
        :rtype: regscale_models.Assessment
        """
        logger.info(
            f"Getting or creating assessment for control implementation {control_implementation_id}"
        )
        assessment: Optional[regscale_models.Assessment] = self.assessment_map.get(
            control_implementation_id
        )
        if assessment:
            logger.debug(
                f"Found cached assessment {assessment.id} for control implementation {control_implementation_id}"
            )
        else:
            logger.debug(
                f"Assessment not found for control implementation {control_implementation_id}"
            )
            assessment = regscale_models.Assessment(
                plannedStart=get_current_datetime(),
                plannedFinish=get_current_datetime(),
                status=regscale_models.AssessmentStatus.COMPLETE.value,
                assessmentResult=regscale_models.AssessmentResultsStatus.FAIL.value,
                actualFinish=get_current_datetime(),
                leadAssessorId=self.assessor_id,
                parentId=control_implementation_id,
                parentModule=regscale_models.ControlImplementation.get_module_string(),
                title=f"{self.title} Assessment",
                assessmentType=regscale_models.AssessmentType.QA_SURVEILLANCE.value,
            ).create()
        self.assessment_map[control_implementation_id] = assessment
        return assessment

    def create_issue_from_finding(
        self, control_implementation_id: int, finding: IntegrationFinding
    ) -> regscale_models.Issue:
        """
        Creates a RegScale issue from a finding

        :param int control_implementation_id: The ID of the control implementation
        :param IntegrationFinding finding: The finding data
        :return: The Issue create from the finding
        :rtype: regscale_models.Issue
        """
        return regscale_models.Issue(
            parentId=control_implementation_id,
            parentModule=regscale_models.ControlImplementation.get_module_string(),
            title=finding.title,
            dateCreated=finding.date_created,
            status=finding.status,
            severityLevel=finding.severity,
            issueOwnerId=self.assessor_id,
            securityPlanId=self.plan_id,
            identification=finding.external_id,
            dueDate=get_current_datetime(),
            description=finding.description,
        ).create()

    @staticmethod
    def update_issues_from_finding(
        issue: regscale_models.Issue, finding: IntegrationFinding
    ) -> regscale_models.Issue:
        """
        Updates RegScale issues based on the integration findings

        :param regscale_models.Issue issue: The issue to update
        :param IntegrationFinding finding: The integration findings
        :return: The updated issue
        :rtype: regscale_models.Issue
        """
        issue.status = finding.status
        issue.severityLevel = finding.severity
        issue.dateLastUpdated = finding.date_last_updated
        issue.description = finding.description
        return issue.save()

    def handle_passing_finding(
        self,
        existing_issues: List[regscale_models.Issue],
        finding: IntegrationFinding,
        control_implementation_id: int,
    ) -> None:
        """
        Handles findings that have passed by closing any open issues associated with the finding.

        :param List[regscale_models.Issue] existing_issues: The list of existing issues to check against
        :param IntegrationFinding finding: The finding data that has passed
        :param int control_implementation_id: The ID of the control implementation associated with the finding
        :return: None
        """
        for issue in existing_issues:
            if (
                issue.identification == finding.external_id
                and issue.status != regscale_models.IssueStatus.Closed
            ):
                logger.info(
                    f"Closing issue {issue.id} for control {self.control_map[control_implementation_id]}"
                )
                issue.status = regscale_models.IssueStatus.Closed
                issue.dateCompleted = finding.date_last_updated
                issue.save()

    def handle_failing_finding(
        self,
        existing_issues: List[regscale_models.Issue],
        finding: IntegrationFinding,
        control_implementation_id: int,
    ) -> None:
        """
        Handles findings that have failed by updating an existing open issue or creating a new one.

        :param List[regscale_models.Issue] existing_issues: The list of existing issues to check against
        :param IntegrationFinding finding: The finding data that has failed
        :param int control_implementation_id: The ID of the control implementation associated with the finding
        :return: None
        """
        found_issue = None
        for issue in existing_issues:
            if (
                issue.identification == finding.external_id
                and issue.status != regscale_models.IssueStatus.Closed
            ):
                logger.info(
                    f"Updating issue {issue.id} for control {self.control_map[control_implementation_id]}"
                )
                found_issue = self.update_issues_from_finding(
                    issue=issue, finding=finding
                )
                break
        if not found_issue:
            # Create a new issue if one doesn't exist
            logger.info(
                f"Creating issue for control {self.control_map[control_implementation_id]}"
            )
            self.create_issue_from_finding(control_implementation_id, finding)

    def update_regscale_findings(self, findings: List[IntegrationFinding]) -> None:
        """
        Updates RegScale findings based on the integration findings

        :param List[IntegrationFinding] findings: The integration findings
        :return: None
        """
        for finding in findings:
            if finding:
                for control_implementation_id in finding.control_ids:
                    assessment = self.get_or_create_assessment(
                        control_implementation_id
                    )
                    control_test = regscale_models.ControlTest(
                        uuid=finding.external_id,
                        parentControlId=control_implementation_id,
                        testCriteria=finding.description,
                    ).get_or_create()
                    regscale_models.ControlTestResult(
                        parentTestId=control_test.id,
                        parentAssessmentId=assessment.id,
                        uuid=finding.external_id,
                        result=finding.status,
                        dateAssessed=finding.date_created,
                        assessedById=self.assessor_id,
                        gaps=finding.gaps,
                        observations=finding.observations,
                        evidence=finding.evidence,
                        identifiedRisk=finding.identified_risk,
                        impact=finding.impact,
                        recommendationForMitigation=finding.recommendation_for_mitigation,
                    ).create()
                    logger.info(
                        f"Created or Updated assessment {assessment.id} for control "
                        f"{self.control_map[control_implementation_id]}"
                    )
                    existing_issues: list[regscale_models.Issue] = (
                        regscale_models.Issue.get_all_by_parent(
                            parent_id=control_implementation_id,
                            parent_module=regscale_models.ControlImplementation.get_module_string(),
                        )
                    )
                    if finding.status == regscale_models.ControlTestResultStatus.PASS:
                        self.handle_passing_finding(
                            existing_issues, finding, control_implementation_id
                        )
                    else:
                        self.handle_failing_finding(
                            existing_issues, finding, control_implementation_id
                        )

    def get_components(self) -> List[regscale_models.Component]:
        """
        Get all components from the integration

        :return: A dictionary of components
        :rtype: dict
        """
        if any(self.components):
            return self.components
        self.components = regscale_models.Component.get_all_by_parent(
            parent_id=self.plan_id,
            parent_module=regscale_models.SecurityPlan.get_module_string(),
        )
        return self.components

    def get_component_by_title(self) -> dict:
        """
        Get all components from the integration

        :return: A dictionary of components
        :rtype: dict
        """
        return {component.title: component for component in self.get_components()}

    def set_asset_defaults(self, asset):
        """
        Set default values for the asset

        :param IntegrationAsset asset: The integration asset
        :return: The asset with which defaults should been set
        :rtype: IntegrationAsset
        """
        if not asset.asset_owner_id:
            asset.asset_owner_id = self.get_assessor_id()
        if not asset.status:
            asset.status = "Active (On Network)"
        return asset

    def update_regscale_assets(self, assets: Iterator[IntegrationAsset]) -> None:
        """
        Updates RegScale assets based on the integration assets

        :param Iterator[IntegrationAsset] assets: The integration assets
        :return: None
        :rtype: None
        """

        logger.info("Updating RegScale assets...")
        loading_assets = self.asset_progress.add_task(
            f"[#f8b737]Creating and updating assets from {self.title}.",
        )
        progress_lock = threading.Lock()
        # Look up Component by title
        components_by_title = self.get_component_by_title()

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_asset = {
                executor.submit(
                    self.process_asset,
                    asset,
                    components_by_title,
                    loading_assets,
                    progress_lock,
                ): asset
                for asset in assets
            }
            for future in concurrent.futures.as_completed(future_to_asset):
                asset = future_to_asset[future]
                try:
                    future.result()
                except Exception as exc:
                    logger.error(f"{asset.name} generated an exception: {exc}")

    def process_asset(
        self,
        asset: IntegrationAsset,
        components_by_title: dict,
        loading_assets,
        progress_lock,
    ) -> None:
        """
        Processes an asset

        :param IntegrationAsset asset: The integration asset
        :param dict components_by_title: The components by title
        :param int loading_assets: The loading assets task
        :param threading.Lock progress_lock: The progress lock
        :return: None
        :rtype: None
        """

        asset = self.set_asset_defaults(asset)
        for component_name in asset.component_names:
            logger.info(f"Checking for existing assets under {component_name}...")
            if not (component := components_by_title.get(component_name)):
                component = regscale_models.Component(
                    title=component_name,
                    componentType=asset.component_type,
                    securityPlansId=self.plan_id,
                    description=component_name,
                    componentOwnerId=self.get_assessor_id(),
                ).create()
                self.components.append(component)
                if component.securityPlansId:
                    regscale_models.ComponentMapping(
                        componentId=component.id,
                        securityPlanId=component.securityPlansId,
                    ).get_or_create()
            components_by_title[component_name] = component
            existing_assets = self.asset_map.get(
                component.id
            ) or regscale_models.Asset.get_all_by_parent(
                parent_id=component.id,
                parent_module=regscale_models.Component.get_module_string(),
            )
            self.asset_map[component.id] = existing_assets
            self.update_or_create_asset(asset, existing_assets, component)
            with progress_lock:
                # Wait until self.num_assets_to_process is set to set task total.
                if self.num_assets_to_process and self.asset_progress.tasks[
                    loading_assets
                ].total != float(self.num_assets_to_process):
                    self.asset_progress.update(
                        loading_assets, total=self.num_assets_to_process
                    )
                self.asset_progress.advance(loading_assets, 1)

    def update_or_create_asset(
        self,
        asset: IntegrationAsset,
        existing_assets: List[regscale_models.Asset],
        component: regscale_models.Component,
    ) -> None:
        """
        Updates an existing asset or creates a new one

        :param IntegrationAsset asset: The integration asset
        :param List[regscale_models.Asset] existing_assets: The existing assets
        :return: None
        """
        found_asset = self.find_existing_asset(asset, existing_assets)

        if found_asset:
            self.update_asset_if_needed(asset, found_asset)
        else:
            self.create_new_asset(asset, component=component)

    def find_existing_asset(
        self, asset: IntegrationAsset, existing_assets: List[regscale_models.Asset]
    ) -> Optional[regscale_models.Asset]:
        """
        Finds an existing asset that matches the integration asset

        :param IntegrationAsset asset: The integration asset
        :param List[regscale_models.Asset] existing_assets: The existing assets
        :return: The matching existing asset, or None if no match is found
        :rtype: Optional[regscale_models.Asset]
        """
        for existing_asset in existing_assets:
            if asset.identifier == getattr(existing_asset, self.asset_identifier_field):
                return existing_asset
        return None

    @staticmethod
    def update_asset_if_needed(
        asset: IntegrationAsset, existing_asset: regscale_models.Asset
    ) -> None:
        """
        Updates an existing asset if any of its fields differ from the integration asset

        :param IntegrationAsset asset: The integration asset
        :param regscale_models.Asset existing_asset: The existing asset
        :return: None
        """
        is_updated = False
        if existing_asset.assetOwnerId != asset.asset_owner_id:
            existing_asset.assetOwnerId = asset.asset_owner_id
            is_updated = True
        if existing_asset.parentId != asset.parent_id:
            existing_asset.parentId = asset.parent_id
            is_updated = True
        if existing_asset.parentModule != asset.parent_module:
            existing_asset.parentModule = asset.parent_module
            is_updated = True
        if existing_asset.assetType != asset.asset_type:
            existing_asset.assetType = asset.asset_type
            is_updated = True
        if existing_asset.status != asset.status:
            existing_asset.status = asset.status
            is_updated = True
        if existing_asset.assetCategory != asset.asset_category:
            existing_asset.assetCategory = asset.asset_category
            is_updated = True

        if is_updated:
            existing_asset.dateLastUpdated = asset.date_last_updated
            existing_asset.save()
            logger.info(f"Updated asset {asset.identifier}")
        else:
            logger.info(f"Asset {asset.identifier} is already up to date")

    def create_new_asset(
        self, asset: IntegrationAsset, component: regscale_models.Component
    ) -> None:
        """
        Creates a new asset based on the integration asset

        :param IntegrationAsset asset: The integration asset
        :param regscale_models.Component component: The component
        :return: None
        """
        new_asset = regscale_models.Asset(
            name=asset.name,
            assetOwnerId=asset.asset_owner_id,
            parentId=component.id,
            parentModule=regscale_models.Component.get_module_string(),
            assetType=asset.asset_type,
            dateLastUpdated=asset.date_last_updated,
            status=asset.status,
            assetCategory=asset.asset_category,
        )
        if self.asset_identifier_field:
            setattr(new_asset, self.asset_identifier_field, asset.identifier)
        new_asset = new_asset.create()
        regscale_models.AssetMapping(
            assetId=new_asset.id,
            componentId=component.id,
        ).get_or_create()
        logger.info(f"Created asset {asset.identifier}")

    @classmethod
    def sync_findings(cls, plan_id: int, **kwargs) -> None:
        """
        Syncs findings from the integration to RegScale

        :param int plan_id: The ID of the security plan
        :return: None
        """
        logger.info(f"Syncing {cls.title} findings...")
        instance = cls(plan_id)
        instance.update_regscale_findings(findings=instance.fetch_findings(**kwargs))

    @classmethod
    def sync_assets(cls, plan_id: int, **kwargs) -> None:
        """
        Syncs assets from the integration to RegScale

        :param int plan_id: The ID of the security plan
        :param Path path: The path to the stig files
        :return: None
        """
        logger.info(f"Syncing {cls.title} assets...")
        instance = cls(plan_id)
        instance.asset_progress = create_progress_object()
        with instance.asset_progress:
            instance.update_regscale_assets(assets=instance.fetch_assets(**kwargs))
