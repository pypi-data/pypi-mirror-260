#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Model for Control Test in the application """

from typing import Optional

from pydantic import ConfigDict

from regscale.models.regscale_models import RegScaleModel


class ControlTest(RegScaleModel):
    """Properties plan model"""

    _module_slug = "controltests"
    _unique_fields = ["uuid"]

    id: int = 0
    isPublic: bool = True
    uuid: str
    testCriteria: str
    parentControlId: int
    parentRequirementId: int = 0

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Function to get additional endpoints for the ControlTest model

        :return: Additional endpoints for the ControlTest model
        :rtype: ConfigDict
        """
        return ConfigDict(get_all_by_parent="/api/{model_slug}/getByControl/{intParentID}")  # type: ignore

    def find_by_unique(self) -> Optional["ControlTest"]:
        """
        Find an object by unique query.

        :return: The object if found, None if not
        :rtype: Optional[ControlTest]
        """

        for instance in self.get_all_by_parent(
            parent_id=self.parentControlId, parent_module=""
        ):
            if instance.uuid == self.uuid:
                return instance
        return None
