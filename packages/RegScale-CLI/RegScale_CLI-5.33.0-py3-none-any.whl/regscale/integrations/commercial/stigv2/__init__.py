#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" RegScale GCP Package """
from pathlib import Path
from typing import List, Iterator, Optional

import click

from regscale.integrations.commercial.stigv2.ckl_parser import (
    parse_checklist,
    get_all_components_from_checklists,
    get_all_assets_from_checklists,
    find_stig_files,
)
from regscale.integrations.scanner_integration import (
    logger,
    IntegrationFinding,
    ScannerIntegration,
    IntegrationAsset,
)
from regscale.models import regscale_models
from regscale.models.regscale_models import AssetType


class StigIntegration(ScannerIntegration):
    title = "STIG Integration"
    asset_identifier_field = "fqdn"

    def fetch_findings(self, path: Optional[Path] = None) -> List[IntegrationFinding]:
        """
        Fetches GCP findings using the SecurityCenterClient

        :return: A list of parsed findings
        :rtype: List[IntegrationFinding]
        """
        findings: List[IntegrationFinding] = []
        return findings

    def fetch_assets(self, path: Optional[Path] = None) -> Iterator[IntegrationAsset]:
        """
        Fetches GCP assets using the AssetServiceClient

        :return: An iterator of parsed assets
        :rtype: Iterator[IntegrationAsset]
        """
        if not path:
            raise ValueError("Path to STIG files is required.")
        logger.info("Fetching assets...")
        stig_files = find_stig_files(path)

        self.num_assets_to_process = len(stig_files)

        loading_stig_files = self.asset_progress.add_task(
            f"[#f8b737]Loading {len(stig_files)} STIG files.",
            total=len(stig_files),
        )
        for stig_file in stig_files:
            logger.info(f"Processing '{stig_file}'")
            checklist = parse_checklist(stig_file)
            for stig_asset in checklist.assets:
                component_names = []
                for stig in checklist.stigs:
                    component_names.append(stig.component_title)

                if not stig_asset.host_name or not stig_asset.host_fqdn:
                    logger.error(f"Failed to extract asset from {stig_asset}")
                    continue

                yield IntegrationAsset(
                    name=stig_asset.host_name,
                    identifier=stig_asset.host_fqdn,
                    asset_type=AssetType.Other,
                    asset_owner_id=self.assessor_id,
                    parent_id=self.plan_id,
                    parent_module=regscale_models.SecurityPlan.get_module_slug(),
                    asset_category="STIG",
                    component_names=component_names,
                    # TODO: Determine correct component type
                    component_type=regscale_models.ComponentType.Software,
                )
            self.asset_progress.update(loading_stig_files, advance=1)


@click.group()
def stigv2():
    """STIG Integrations"""


@stigv2.command(name="sync_findings")
@click.option(
    "-p",
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
@click.option(
    "-d",
    "--stig_directory",
    type=click.Path(exists=True),
    help="The directory where STIG files are located",
    prompt="Enter STIG directory",
    required=True,
)
def sync_findings(regscale_ssp_id, stig_directory):
    """Sync GCP Findings to RegScale."""
    StigIntegration.sync_findings(plan_id=regscale_ssp_id, path=stig_directory)


@stigv2.command(name="sync_assets")
@click.option(
    "-p",
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
@click.option(
    "-d",
    "--stig_directory",
    type=click.Path(exists=True),
    help="The directory where STIG files are located",
    prompt="Enter STIG directory",
    required=True,
)
def sync_assets(regscale_ssp_id, stig_directory):
    """Sync GCP Assets to RegScale."""
    StigIntegration.sync_assets(plan_id=regscale_ssp_id, path=stig_directory)
