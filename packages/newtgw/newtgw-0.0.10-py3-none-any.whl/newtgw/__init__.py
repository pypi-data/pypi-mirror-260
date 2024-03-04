'''
# replace this
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import constructs as _constructs_77d1e7e8


class AcceptTransitPeering(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="newtgw.AcceptTransitPeering",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        transit_gateway_attachment_id: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param transit_gateway_attachment_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8985f300b1964da28df19093f983eab7591f05c88e6efc9f2ef34a56a7252649)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument transit_gateway_attachment_id", value=transit_gateway_attachment_id, expected_type=type_hints["transit_gateway_attachment_id"])
        jsii.create(self.__class__, self, [scope, id, transit_gateway_attachment_id])


__all__ = [
    "AcceptTransitPeering",
]

publication.publish()

def _typecheckingstub__8985f300b1964da28df19093f983eab7591f05c88e6efc9f2ef34a56a7252649(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    transit_gateway_attachment_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
