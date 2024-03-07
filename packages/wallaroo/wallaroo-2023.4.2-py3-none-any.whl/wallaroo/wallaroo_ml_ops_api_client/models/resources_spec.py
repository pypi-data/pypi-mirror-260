from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.architecture import Architecture
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.resource_spec import ResourceSpec





T = TypeVar("T", bound="ResourcesSpec")


@attr.s(auto_attribs=True)
class ResourcesSpec:
    """ 
        Attributes:
            limits (ResourceSpec):
            requests (ResourceSpec):
            arch (Union[Unset, Architecture]): Processor architecture to execute on
            gpu (Union[Unset, bool]):
            image (Union[Unset, None, str]):
     """

    limits: 'ResourceSpec'
    requests: 'ResourceSpec'
    arch: Union[Unset, Architecture] = UNSET
    gpu: Union[Unset, bool] = UNSET
    image: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        limits = self.limits.to_dict()

        requests = self.requests.to_dict()

        arch: Union[Unset, str] = UNSET
        if not isinstance(self.arch, Unset):
            arch = self.arch.value

        gpu = self.gpu
        image = self.image

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "limits": limits,
            "requests": requests,
        })
        if arch is not UNSET:
            field_dict["arch"] = arch
        if gpu is not UNSET:
            field_dict["gpu"] = gpu
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.resource_spec import ResourceSpec
        d = src_dict.copy()
        limits = ResourceSpec.from_dict(d.pop("limits"))




        requests = ResourceSpec.from_dict(d.pop("requests"))




        _arch = d.pop("arch", UNSET)
        arch: Union[Unset, Architecture]
        if isinstance(_arch,  Unset):
            arch = UNSET
        else:
            arch = Architecture(_arch)




        gpu = d.pop("gpu", UNSET)

        image = d.pop("image", UNSET)

        resources_spec = cls(
            limits=limits,
            requests=requests,
            arch=arch,
            gpu=gpu,
            image=image,
        )

        resources_spec.additional_properties = d
        return resources_spec

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
