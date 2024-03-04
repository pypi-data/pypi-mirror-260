'''
# Appflow Patterns - a library to facilitate data flows

This library aims at simplifying the task of setting up data flows between SaaS like SharePoint and S3.

This library is  written using the wonderful [projen](https://github.com/projen/projen) framework.

Note: this library is just the result of some personal experimentation. It is not an official AWS library and is not supported by AWS!

# Installation

The library is available on npmjs.com and can be installed using:

`npm i dms-patterns`

And on pypi:

`pip install dms-patterns`

# Usage Examples

## Sharepoint to S3

This example creates a scheduled and ondemand flow from a sharepoint site to an s3 bucket.

```python
import { Sharepoint2S3Flow } from '../src/appflow-patterns/sharepoint2s3';


export class Sharepoint2S3Stack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: cdk.StackProps) {
    super(scope, id, props);

    const bucket = new s3.Bucket(this, 'Bucket', {
      bucketName: 'my-bucket',
    });

    new Sharepoint2S3Flow(this, 'Sharepoint2S3Flow', {
      site: 'sites/${siteName},${siteID},${webID}',
      entities: ['${site}/_api/v2.0/drive/root:/path/to/folder'],
      profileArn: 'arn:aws:appflow:us-east-1:123456789012:connector-profile/12345678-1234-1234-1234-123456789012',
      bucketName: bucket.bucketName,
      scheduleExpression: 'rate(12 hour)',
    });

  }
}
```

Currently, only carbon-based entities are supported due to a limitation of AWS Appflow.
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


class Sharepoint2S3Flow(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="appflow-patterns.Sharepoint2S3Flow",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_name: builtins.str,
        entities: typing.Sequence[builtins.str],
        profile_arn: builtins.str,
        site: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
        schedule_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_name: 
        :param entities: 
        :param profile_arn: 
        :param site: 
        :param prefix: 
        :param schedule_expression: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eab6bf2e8abcb9667c7e568c7c7bce83299e9017a6441fcd99caeee22887321)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Sharepoint2S3FlowProps(
            bucket_name=bucket_name,
            entities=entities,
            profile_arn=profile_arn,
            site=site,
            prefix=prefix,
            schedule_expression=schedule_expression,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="appflow-patterns.Sharepoint2S3FlowProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "entities": "entities",
        "profile_arn": "profileArn",
        "site": "site",
        "prefix": "prefix",
        "schedule_expression": "scheduleExpression",
    },
)
class Sharepoint2S3FlowProps:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        entities: typing.Sequence[builtins.str],
        profile_arn: builtins.str,
        site: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
        schedule_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: 
        :param entities: 
        :param profile_arn: 
        :param site: 
        :param prefix: 
        :param schedule_expression: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905079eb24fa7315d14540896abd511c1be362d9c562450f55e42dc5b2841354)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument entities", value=entities, expected_type=type_hints["entities"])
            check_type(argname="argument profile_arn", value=profile_arn, expected_type=type_hints["profile_arn"])
            check_type(argname="argument site", value=site, expected_type=type_hints["site"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "entities": entities,
            "profile_arn": profile_arn,
            "site": site,
        }
        if prefix is not None:
            self._values["prefix"] = prefix
        if schedule_expression is not None:
            self._values["schedule_expression"] = schedule_expression

    @builtins.property
    def bucket_name(self) -> builtins.str:
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entities(self) -> typing.List[builtins.str]:
        result = self._values.get("entities")
        assert result is not None, "Required property 'entities' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def profile_arn(self) -> builtins.str:
        result = self._values.get("profile_arn")
        assert result is not None, "Required property 'profile_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def site(self) -> builtins.str:
        result = self._values.get("site")
        assert result is not None, "Required property 'site' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_expression(self) -> typing.Optional[builtins.str]:
        result = self._values.get("schedule_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sharepoint2S3FlowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Sharepoint2S3Flow",
    "Sharepoint2S3FlowProps",
]

publication.publish()

def _typecheckingstub__3eab6bf2e8abcb9667c7e568c7c7bce83299e9017a6441fcd99caeee22887321(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_name: builtins.str,
    entities: typing.Sequence[builtins.str],
    profile_arn: builtins.str,
    site: builtins.str,
    prefix: typing.Optional[builtins.str] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905079eb24fa7315d14540896abd511c1be362d9c562450f55e42dc5b2841354(
    *,
    bucket_name: builtins.str,
    entities: typing.Sequence[builtins.str],
    profile_arn: builtins.str,
    site: builtins.str,
    prefix: typing.Optional[builtins.str] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
