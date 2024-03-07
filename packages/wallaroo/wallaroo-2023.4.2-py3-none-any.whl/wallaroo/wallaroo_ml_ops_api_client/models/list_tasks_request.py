from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListTasksRequest")


@attr.s(auto_attribs=True)
class ListTasksRequest:
    """ 
        Attributes:
            workspace_id (int):
            killed (Union[Unset, None, bool]):
            orch_id (Union[Unset, None, str]):
            orch_sha (Union[Unset, None, str]):
            run_limit (Union[Unset, None, int]):
     """

    workspace_id: int
    killed: Union[Unset, None, bool] = UNSET
    orch_id: Union[Unset, None, str] = UNSET
    orch_sha: Union[Unset, None, str] = UNSET
    run_limit: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        killed = self.killed
        orch_id = self.orch_id
        orch_sha = self.orch_sha
        run_limit = self.run_limit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspace_id": workspace_id,
        })
        if killed is not UNSET:
            field_dict["killed"] = killed
        if orch_id is not UNSET:
            field_dict["orch_id"] = orch_id
        if orch_sha is not UNSET:
            field_dict["orch_sha"] = orch_sha
        if run_limit is not UNSET:
            field_dict["run_limit"] = run_limit

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        killed = d.pop("killed", UNSET)

        orch_id = d.pop("orch_id", UNSET)

        orch_sha = d.pop("orch_sha", UNSET)

        run_limit = d.pop("run_limit", UNSET)

        list_tasks_request = cls(
            workspace_id=workspace_id,
            killed=killed,
            orch_id=orch_id,
            orch_sha=orch_sha,
            run_limit=run_limit,
        )

        list_tasks_request.additional_properties = d
        return list_tasks_request

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
