from abc import ABC, abstractmethod
import json
import os
from typing import Dict, List, Literal, Optional, Sequence, Union, Any
import boto3

from attr import Factory, define, field
import attr
from hangar_sdk.core.constructs.base import IBuffer, IGroup, IResource, IStateManager
from hangar_sdk.core.terraform_tool import TerraformBuffer, TerraformStateManager

@define(kw_only=True)
class L1GroupBase(IGroup):
    name: str
    resources: List["L1ResourceBase"] = field(default=Factory(list))

    def __attrs_post_init__(self, **kwargs):
        self.state_manager = TerraformStateManager()
        self.buffer = TerraformBuffer(
            basepath=".hangar",
            state_manager=self.state_manager,
            group=self
        )

    def get_name(self) -> str:
        return self.name

    def resolve(self):
        resources = []
        resources += self.resources

        base_resources = []

        while len(resources) != 0:
            resource = resources.pop()

            if isinstance(resource, L1ResourceBase):
                sub_resources = resource.resolve()
                base_resources += sub_resources
            else:
                base_resources += resource

        self.buffer.add_list(self.resources)
        self.buffer.flush()

    def get_resources(self) -> Sequence[IResource]:
        return self.resources

    def add_resource(self, resource: "L1ResourceBase"):
        self.resources.append(resource)


@define(kw_only=True, slots=False)
class L1ResourceBase(IResource, ABC):
    name: str
    group: L1GroupBase
    _dependencies: list = field(default=Factory(list))

    def __attrs_post_init__(self):
        # if a field is a type of L1ResourceBase, add it to the dependencies list
        for field in attr.fields(type(self)):
            if isinstance(field.type, L1ResourceBase):
                self._dependencies.append(field.name)

        self.group.add_resource(self)

    def get_name(self) -> str:
        return self.name

    def get_type(self):
        return self.__class__.__name__

    @abstractmethod
    def resolve(self) -> Sequence[IResource]:
        pass

    def get_group(self):
        return self.group

    @property
    def state(self):
        return self.get_state(self.group.state_manager)

    def get_state(self, state_manager: IStateManager) -> Dict:
        res = {}
        for resource in self.resolve():
            rtype = resource.get_type()
            rname = resource.get_name()

            if rtype not in res:
                res[rtype] = {}

            res[rtype][rname] = state_manager.get_state(rname)

        return res