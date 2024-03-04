'''
# CDK IAM Utilities

Work in progress.

* Breaking changes may occur.
* Not all types are exported
* Some parts are not yet tested

## Developer Notes

The general idea is that the utilities in this library can serve as building blocks for composing other utilities that ideally should aid the existing aws-iam library in certain situations.

This library has been developed in context with [catnekaise/actions-constructs](https://github.com/catnekaise/actions-constructs) and a yet unreleased thing.

## Constraints

In the context of this library, constraining is the act of appending an existing `iam.PolicyStatement` (or via `iam.Grant`) with conditions. **One** constraint may conditionally add `none`, `one` or `many` conditions to the underlying `iam.PolicyStatement`.

The goal of constraints is to simplify working with the condition block of a policy when many conditions are being added, and to help make working with the conditions contextual to what is being accomplished. Example usage of this should be available *soon️* in [catnekaise/actions-constructs](https://github.com/catnekaise/actions-constructs).
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@catnekaise/cdk-iam-utilities.ArnConditionOperator")
class ArnConditionOperator(enum.Enum):
    '''
    :stability: experimental
    '''

    ARN_EQUALS = "ARN_EQUALS"
    '''
    :stability: experimental
    '''
    ARN_LIKE = "ARN_LIKE"
    '''
    :stability: experimental
    '''
    ARN_NOT_EQUALS = "ARN_NOT_EQUALS"
    '''
    :stability: experimental
    '''
    ARN_NOT_LIKE = "ARN_NOT_LIKE"
    '''
    :stability: experimental
    '''
    ARN_EQUALS_IFEXISTS = "ARN_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    ARN_LIKE_IFEXISTS = "ARN_LIKE_IFEXISTS"
    '''
    :stability: experimental
    '''
    ARN_NOT_EQUALS_IFEXISTS = "ARN_NOT_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    ARN_NOT_LIKE_IFEXISTS = "ARN_NOT_LIKE_IFEXISTS"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="@catnekaise/cdk-iam-utilities.CalledViaServicePrincipal")
class CalledViaServicePrincipal(enum.Enum):
    '''
    :stability: experimental
    '''

    AOSS = "AOSS"
    '''
    :stability: experimental
    '''
    ATHENA = "ATHENA"
    '''
    :stability: experimental
    '''
    BACKUP = "BACKUP"
    '''
    :stability: experimental
    '''
    CLOUD9 = "CLOUD9"
    '''
    :stability: experimental
    '''
    CLOUDFORMATION = "CLOUDFORMATION"
    '''
    :stability: experimental
    '''
    DATABREW = "DATABREW"
    '''
    :stability: experimental
    '''
    DATAEXCHANGE = "DATAEXCHANGE"
    '''
    :stability: experimental
    '''
    DYNAMODB = "DYNAMODB"
    '''
    :stability: experimental
    '''
    IMAGEBUILDER = "IMAGEBUILDER"
    '''
    :stability: experimental
    '''
    KMS = "KMS"
    '''
    :stability: experimental
    '''
    MGN = "MGN"
    '''
    :stability: experimental
    '''
    NIMBLE = "NIMBLE"
    '''
    :stability: experimental
    '''
    OMICS = "OMICS"
    '''
    :stability: experimental
    '''
    RAM = "RAM"
    '''
    :stability: experimental
    '''
    ROBOMAKER = "ROBOMAKER"
    '''
    :stability: experimental
    '''
    SERVICECATALOG_APPREGISTRY = "SERVICECATALOG_APPREGISTRY"
    '''
    :stability: experimental
    '''
    SQLWORKBENCH = "SQLWORKBENCH"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@catnekaise/cdk-iam-utilities.Claim",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tag_name": "tagName"},
)
class Claim:
    def __init__(self, *, name: builtins.str, tag_name: builtins.str) -> None:
        '''
        :param name: (experimental) Name represents the original value of the claim/attribute.
        :param tag_name: (experimental) Tag Name is name of the tag corresponding to name. It can either match name or be a different value

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab25c6309333e6584c398c621174042fdfb5012f94c17be42b53ab2cc9b266dc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "tag_name": tag_name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name represents the original value of the claim/attribute.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_name(self) -> builtins.str:
        '''(experimental) Tag Name is name of the tag corresponding to name.

        It can either match name or be a different value

        :stability: experimental
        '''
        result = self._values.get("tag_name")
        assert result is not None, "Required property 'tag_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Claim(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@catnekaise/cdk-iam-utilities.ClaimsIamResourcePathBuilderSettings",
    jsii_struct_bases=[],
    name_mapping={"claims_context": "claimsContext"},
)
class ClaimsIamResourcePathBuilderSettings:
    def __init__(self, *, claims_context: "IClaimsContext") -> None:
        '''
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0317f73650c04e91692ffec0edb82d3ce0a71629f2f57aa04cda5688fe984661)
            check_type(argname="argument claims_context", value=claims_context, expected_type=type_hints["claims_context"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claims_context": claims_context,
        }

    @builtins.property
    def claims_context(self) -> "IClaimsContext":
        '''
        :stability: experimental
        '''
        result = self._values.get("claims_context")
        assert result is not None, "Required property 'claims_context' is missing"
        return typing.cast("IClaimsContext", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClaimsIamResourcePathBuilderSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClaimsUtility(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.ClaimsUtility",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="forContext")
    @builtins.classmethod
    def for_context(cls, context: "IClaimsContext") -> "ClaimsUtility":
        '''
        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a356deb85e8c63ad361d1eb5f7e12a40c7326a862c7032f99a3a1553b91c1ba5)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast("ClaimsUtility", jsii.sinvoke(cls, "forContext", [context]))

    @jsii.member(jsii_name="principalTagCondition")
    def principal_tag_condition(
        self,
        claim: builtins.str,
    ) -> "AwsPrincipalTagConditionKey":
        '''
        :param claim: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5718b11866e4b3aab2dc7baa7263d4d6318f667c4a5d8d104785d87635d22e)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
        return typing.cast("AwsPrincipalTagConditionKey", jsii.invoke(self, "principalTagCondition", [claim]))

    @jsii.member(jsii_name="requestTagCondition")
    def request_tag_condition(self, claim: builtins.str) -> "AwsRequestTagConditionKey":
        '''
        :param claim: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0583a87b24d891bb0df6eb7993caa44fd2374e6676bd75f4db18d4e1f1881043)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
        return typing.cast("AwsRequestTagConditionKey", jsii.invoke(self, "requestTagCondition", [claim]))

    @jsii.member(jsii_name="tagName")
    def tag_name(
        self,
        scope: _constructs_77d1e7e8.Construct,
        claim: builtins.str,
    ) -> builtins.str:
        '''
        :param scope: -
        :param claim: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8f0353c4210b3f52c4d274ae44921c9f937056c0c47c95c50b029eadbaf2be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
        return typing.cast(builtins.str, jsii.invoke(self, "tagName", [scope, claim]))

    @jsii.member(jsii_name="tagNameForClaim")
    def tag_name_for_claim(self, claim: builtins.str) -> builtins.str:
        '''
        :param claim: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ac86b0aed994242823fe1a55a5b5f1ad2ccb2bae3b64bc7fcee64891a6ed71)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
        return typing.cast(builtins.str, jsii.invoke(self, "tagNameForClaim", [claim]))

    @builtins.property
    @jsii.member(jsii_name="knownClaims")
    def known_claims(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "knownClaims"))

    @builtins.property
    @jsii.member(jsii_name="mappedClaims")
    def mapped_claims(self) -> "IMappedClaims":
        '''
        :stability: experimental
        '''
        return typing.cast("IMappedClaims", jsii.get(self, "mappedClaims"))


class ConditionKey(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/cdk-iam-utilities.ConditionKey",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        name: builtins.str,
        *,
        supported_operators: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: -
        :param supported_operators: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5412030d13299c5c30b54c36b080e24f1f859865109b8669b52374f6252be1d1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        settings = ConditionKeySettings(supported_operators=supported_operators)

        jsii.create(self.__class__, self, [name, settings])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "ConditionKeySettings":
        '''
        :stability: experimental
        '''
        return typing.cast("ConditionKeySettings", jsii.get(self, "settings"))


class _ConditionKeyProxy(ConditionKey):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ConditionKey).__jsii_proxy_class__ = lambda : _ConditionKeyProxy


@jsii.data_type(
    jsii_type="@catnekaise/cdk-iam-utilities.ConditionKeySettings",
    jsii_struct_bases=[],
    name_mapping={"supported_operators": "supportedOperators"},
)
class ConditionKeySettings:
    def __init__(self, *, supported_operators: typing.Sequence[builtins.str]) -> None:
        '''
        :param supported_operators: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d15eae8e900b27091d34838b9120d39b07b555eb7d984f5943081e6ae2300d)
            check_type(argname="argument supported_operators", value=supported_operators, expected_type=type_hints["supported_operators"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "supported_operators": supported_operators,
        }

    @builtins.property
    def supported_operators(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("supported_operators")
        assert result is not None, "Required property 'supported_operators' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionKeySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@catnekaise/cdk-iam-utilities.ConditionOperator")
class ConditionOperator(enum.Enum):
    '''
    :stability: experimental
    '''

    STRING_EQUALS = "STRING_EQUALS"
    '''
    :stability: experimental
    '''
    STRING_NOT_EQUALS = "STRING_NOT_EQUALS"
    '''
    :stability: experimental
    '''
    STRING_EQUALS_IGNORECASE = "STRING_EQUALS_IGNORECASE"
    '''
    :stability: experimental
    '''
    STRING_NOT_EQUALS_IGNORECASE = "STRING_NOT_EQUALS_IGNORECASE"
    '''
    :stability: experimental
    '''
    STRING_LIKE = "STRING_LIKE"
    '''
    :stability: experimental
    '''
    STRING_NOT_LIKE = "STRING_NOT_LIKE"
    '''
    :stability: experimental
    '''
    STRING_EQUALS_IFEXISTS = "STRING_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    STRING_NOT_EQUALS_IFEXISTS = "STRING_NOT_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    STRING_EQUALS_IGNORECASE_IFEXISTS = "STRING_EQUALS_IGNORECASE_IFEXISTS"
    '''
    :stability: experimental
    '''
    STRING_NOT_EQUALS_IGNORECASE_IFEXISTS = "STRING_NOT_EQUALS_IGNORECASE_IFEXISTS"
    '''
    :stability: experimental
    '''
    STRING_LIKE_IFEXISTS = "STRING_LIKE_IFEXISTS"
    '''
    :stability: experimental
    '''
    STRING_NOT_LIKE_IFEXISTS = "STRING_NOT_LIKE_IFEXISTS"
    '''
    :stability: experimental
    '''
    DATE_EQUALS = "DATE_EQUALS"
    '''
    :stability: experimental
    '''
    DATE_NOT_EQUALS = "DATE_NOT_EQUALS"
    '''
    :stability: experimental
    '''
    DATE_LESS_THAN = "DATE_LESS_THAN"
    '''
    :stability: experimental
    '''
    DATE_LESS_THAN_EQUALS = "DATE_LESS_THAN_EQUALS"
    '''
    :stability: experimental
    '''
    DATE_GREATER_THAN = "DATE_GREATER_THAN"
    '''
    :stability: experimental
    '''
    DATE_GREATER_THAN_EQUALS = "DATE_GREATER_THAN_EQUALS"
    '''
    :stability: experimental
    '''
    DATE_EQUALS_IFEXISTS = "DATE_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    DATE_NOT_EQUALS_IFEXISTS = "DATE_NOT_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    DATE_LESS_THAN_IFEXISTS = "DATE_LESS_THAN_IFEXISTS"
    '''
    :stability: experimental
    '''
    DATE_LESS_THAN_EQUALS_IFEXISTS = "DATE_LESS_THAN_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    DATE_GREATER_THAN_IFEXISTS = "DATE_GREATER_THAN_IFEXISTS"
    '''
    :stability: experimental
    '''
    DATE_GREATER_THAN_EQUALS_IFEXISTS = "DATE_GREATER_THAN_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    NUMERIC_EQUALS = "NUMERIC_EQUALS"
    '''
    :stability: experimental
    '''
    NUMERIC_NOT_EQUALS = "NUMERIC_NOT_EQUALS"
    '''
    :stability: experimental
    '''
    NUMERIC_LESS_THAN = "NUMERIC_LESS_THAN"
    '''
    :stability: experimental
    '''
    NUMERIC_LESS_THAN_EQUALS = "NUMERIC_LESS_THAN_EQUALS"
    '''
    :stability: experimental
    '''
    NUMERIC_GREATER_THAN = "NUMERIC_GREATER_THAN"
    '''
    :stability: experimental
    '''
    NUMERIC_GREATER_THAN_EQUALS = "NUMERIC_GREATER_THAN_EQUALS"
    '''
    :stability: experimental
    '''
    NUMERIC_EQUALS_IFEXISTS = "NUMERIC_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    NUMERIC_NOT_EQUALS_IFEXISTS = "NUMERIC_NOT_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    NUMERIC_LESS_THAN_IFEXISTS = "NUMERIC_LESS_THAN_IFEXISTS"
    '''
    :stability: experimental
    '''
    NUMERIC_LESS_THAN_EQUALS_IFEXISTS = "NUMERIC_LESS_THAN_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    NUMERIC_GREATER_THAN_IFEXISTS = "NUMERIC_GREATER_THAN_IFEXISTS"
    '''
    :stability: experimental
    '''
    NUMERIC_GREATER_THAN_EQUALS_IFEXISTS = "NUMERIC_GREATER_THAN_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    FOR_ANY_VALUE_STRING_LIKE = "FOR_ANY_VALUE_STRING_LIKE"
    '''
    :stability: experimental
    '''
    FOR_ANY_VALUE_STRING_EQUALS = "FOR_ANY_VALUE_STRING_EQUALS"
    '''
    :stability: experimental
    '''
    FOR_ALL_VALUES_STRING_LIKE = "FOR_ALL_VALUES_STRING_LIKE"
    '''
    :stability: experimental
    '''
    FOR_ALL_VALUES_STRING_EQUALS = "FOR_ALL_VALUES_STRING_EQUALS"
    '''
    :stability: experimental
    '''
    FOR_ALL_VALUES_STRING_EQUALS_IGNORECASE = "FOR_ALL_VALUES_STRING_EQUALS_IGNORECASE"
    '''
    :stability: experimental
    '''
    BOOL = "BOOL"
    '''
    :stability: experimental
    '''
    BOOL_IFEXISTS = "BOOL_IFEXISTS"
    '''
    :stability: experimental
    '''
    BINARY_EQUALS = "BINARY_EQUALS"
    '''
    :stability: experimental
    '''
    ARN_EQUALS = "ARN_EQUALS"
    '''
    :stability: experimental
    '''
    ARN_LIKE = "ARN_LIKE"
    '''
    :stability: experimental
    '''
    ARN_NOT_EQUALS = "ARN_NOT_EQUALS"
    '''
    :stability: experimental
    '''
    ARN_NOT_LIKE = "ARN_NOT_LIKE"
    '''
    :stability: experimental
    '''
    ARN_EQUALS_IFEXISTS = "ARN_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    ARN_LIKE_IFEXISTS = "ARN_LIKE_IFEXISTS"
    '''
    :stability: experimental
    '''
    ARN_NOT_EQUALS_IFEXISTS = "ARN_NOT_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    ARN_NOT_LIKE_IFEXISTS = "ARN_NOT_LIKE_IFEXISTS"
    '''
    :stability: experimental
    '''
    IP_ADDRESS = "IP_ADDRESS"
    '''
    :stability: experimental
    '''
    IP_ADDRESS_IFEXISTS = "IP_ADDRESS_IFEXISTS"
    '''
    :stability: experimental
    '''
    NOT_IP_ADDRESS = "NOT_IP_ADDRESS"
    '''
    :stability: experimental
    '''
    NOT_IP_ADDRESS_IFEXISTS = "NOT_IP_ADDRESS_IFEXISTS"
    '''
    :stability: experimental
    '''
    NULL = "NULL"
    '''
    :stability: experimental
    '''


class Constraint(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/cdk-iam-utilities.Constraint",
):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="assemble")
    @abc.abstractmethod
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: "PolicyType",
        claims_context: typing.Optional["IClaimsContext"] = None,
    ) -> typing.List["ConstraintPolicyMutation"]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="isNotNullCondition")
    def _is_not_null_condition(self, key: ConditionKey) -> "ConstraintPolicyMutation":
        '''
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3554a7416b8f4325bad1fcd245ed1b4a55aacd87adb9ae78b49ae1e9d4b2923c)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("ConstraintPolicyMutation", jsii.invoke(self, "isNotNullCondition", [key]))


class _ConstraintProxy(Constraint):
    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: "PolicyType",
        claims_context: typing.Optional["IClaimsContext"] = None,
    ) -> typing.List["ConstraintPolicyMutation"]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78512b1ae9454b85939b9732af5a8c6e813419973de1d01fc7c98f805c9a9cc2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List["ConstraintPolicyMutation"], jsii.invoke(self, "assemble", [scope, context]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Constraint).__jsii_proxy_class__ = lambda : _ConstraintProxy


@jsii.data_type(
    jsii_type="@catnekaise/cdk-iam-utilities.ConstraintAssembleContext",
    jsii_struct_bases=[],
    name_mapping={
        "effect": "effect",
        "policy_type": "policyType",
        "claims_context": "claimsContext",
    },
)
class ConstraintAssembleContext:
    def __init__(
        self,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: "PolicyType",
        claims_context: typing.Optional["IClaimsContext"] = None,
    ) -> None:
        '''
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2863a74feda187cf9c7428a7acb3c75561d377d334bbce8ebc9980cfb73f988)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            check_type(argname="argument claims_context", value=claims_context, expected_type=type_hints["claims_context"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "effect": effect,
            "policy_type": policy_type,
        }
        if claims_context is not None:
            self._values["claims_context"] = claims_context

    @builtins.property
    def effect(self) -> _aws_cdk_aws_iam_ceddda9d.Effect:
        '''
        :stability: experimental
        '''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Effect, result)

    @builtins.property
    def policy_type(self) -> "PolicyType":
        '''
        :stability: experimental
        '''
        result = self._values.get("policy_type")
        assert result is not None, "Required property 'policy_type' is missing"
        return typing.cast("PolicyType", result)

    @builtins.property
    def claims_context(self) -> typing.Optional["IClaimsContext"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("claims_context")
        return typing.cast(typing.Optional["IClaimsContext"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConstraintAssembleContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@catnekaise/cdk-iam-utilities.ConstraintPolicyMutation",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "operator": "operator",
        "type": "type",
        "value": "value",
        "actions_match_service": "actionsMatchService",
        "order": "order",
        "strategy": "strategy",
    },
)
class ConstraintPolicyMutation:
    def __init__(
        self,
        *,
        key: ConditionKey,
        operator: ConditionOperator,
        type: "ConstraintPolicyMutationType",
        value: typing.Sequence[typing.Any],
        actions_match_service: typing.Optional[builtins.str] = None,
        order: typing.Optional[jsii.Number] = None,
        strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: 
        :param operator: 
        :param type: 
        :param value: 
        :param actions_match_service: 
        :param order: 
        :param strategy: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f4d85ef5f1e6942b1ccbff7fa8879ab6331a388eb63dff395619cf0e4eeb0a)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument actions_match_service", value=actions_match_service, expected_type=type_hints["actions_match_service"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "operator": operator,
            "type": type,
            "value": value,
        }
        if actions_match_service is not None:
            self._values["actions_match_service"] = actions_match_service
        if order is not None:
            self._values["order"] = order
        if strategy is not None:
            self._values["strategy"] = strategy

    @builtins.property
    def key(self) -> ConditionKey:
        '''
        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(ConditionKey, result)

    @builtins.property
    def operator(self) -> ConditionOperator:
        '''
        :stability: experimental
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(ConditionOperator, result)

    @builtins.property
    def type(self) -> "ConstraintPolicyMutationType":
        '''
        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("ConstraintPolicyMutationType", result)

    @builtins.property
    def value(self) -> typing.List[typing.Any]:
        '''
        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(typing.List[typing.Any], result)

    @builtins.property
    def actions_match_service(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("actions_match_service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def strategy(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConstraintPolicyMutation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@catnekaise/cdk-iam-utilities.ConstraintPolicyMutationType")
class ConstraintPolicyMutationType(enum.Enum):
    '''
    :stability: experimental
    '''

    CONDITION = "CONDITION"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@catnekaise/cdk-iam-utilities.ConstraintUtilitySettings",
    jsii_struct_bases=[],
    name_mapping={
        "policy_type": "policyType",
        "append_condition_values": "appendConditionValues",
        "claims_context": "claimsContext",
    },
)
class ConstraintUtilitySettings:
    def __init__(
        self,
        *,
        policy_type: "PolicyType",
        append_condition_values: typing.Optional[builtins.bool] = None,
        claims_context: typing.Optional["IClaimsContext"] = None,
    ) -> None:
        '''
        :param policy_type: 
        :param append_condition_values: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8202a24804394817fbbdfa37ce377a9161710e16f06238342326944636ab46)
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            check_type(argname="argument append_condition_values", value=append_condition_values, expected_type=type_hints["append_condition_values"])
            check_type(argname="argument claims_context", value=claims_context, expected_type=type_hints["claims_context"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_type": policy_type,
        }
        if append_condition_values is not None:
            self._values["append_condition_values"] = append_condition_values
        if claims_context is not None:
            self._values["claims_context"] = claims_context

    @builtins.property
    def policy_type(self) -> "PolicyType":
        '''
        :stability: experimental
        '''
        result = self._values.get("policy_type")
        assert result is not None, "Required property 'policy_type' is missing"
        return typing.cast("PolicyType", result)

    @builtins.property
    def append_condition_values(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("append_condition_values")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def claims_context(self) -> typing.Optional["IClaimsContext"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("claims_context")
        return typing.cast(typing.Optional["IClaimsContext"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConstraintUtilitySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@catnekaise/cdk-iam-utilities.ConstraintsBuilderSettings",
    jsii_struct_bases=[],
    name_mapping={"claims_context": "claimsContext"},
)
class ConstraintsBuilderSettings:
    def __init__(
        self,
        *,
        claims_context: typing.Optional["IClaimsContext"] = None,
    ) -> None:
        '''
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0bb2cf82c461dbaed99d2b9387bf74b270114927f3b4500911fe2032887e59)
            check_type(argname="argument claims_context", value=claims_context, expected_type=type_hints["claims_context"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if claims_context is not None:
            self._values["claims_context"] = claims_context

    @builtins.property
    def claims_context(self) -> typing.Optional["IClaimsContext"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("claims_context")
        return typing.cast(typing.Optional["IClaimsContext"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConstraintsBuilderSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConstraintsUtility(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.ConstraintsUtility",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="forConstraints")
    @builtins.classmethod
    def for_constraints(
        cls,
        constraints: typing.Sequence[Constraint],
    ) -> "ConstraintsUtility":
        '''
        :param constraints: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bff860b975c707fa9fd54d708b6ac2b5cf35ea2c2608acca3bd4b21c26490bd)
            check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
        return typing.cast("ConstraintsUtility", jsii.sinvoke(cls, "forConstraints", [constraints]))

    @jsii.member(jsii_name="appendGrant")
    def append_grant(
        self,
        scope: _constructs_77d1e7e8.Construct,
        settings: typing.Union[ConstraintUtilitySettings, typing.Dict[builtins.str, typing.Any]],
        grant: _aws_cdk_aws_iam_ceddda9d.Grant,
    ) -> None:
        '''
        :param scope: -
        :param settings: -
        :param grant: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325002ec7621292d99171ac86ec16036443d8414671cab78972916d40a137264)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument grant", value=grant, expected_type=type_hints["grant"])
        return typing.cast(None, jsii.invoke(self, "appendGrant", [scope, settings, grant]))

    @jsii.member(jsii_name="appendPolicy")
    def append_policy(
        self,
        scope: _constructs_77d1e7e8.Construct,
        settings: typing.Union[ConstraintUtilitySettings, typing.Dict[builtins.str, typing.Any]],
        policy_statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    ) -> None:
        '''
        :param scope: -
        :param settings: -
        :param policy_statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db2dfdf69b0d2e1a41d8274bec1b68b48b68db05fbb4acb7997fbc8949589707)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument policy_statement", value=policy_statement, expected_type=type_hints["policy_statement"])
        return typing.cast(None, jsii.invoke(self, "appendPolicy", [scope, settings, policy_statement]))


class DateConstraint(
    Constraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.DateConstraint",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="betweenDates")
    @builtins.classmethod
    def between_dates(
        cls,
        key: ConditionKey,
        from_: datetime.datetime,
        to: datetime.datetime,
    ) -> "DateConstraint":
        '''
        :param key: -
        :param from_: -
        :param to: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4992c18f8a0db5811b6d76506dbd028413eda56be7be629ab03aec38e2e4d85)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
        return typing.cast("DateConstraint", jsii.sinvoke(cls, "betweenDates", [key, from_, to]))

    @jsii.member(jsii_name="greaterThan")
    @builtins.classmethod
    def greater_than(
        cls,
        key: ConditionKey,
        date: datetime.datetime,
    ) -> "DateConstraint":
        '''
        :param key: -
        :param date: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc8cfaa4a7e50633fa490fcfad37b0aa1e1b812f45133a9ef71b2a9c37a3b71)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument date", value=date, expected_type=type_hints["date"])
        return typing.cast("DateConstraint", jsii.sinvoke(cls, "greaterThan", [key, date]))

    @jsii.member(jsii_name="lessThan")
    @builtins.classmethod
    def less_than(cls, key: ConditionKey, date: datetime.datetime) -> "DateConstraint":
        '''
        :param key: -
        :param date: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18eba81bcc8d9cecb2480c521f139d67172ef1e24866864bff6ce9f0c3de3ddc)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument date", value=date, expected_type=type_hints["date"])
        return typing.cast("DateConstraint", jsii.sinvoke(cls, "lessThan", [key, date]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: "PolicyType",
        claims_context: typing.Optional["IClaimsContext"] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b23c6608a91ebbb65c20252e74279635ccf77e22ee2acd1b266d9898d825f35)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))


class GenericConditionKey(
    ConditionKey,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.GenericConditionKey",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(
        cls,
        name: builtins.str,
        *,
        supported_operators: typing.Sequence[builtins.str],
    ) -> "GenericConditionKey":
        '''
        :param name: -
        :param supported_operators: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3919b9b736f87daa6d0e2684a80fc75b05b31f28edf68f9016ca7d3a36984640)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        settings = ConditionKeySettings(supported_operators=supported_operators)

        return typing.cast("GenericConditionKey", jsii.sinvoke(cls, "custom", [name, settings]))


class GenericConstraint(
    Constraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.GenericConstraint",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        operator: ConditionOperator,
        key: ConditionKey,
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> None:
        '''
        :param operator: -
        :param key: -
        :param value: -
        :param additional_values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc6d56ac9755bf1c9d32d04f4b771dbe5c3e436767a17a8bea59c23010f0143)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        jsii.create(self.__class__, self, [operator, key, value, *additional_values])

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: "PolicyType",
        claims_context: typing.Optional["IClaimsContext"] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e18ea26ae53c1a58603c85c38641087e286d6db9153b9fd74d42ab6f55769f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> ConditionKey:
        '''
        :stability: experimental
        '''
        return typing.cast(ConditionKey, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> ConditionOperator:
        '''
        :stability: experimental
        '''
        return typing.cast(ConditionOperator, jsii.get(self, "operator"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "value"))


class GlobalConditionKey(
    ConditionKey,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.GlobalConditionKey",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="principalTag")
    @builtins.classmethod
    def principal_tag(cls, tag_name: builtins.str) -> "AwsPrincipalTagConditionKey":
        '''(experimental) Use this key to compare the tag attached to the principal making the request with the tag that you specify in the policy.

        :param tag_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aefa7245f6d829948254ee45c80e68195f85098c711c878cacb3dfdb67d4479)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        return typing.cast("AwsPrincipalTagConditionKey", jsii.sinvoke(cls, "principalTag", [tag_name]))

    @jsii.member(jsii_name="requestTag")
    @builtins.classmethod
    def request_tag(cls, tag_name: builtins.str) -> "AwsRequestTagConditionKey":
        '''(experimental) Use this key to compare the tag key-value pair that was passed in the request with the tag pair that you specify in the policy.

        :param tag_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3817ac0061bbb05b1fa3605c686b667f95aa4b4bb0043641016b74eeccd9fb6a)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        return typing.cast("AwsRequestTagConditionKey", jsii.sinvoke(cls, "requestTag", [tag_name]))

    @jsii.member(jsii_name="resourceTag")
    @builtins.classmethod
    def resource_tag(cls, tag_name: builtins.str) -> "AwsResourceTagConditionKey":
        '''(experimental) Use this key to compare the tag key-value pair that you specify in the policy with the key-value pair attached to the resource.

        :param tag_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a171c8016e1c970bc8ff80e029f7183e923e1b4417fcec179055886649c2303d)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        return typing.cast("AwsResourceTagConditionKey", jsii.sinvoke(cls, "resourceTag", [tag_name]))

    @jsii.member(jsii_name="toConstraint")
    def to_constraint(
        self,
        operator: ConditionOperator,
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> GenericConstraint:
        '''
        :param operator: -
        :param value: -
        :param additional_values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a6db3a31b14dc73a7ad1fbb2bd3ed0aef04ede0ab59b100cf638cddc64987a2)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(GenericConstraint, jsii.invoke(self, "toConstraint", [operator, value, *additional_values]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CalledVia")
    def CALLED_VIA(cls) -> "GlobalConditionKey":
        '''(experimental) Use this key to compare the services in the policy with the services that made requests on behalf of the IAM principal (user or role).

        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "CalledVia"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CalledViaFirst")
    def CALLED_VIA_FIRST(cls) -> "GlobalConditionKey":
        '''(experimental) Use this key to compare the services in the policy with the first service that made a request on behalf of the IAM principal (user or role).

        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "CalledViaFirst"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CalledViaLast")
    def CALLED_VIA_LAST(cls) -> "GlobalConditionKey":
        '''(experimental) Use this key to compare the services in the policy with the last service that made a request on behalf of the IAM principal (user or role).

        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "CalledViaLast"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CurrentTime")
    def CURRENT_TIME(cls) -> "GlobalConditionKey":
        '''(experimental) Use this key to compare the date and time of the request with the date and time that you specify in the policy.

        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "CurrentTime"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Ec2InstanceSourcePrivateIPv4")
    def EC2_INSTANCE_SOURCE_PRIVATE_I_PV4(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "Ec2InstanceSourcePrivateIPv4"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Ec2InstanceSourceVpc")
    def EC2_INSTANCE_SOURCE_VPC(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "Ec2InstanceSourceVpc"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="EpochTime")
    def EPOCH_TIME(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "EpochTime"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FederatedProvider")
    def FEDERATED_PROVIDER(cls) -> "AwsFederatedProviderConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("AwsFederatedProviderConditionKey", jsii.sget(cls, "FederatedProvider"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MultiFactorAuthAge")
    def MULTI_FACTOR_AUTH_AGE(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "MultiFactorAuthAge"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MultiFactorAuthPresent")
    def MULTI_FACTOR_AUTH_PRESENT(cls) -> "GlobalBoolConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalBoolConditionKey", jsii.sget(cls, "MultiFactorAuthPresent"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PrincipalAccount")
    def PRINCIPAL_ACCOUNT(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "PrincipalAccount"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PrincipalArn")
    def PRINCIPAL_ARN(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "PrincipalArn"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PrincipalIsAWSService")
    def PRINCIPAL_IS_AWS_SERVICE(cls) -> "GlobalBoolConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalBoolConditionKey", jsii.sget(cls, "PrincipalIsAWSService"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PrincipalOrgID")
    def PRINCIPAL_ORG_ID(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "PrincipalOrgID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PrincipalOrgPaths")
    def PRINCIPAL_ORG_PATHS(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "PrincipalOrgPaths"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PrincipalServiceName")
    def PRINCIPAL_SERVICE_NAME(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "PrincipalServiceName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PrincipalServiceNamesList")
    def PRINCIPAL_SERVICE_NAMES_LIST(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "PrincipalServiceNamesList"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PrincipalType")
    def PRINCIPAL_TYPE(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "PrincipalType"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Referer")
    def REFERER(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "Referer"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RequestedRegion")
    def REQUESTED_REGION(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "RequestedRegion"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ResourceAccount")
    def RESOURCE_ACCOUNT(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "ResourceAccount"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ResourceOrgID")
    def RESOURCE_ORG_ID(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "ResourceOrgID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ResourceOrgPaths")
    def RESOURCE_ORG_PATHS(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "ResourceOrgPaths"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SecureTransport")
    def SECURE_TRANSPORT(cls) -> "GlobalBoolConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalBoolConditionKey", jsii.sget(cls, "SecureTransport"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SourceAccount")
    def SOURCE_ACCOUNT(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "SourceAccount"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SourceArn")
    def SOURCE_ARN(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "SourceArn"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SourceIdentity")
    def SOURCE_IDENTITY(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "SourceIdentity"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SourceIp")
    def SOURCE_IP(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "SourceIp"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SourceOrgID")
    def SOURCE_ORG_ID(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "SourceOrgID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SourceOrgPaths")
    def SOURCE_ORG_PATHS(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "SourceOrgPaths"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SourceVpc")
    def SOURCE_VPC(cls) -> "AwsSourceVpcConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("AwsSourceVpcConditionKey", jsii.sget(cls, "SourceVpc"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SourceVpce")
    def SOURCE_VPCE(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "SourceVpce"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TagKeys")
    def TAG_KEYS(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "TagKeys"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TokenIssueTime")
    def TOKEN_ISSUE_TIME(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "TokenIssueTime"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UserAgent")
    def USER_AGENT(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "UserAgent"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Userid")
    def USERID(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "Userid"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Username")
    def USERNAME(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "Username"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ViaAWSService")
    def VIA_AWS_SERVICE(cls) -> "GlobalBoolConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalBoolConditionKey", jsii.sget(cls, "ViaAWSService"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VpcSourceIp")
    def VPC_SOURCE_IP(cls) -> "GlobalConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalConditionKey", jsii.sget(cls, "VpcSourceIp"))


@jsii.interface(jsii_type="@catnekaise/cdk-iam-utilities.IClaimsContext")
class IClaimsContext(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="knownClaims")
    def known_claims(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="mappedClaims")
    def mapped_claims(self) -> "IMappedClaims":
        '''
        :stability: experimental
        '''
        ...


class _IClaimsContextProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@catnekaise/cdk-iam-utilities.IClaimsContext"

    @builtins.property
    @jsii.member(jsii_name="knownClaims")
    def known_claims(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "knownClaims"))

    @builtins.property
    @jsii.member(jsii_name="mappedClaims")
    def mapped_claims(self) -> "IMappedClaims":
        '''
        :stability: experimental
        '''
        return typing.cast("IMappedClaims", jsii.get(self, "mappedClaims"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IClaimsContext).__jsii_proxy_class__ = lambda : _IClaimsContextProxy


@jsii.interface(jsii_type="@catnekaise/cdk-iam-utilities.IConstraintsBuilder")
class IConstraintsBuilder(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="constraints")
    def constraints(self) -> typing.List[Constraint]:
        '''
        :stability: experimental
        '''
        ...


class _IConstraintsBuilderProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@catnekaise/cdk-iam-utilities.IConstraintsBuilder"

    @builtins.property
    @jsii.member(jsii_name="constraints")
    def constraints(self) -> typing.List[Constraint]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[Constraint], jsii.get(self, "constraints"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IConstraintsBuilder).__jsii_proxy_class__ = lambda : _IConstraintsBuilderProxy


@jsii.interface(jsii_type="@catnekaise/cdk-iam-utilities.IIamResourcePath")
class IIamResourcePath(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...


class _IIamResourcePathProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@catnekaise/cdk-iam-utilities.IIamResourcePath"

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIamResourcePath).__jsii_proxy_class__ = lambda : _IIamResourcePathProxy


@jsii.interface(jsii_type="@catnekaise/cdk-iam-utilities.IMappedClaims")
class IMappedClaims(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="claims")
    def claims(self) -> typing.List[Claim]:
        '''
        :stability: experimental
        '''
        ...


class _IMappedClaimsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@catnekaise/cdk-iam-utilities.IMappedClaims"

    @builtins.property
    @jsii.member(jsii_name="claims")
    def claims(self) -> typing.List[Claim]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[Claim], jsii.get(self, "claims"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMappedClaims).__jsii_proxy_class__ = lambda : _IMappedClaimsProxy


@jsii.implements(IIamResourcePath)
class IamResourcePathBuilder(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/cdk-iam-utilities.IamResourcePathBuilder",
):
    '''
    :stability: experimental
    '''

    def __init__(self, path: typing.Sequence[builtins.str]) -> None:
        '''
        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba1e72ca0a3003f8df7f5496395661bfafc24cedfd038bf2e22c1067f90896ad)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        jsii.create(self.__class__, self, [path])

    @jsii.member(jsii_name="appendPolicyVariable")
    def _append_policy_variable(
        self,
        policy_variable: "PolicyVariable",
    ) -> typing.List[builtins.str]:
        '''
        :param policy_variable: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d579f24ae2420110c9c7fff9581283e01cac2a05785b7ee0490e58d4cc8d60)
            check_type(argname="argument policy_variable", value=policy_variable, expected_type=type_hints["policy_variable"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "appendPolicyVariable", [policy_variable]))

    @jsii.member(jsii_name="appendText")
    def _append_text(self, *values: builtins.str) -> typing.List[builtins.str]:
        '''
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7eb01baa4d9c06bf4268d443321102495cd9df3cf50b92db5350afd328998ce)
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "appendText", [*values]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="path")
    def _path(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "path"))


class _IamResourcePathBuilderProxy(IamResourcePathBuilder):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, IamResourcePathBuilder).__jsii_proxy_class__ = lambda : _IamResourcePathBuilderProxy


class IamResourceTagConditionKey(
    ConditionKey,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.IamResourceTagConditionKey",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="tag")
    @builtins.classmethod
    def tag(cls, tag_name: builtins.str) -> "IamResourceTagConditionKey":
        '''
        :param tag_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030a7bfd41157f13c93d46727685067ac955c3140c95dcdf8b11b6b027044b1d)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        return typing.cast("IamResourceTagConditionKey", jsii.sinvoke(cls, "tag", [tag_name]))


@jsii.enum(jsii_type="@catnekaise/cdk-iam-utilities.IpAddressConditionOperator")
class IpAddressConditionOperator(enum.Enum):
    '''
    :stability: experimental
    '''

    IP_ADDRESS = "IP_ADDRESS"
    '''
    :stability: experimental
    '''
    IP_ADDRESS_IFEXISTS = "IP_ADDRESS_IFEXISTS"
    '''
    :stability: experimental
    '''
    NOT_IP_ADDRESS = "NOT_IP_ADDRESS"
    '''
    :stability: experimental
    '''
    NOT_IP_ADDRESS_IFEXISTS = "NOT_IP_ADDRESS_IFEXISTS"
    '''
    :stability: experimental
    '''


@jsii.implements(IMappedClaims)
class MappedClaims(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.MappedClaims",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        claim: builtins.str,
        *additional_claims: builtins.str,
    ) -> "MappedClaims":
        '''
        :param claim: -
        :param additional_claims: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e711bf055273418ac3ba61f42de5b832c88a434f94d54c2d2b914647eeb61554)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument additional_claims", value=additional_claims, expected_type=typing.Tuple[type_hints["additional_claims"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("MappedClaims", jsii.sinvoke(cls, "create", [claim, *additional_claims]))

    @jsii.member(jsii_name="createMapped")
    @builtins.classmethod
    def create_mapped(
        cls,
        claims: typing.Mapping[builtins.str, builtins.str],
    ) -> "MappedClaims":
        '''
        :param claims: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bcc6095d8f2766a839d79d92afef176839c9e97fe75c204245ee2428729ace2)
            check_type(argname="argument claims", value=claims, expected_type=type_hints["claims"])
        return typing.cast("MappedClaims", jsii.sinvoke(cls, "createMapped", [claims]))

    @builtins.property
    @jsii.member(jsii_name="claims")
    def claims(self) -> typing.List[Claim]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[Claim], jsii.get(self, "claims"))


class NullConstraint(
    Constraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.NullConstraint",
):
    '''
    :stability: experimental
    '''

    def __init__(self, key: ConditionKey, is_null: builtins.bool) -> None:
        '''
        :param key: -
        :param is_null: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf5999407d1006bcfcd695c3e91204050d66d5fca2a57aa8b0b2f364a1b510ac)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument is_null", value=is_null, expected_type=type_hints["is_null"])
        jsii.create(self.__class__, self, [key, is_null])

    @jsii.member(jsii_name="isNotNull")
    @builtins.classmethod
    def is_not_null(cls, key: ConditionKey) -> "NullConstraint":
        '''
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4293d5f1c3aa4f036928c8834639298950ef25d6a46253f7e64ccfd3d1b1c8)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("NullConstraint", jsii.sinvoke(cls, "isNotNull", [key]))

    @jsii.member(jsii_name="isNull")
    @builtins.classmethod
    def is_null(cls, key: ConditionKey) -> "NullConstraint":
        '''
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b39095ecd276d15bab406a4d6b27214f44e0662fe5d5aaa692f2a1e307f4d3)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("NullConstraint", jsii.sinvoke(cls, "isNull", [key]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: "PolicyType",
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e64cd196439f79b45dc041c976004a54872cad55227156ba3488b656f6584e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))


class OperatorUtils(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/cdk-iam-utilities.OperatorUtils",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="arraySupport")
    @builtins.classmethod
    def array_support(cls, value: ConditionOperator) -> builtins.bool:
        '''
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d3f7b564d18a0f22f7b97e970c9e6dfa1d47339825a88598c2844533e9a410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "arraySupport", [value]))

    @jsii.member(jsii_name="convert")
    @builtins.classmethod
    def convert(cls, value: typing.Any) -> ConditionOperator:
        '''
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1dce653b1ac742d1f45816e7704a5f56a7cef1b8dba7fdafb34937386223c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(ConditionOperator, jsii.sinvoke(cls, "convert", [value]))

    @jsii.member(jsii_name="operatorIsSupported")
    @builtins.classmethod
    def operator_is_supported(
        cls,
        supported_operators: typing.Sequence[builtins.str],
        operator: ConditionOperator,
    ) -> typing.Optional[builtins.bool]:
        '''
        :param supported_operators: -
        :param operator: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31efcd8d4fbd78fef9330070e8016aaf02f4b0882626bfc2b088512203f336cd)
            check_type(argname="argument supported_operators", value=supported_operators, expected_type=type_hints["supported_operators"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        return typing.cast(typing.Optional[builtins.bool], jsii.sinvoke(cls, "operatorIsSupported", [supported_operators, operator]))

    @jsii.member(jsii_name="operatorShortName")
    @builtins.classmethod
    def operator_short_name(cls, operator: ConditionOperator) -> builtins.str:
        '''
        :param operator: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be7b72649f14a5c461b6d971c62f67f4d66f0a8e9fd1583f81d480d9fc61a96)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "operatorShortName", [operator]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Arn")
    def ARN(cls) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "Arn"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Binary")
    def BINARY(cls) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "Binary"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Bool")
    def BOOL(cls) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "Bool"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Date")
    def DATE(cls) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "Date"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="IpAddress")
    def IP_ADDRESS(cls) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "IpAddress"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Many")
    def MANY(cls) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "Many"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Numeric")
    def NUMERIC(cls) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "Numeric"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="String")
    def STRING(cls) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "String"))


class _OperatorUtilsProxy(OperatorUtils):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, OperatorUtils).__jsii_proxy_class__ = lambda : _OperatorUtilsProxy


class PassClaimsConstraint(
    Constraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.PassClaimsConstraint",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        *,
        allow_any_tags: builtins.bool,
        claims: typing.Mapping[builtins.str, builtins.str],
        specifically_allowed_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> "PassClaimsConstraint":
        '''
        :param allow_any_tags: 
        :param claims: 
        :param specifically_allowed_tags: 

        :stability: experimental
        '''
        claims_ = PassClaimsConstraintSettings(
            allow_any_tags=allow_any_tags,
            claims=claims,
            specifically_allowed_tags=specifically_allowed_tags,
        )

        return typing.cast("PassClaimsConstraint", jsii.sinvoke(cls, "create", [claims_]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: "PolicyType",
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f387b0bc01f59b65dfc380d9b67da751e6b78ddb04ae9a970ee2f97db95653c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "PassClaimsConstraintSettings":
        '''
        :stability: experimental
        '''
        return typing.cast("PassClaimsConstraintSettings", jsii.get(self, "settings"))


@jsii.data_type(
    jsii_type="@catnekaise/cdk-iam-utilities.PassClaimsConstraintSettings",
    jsii_struct_bases=[],
    name_mapping={
        "allow_any_tags": "allowAnyTags",
        "claims": "claims",
        "specifically_allowed_tags": "specificallyAllowedTags",
    },
)
class PassClaimsConstraintSettings:
    def __init__(
        self,
        *,
        allow_any_tags: builtins.bool,
        claims: typing.Mapping[builtins.str, builtins.str],
        specifically_allowed_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allow_any_tags: 
        :param claims: 
        :param specifically_allowed_tags: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed089b1d5517d7b95e7e69859d1f621cb27884a1dfbf2b81b7afec5d7aff152)
            check_type(argname="argument allow_any_tags", value=allow_any_tags, expected_type=type_hints["allow_any_tags"])
            check_type(argname="argument claims", value=claims, expected_type=type_hints["claims"])
            check_type(argname="argument specifically_allowed_tags", value=specifically_allowed_tags, expected_type=type_hints["specifically_allowed_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allow_any_tags": allow_any_tags,
            "claims": claims,
        }
        if specifically_allowed_tags is not None:
            self._values["specifically_allowed_tags"] = specifically_allowed_tags

    @builtins.property
    def allow_any_tags(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        result = self._values.get("allow_any_tags")
        assert result is not None, "Required property 'allow_any_tags' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def claims(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("claims")
        assert result is not None, "Required property 'claims' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def specifically_allowed_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("specifically_allowed_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PassClaimsConstraintSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyType(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.PolicyType",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="resourcePolicy")
    @builtins.classmethod
    def resource_policy(cls, type: "ResourcePolicyType") -> "PolicyType":
        '''
        :param type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1488aab025da2f6ebe837b89cd7d4d152b1a9ede9a20d7f699aded9437cc3b)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        return typing.cast("PolicyType", jsii.sinvoke(cls, "resourcePolicy", [type]))

    @jsii.member(jsii_name="trustPolicy")
    @builtins.classmethod
    def trust_policy(cls, principal_type: "PrincipalType") -> "PolicyType":
        '''
        :param principal_type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c35d7afcfe150bef534798fbf915f3bbf72ed6fcc34142e86ad7556b4034ef)
            check_type(argname="argument principal_type", value=principal_type, expected_type=type_hints["principal_type"])
        return typing.cast("PolicyType", jsii.sinvoke(cls, "trustPolicy", [principal_type]))

    @jsii.member(jsii_name="isResourcePolicyForService")
    def is_resource_policy_for_service(
        self,
        service: "ResourcePolicyType",
    ) -> builtins.bool:
        '''
        :param service: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__929540b146757b024841c74dcecbcb001b2b0c94c3910ed102951d755674516b)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isResourcePolicyForService", [service]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="IdentityPolicy")
    def IDENTITY_POLICY(cls) -> "PolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("PolicyType", jsii.sget(cls, "IdentityPolicy"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NonSpecific")
    def NON_SPECIFIC(cls) -> "PolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("PolicyType", jsii.sget(cls, "NonSpecific"))

    @builtins.property
    @jsii.member(jsii_name="isIdentityPolicy")
    def is_identity_policy(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isIdentityPolicy"))

    @builtins.property
    @jsii.member(jsii_name="isResourcePolicy")
    def is_resource_policy(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isResourcePolicy"))

    @builtins.property
    @jsii.member(jsii_name="isTrustPolicy")
    def is_trust_policy(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isTrustPolicy"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="principalType")
    def principal_type(self) -> typing.Optional["PrincipalType"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["PrincipalType"], jsii.get(self, "principalType"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> typing.Optional["ResourcePolicyType"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["ResourcePolicyType"], jsii.get(self, "service"))


class PolicyVariable(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.PolicyVariable",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="principalOrgId")
    @builtins.classmethod
    def principal_org_id(
        cls,
        default_value: typing.Optional[builtins.str] = None,
    ) -> "PolicyVariable":
        '''
        :param default_value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bccd0b528f3b8e599b67953eafb64f9fab704c22221ad16dd6f3b51546e902ff)
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
        return typing.cast("PolicyVariable", jsii.sinvoke(cls, "principalOrgId", [default_value]))

    @jsii.member(jsii_name="principalTag")
    @builtins.classmethod
    def principal_tag(
        cls,
        tag_name: builtins.str,
        default_value: typing.Optional[builtins.str] = None,
    ) -> "PolicyVariable":
        '''
        :param tag_name: -
        :param default_value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a3facd6bb8b1c1f9bb9306169f86328fb37f31579149f4c5e3b3f692706789)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
        return typing.cast("PolicyVariable", jsii.sinvoke(cls, "principalTag", [tag_name, default_value]))

    @jsii.member(jsii_name="principalType")
    @builtins.classmethod
    def principal_type(
        cls,
        default_value: typing.Optional[builtins.str] = None,
    ) -> "PolicyVariable":
        '''
        :param default_value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a03101e09da0f49d5a1d6e3f636ca9ed765f56d0484fd8f8c22a903404d561)
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
        return typing.cast("PolicyVariable", jsii.sinvoke(cls, "principalType", [default_value]))

    @jsii.member(jsii_name="requestTag")
    @builtins.classmethod
    def request_tag(
        cls,
        tag_name: builtins.str,
        default_value: typing.Optional[builtins.str] = None,
    ) -> "PolicyVariable":
        '''
        :param tag_name: -
        :param default_value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3638d25c3dc30d928c8d1bbe488b7152d1fab341bef38474160d9925506127)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
        return typing.cast("PolicyVariable", jsii.sinvoke(cls, "requestTag", [tag_name, default_value]))

    @jsii.member(jsii_name="resourceTag")
    @builtins.classmethod
    def resource_tag(
        cls,
        tag_name: builtins.str,
        default_value: typing.Optional[builtins.str] = None,
    ) -> "PolicyVariable":
        '''
        :param tag_name: -
        :param default_value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883cda25eaf830ee9d8700fc6a11edeba6785a3280bc35df7fa5f34711f5505b)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
        return typing.cast("PolicyVariable", jsii.sinvoke(cls, "resourceTag", [tag_name, default_value]))

    @jsii.member(jsii_name="userId")
    @builtins.classmethod
    def user_id(
        cls,
        default_value: typing.Optional[builtins.str] = None,
    ) -> "PolicyVariable":
        '''
        :param default_value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08288fcc4d04360808bfb0a61c743a193ee5405701fd7a5aa3a65433f6d5a333)
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
        return typing.cast("PolicyVariable", jsii.sinvoke(cls, "userId", [default_value]))

    @jsii.member(jsii_name="username")
    @builtins.classmethod
    def username(
        cls,
        default_value: typing.Optional[builtins.str] = None,
    ) -> "PolicyVariable":
        '''
        :param default_value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a1da200217adabcdc65a4c18e6d944df345f831bc517251ea247c586d34368)
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
        return typing.cast("PolicyVariable", jsii.sinvoke(cls, "username", [default_value]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="isTag")
    def is_tag(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isTag"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="defaultValue")
    def default_value(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultValue"))

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagName"))


class PrincipalType(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.PrincipalType",
):
    '''
    :stability: experimental
    '''

    @jsii.python.classproperty
    @jsii.member(jsii_name="Aws")
    def AWS(cls) -> "PrincipalType":
        '''
        :stability: experimental
        '''
        return typing.cast("PrincipalType", jsii.sget(cls, "Aws"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Federated")
    def FEDERATED(cls) -> "PrincipalType":
        '''
        :stability: experimental
        '''
        return typing.cast("PrincipalType", jsii.sget(cls, "Federated"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Saml")
    def SAML(cls) -> "PrincipalType":
        '''
        :stability: experimental
        '''
        return typing.cast("PrincipalType", jsii.sget(cls, "Saml"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Service")
    def SERVICE(cls) -> "PrincipalType":
        '''
        :stability: experimental
        '''
        return typing.cast("PrincipalType", jsii.sget(cls, "Service"))

    @builtins.property
    @jsii.member(jsii_name="isAws")
    def is_aws(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isAws"))

    @builtins.property
    @jsii.member(jsii_name="isFederated")
    def is_federated(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isFederated"))

    @builtins.property
    @jsii.member(jsii_name="isSaml")
    def is_saml(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isSaml"))

    @builtins.property
    @jsii.member(jsii_name="isService")
    def is_service(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isService"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))


class ResourcePolicyType(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.ResourcePolicyType",
):
    '''
    :stability: experimental
    '''

    @jsii.python.classproperty
    @jsii.member(jsii_name="API_GATEWAY")
    def API_GATEWAY(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "API_GATEWAY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BACKUP")
    def BACKUP(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "BACKUP"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CODE_BUILD")
    def CODE_BUILD(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "CODE_BUILD"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ECR")
    def ECR(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "ECR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="EVENTBRIDGE")
    def EVENTBRIDGE(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "EVENTBRIDGE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GLUE")
    def GLUE(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "GLUE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="KMS")
    def KMS(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "KMS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LAMBDA")
    def LAMBDA_(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "LAMBDA"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="S3")
    def S3(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "S3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SECRETS_MANAGER")
    def SECRETS_MANAGER(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "SECRETS_MANAGER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SNS")
    def SNS(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "SNS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SQS")
    def SQS(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "SQS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STS")
    def STS(cls) -> "ResourcePolicyType":
        '''
        :stability: experimental
        '''
        return typing.cast("ResourcePolicyType", jsii.sget(cls, "STS"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.enum(jsii_type="@catnekaise/cdk-iam-utilities.StringConditionOperator")
class StringConditionOperator(enum.Enum):
    '''
    :stability: experimental
    '''

    STRING_EQUALS = "STRING_EQUALS"
    '''
    :stability: experimental
    '''
    STRING_NOT_EQUALS = "STRING_NOT_EQUALS"
    '''
    :stability: experimental
    '''
    STRING_EQUALS_IGNORECASE = "STRING_EQUALS_IGNORECASE"
    '''
    :stability: experimental
    '''
    STRING_NOT_EQUALS_IGNORECASE = "STRING_NOT_EQUALS_IGNORECASE"
    '''
    :stability: experimental
    '''
    STRING_LIKE = "STRING_LIKE"
    '''
    :stability: experimental
    '''
    STRING_NOT_LIKE = "STRING_NOT_LIKE"
    '''
    :stability: experimental
    '''
    STRING_EQUALS_IFEXISTS = "STRING_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    STRING_NOT_EQUALS_IFEXISTS = "STRING_NOT_EQUALS_IFEXISTS"
    '''
    :stability: experimental
    '''
    STRING_EQUALS_IGNORECASE_IFEXISTS = "STRING_EQUALS_IGNORECASE_IFEXISTS"
    '''
    :stability: experimental
    '''
    STRING_NOT_EQUALS_IGNORECASE_IFEXISTS = "STRING_NOT_EQUALS_IGNORECASE_IFEXISTS"
    '''
    :stability: experimental
    '''
    STRING_LIKE_IFEXISTS = "STRING_LIKE_IFEXISTS"
    '''
    :stability: experimental
    '''
    STRING_NOT_LIKE_IFEXISTS = "STRING_NOT_LIKE_IFEXISTS"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="@catnekaise/cdk-iam-utilities.StringMultiValueConditionOperator")
class StringMultiValueConditionOperator(enum.Enum):
    '''
    :stability: experimental
    '''

    FOR_ANY_VALUE_STRING_LIKE = "FOR_ANY_VALUE_STRING_LIKE"
    '''
    :stability: experimental
    '''
    FOR_ALL_VALUES_STRING_LIKE = "FOR_ALL_VALUES_STRING_LIKE"
    '''
    :stability: experimental
    '''
    FOR_ALL_VALUES_STRING_EQUALS = "FOR_ALL_VALUES_STRING_EQUALS"
    '''
    :stability: experimental
    '''
    FOR_ALL_VALUES_STRING_EQUALS_IGNORECASE = "FOR_ALL_VALUES_STRING_EQUALS_IGNORECASE"
    '''
    :stability: experimental
    '''
    FOR_ANY_VALUE_STRING_EQUALS = "FOR_ANY_VALUE_STRING_EQUALS"
    '''
    :stability: experimental
    '''


class StsCognitoIdentityConstraint(
    Constraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.StsCognitoIdentityConstraint",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="identityPool")
    @builtins.classmethod
    def identity_pool(
        cls,
        identity_pool_id: builtins.str,
        amr: builtins.str,
    ) -> "StsCognitoIdentityConstraint":
        '''
        :param identity_pool_id: -
        :param amr: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02db5ce86332fc29de0795c8c2d47dbe9d0d2b9205f06263b8d4acfee0b5fe52)
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
            check_type(argname="argument amr", value=amr, expected_type=type_hints["amr"])
        return typing.cast("StsCognitoIdentityConstraint", jsii.sinvoke(cls, "identityPool", [identity_pool_id, amr]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: PolicyType,
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d8056bf07a1aa9c5c0884f21f5f45814a4cfb966c1657b8321e3a793ceecee0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))

    @builtins.property
    @jsii.member(jsii_name="amr")
    def amr(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "amr"))

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "identityPoolId"))


class StsServiceConditionKey(
    ConditionKey,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.StsServiceConditionKey",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="iamResourceTag")
    @builtins.classmethod
    def iam_resource_tag(cls, tag_name: builtins.str) -> IamResourceTagConditionKey:
        '''(experimental) Filters access by the tags that are attached to the role that is being assumed.

        :param tag_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23405446a48da79d84427a4652cf6d05a247906574ad6abe1b5656f49de09201)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        return typing.cast(IamResourceTagConditionKey, jsii.sinvoke(cls, "iamResourceTag", [tag_name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AWSServiceName")
    def AWS_SERVICE_NAME(cls) -> "StsServiceConditionKey":
        '''(experimental) Filters access by the service that is obtaining a bearer token.

        :stability: experimental
        '''
        return typing.cast("StsServiceConditionKey", jsii.sget(cls, "AWSServiceName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CognitoIdentityAmr")
    def COGNITO_IDENTITY_AMR(cls) -> "StsServiceConditionKey":
        '''(experimental) Filters access by the login information for Amazon Cognito.

        :stability: experimental
        '''
        return typing.cast("StsServiceConditionKey", jsii.sget(cls, "CognitoIdentityAmr"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CognitoIdentityAud")
    def COGNITO_IDENTITY_AUD(cls) -> "StsServiceConditionKey":
        '''(experimental) Filters access by the Amazon Cognito identity pool ID.

        :stability: experimental
        '''
        return typing.cast("StsServiceConditionKey", jsii.sget(cls, "CognitoIdentityAud"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CognitoIdentitySub")
    def COGNITO_IDENTITY_SUB(cls) -> "StsServiceConditionKey":
        '''(experimental) Filters access by the subject of the claim (the Amazon Cognito user ID).

        :stability: experimental
        '''
        return typing.cast("StsServiceConditionKey", jsii.sget(cls, "CognitoIdentitySub"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DurationSeconds")
    def DURATION_SECONDS(cls) -> "StsServiceConditionKey":
        '''(experimental) Filters access by the duration in seconds when getting a bearer token.

        :stability: experimental
        '''
        return typing.cast("StsServiceConditionKey", jsii.sget(cls, "DurationSeconds"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ExternalId")
    def EXTERNAL_ID(cls) -> "StsServiceConditionKey":
        '''(experimental) Filters access by the unique identifier required when you assume a role in another account.

        :stability: experimental
        '''
        return typing.cast("StsServiceConditionKey", jsii.sget(cls, "ExternalId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RoleSessionName")
    def ROLE_SESSION_NAME(cls) -> "StsServiceConditionKey":
        '''(experimental) Filters access by the role session name required when you assume a role.

        :stability: experimental
        '''
        return typing.cast("StsServiceConditionKey", jsii.sget(cls, "RoleSessionName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SourceIdentity")
    def SOURCE_IDENTITY(cls) -> "StsServiceConditionKey":
        '''(experimental) Filters access by the source identity that is passed in the request.

        :stability: experimental
        '''
        return typing.cast("StsServiceConditionKey", jsii.sget(cls, "SourceIdentity"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TransitiveTagKeys")
    def TRANSITIVE_TAG_KEYS(cls) -> "StsServiceConditionKey":
        '''(experimental) Filters access by the transitive tag keys that are passed in the request.

        :stability: experimental
        '''
        return typing.cast("StsServiceConditionKey", jsii.sget(cls, "TransitiveTagKeys"))


class StsTransitiveTagKeysConstraint(
    Constraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.StsTransitiveTagKeysConstraint",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="tagsEqualsAndPresent")
    @builtins.classmethod
    def tags_equals_and_present(
        cls,
        value: builtins.str,
        *values: builtins.str,
    ) -> "StsTransitiveTagKeysConstraint":
        '''(experimental) Limit transitive tags to those specified and check for null.

        :param value: -
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02d97fabc6c222666aeaa70205e42ac5eca657ae270c8fccd3f0f18980795c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("StsTransitiveTagKeysConstraint", jsii.sinvoke(cls, "tagsEqualsAndPresent", [value, *values]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: PolicyType,
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c46fa22e756540429e63a748dddbc3ba28221d1abc275d60cf3aefba145b524)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))


class TagConstraint(
    Constraint,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/cdk-iam-utilities.TagConstraint",
):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])


class _TagConstraintProxy(
    TagConstraint,
    jsii.proxy_for(Constraint), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TagConstraint).__jsii_proxy_class__ = lambda : _TagConstraintProxy


class TagKeysConstraint(
    Constraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.TagKeysConstraint",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        operator: StringMultiValueConditionOperator,
        is_not_null: builtins.bool,
        value: builtins.str,
        *values: builtins.str,
    ) -> "TagKeysConstraint":
        '''
        :param operator: -
        :param is_not_null: -
        :param value: -
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef7bb46e092f123fecb0a805198943cb6d59203ac304e40b656a63f121439ef)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument is_not_null", value=is_not_null, expected_type=type_hints["is_not_null"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("TagKeysConstraint", jsii.sinvoke(cls, "create", [operator, is_not_null, value, *values]))

    @jsii.member(jsii_name="requireTagsEquals")
    @builtins.classmethod
    def require_tags_equals(
        cls,
        value: builtins.str,
        *values: builtins.str,
    ) -> "TagKeysConstraint":
        '''(experimental) Limit request tags to those specified and check for null.

        :param value: -
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ae7e09f0cf786d7b0154550eda9cbd7325103a8ada8589cb31865fe3007b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("TagKeysConstraint", jsii.sinvoke(cls, "requireTagsEquals", [value, *values]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: PolicyType,
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8786f6943acbde741df4330fb047d08591c1ea25a76842474c7f89ea3c8c1c8a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        _ = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, _]))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> StringMultiValueConditionOperator:
        '''
        :stability: experimental
        '''
        return typing.cast(StringMultiValueConditionOperator, jsii.get(self, "operator"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))


class AwsFederatedProviderConditionKey(
    ConditionKey,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.AwsFederatedProviderConditionKey",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="toCognitoIdentityConstraint")
    def to_cognito_identity_constraint(self) -> Constraint:
        '''
        :stability: experimental
        '''
        return typing.cast(Constraint, jsii.invoke(self, "toCognitoIdentityConstraint", []))

    @jsii.member(jsii_name="toConstraint")
    def to_constraint(
        self,
        operator: ConditionOperator,
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> GenericConstraint:
        '''
        :param operator: -
        :param value: -
        :param additional_values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e5f880a5a6fe3634905ff9ad29a9d68406f8420aa0965f8e003419e2f1e9da)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(GenericConstraint, jsii.invoke(self, "toConstraint", [operator, value, *additional_values]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Create")
    def CREATE(cls) -> "AwsFederatedProviderConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("AwsFederatedProviderConditionKey", jsii.sget(cls, "Create"))


class AwsPrincipalTagConditionKey(
    ConditionKey,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.AwsPrincipalTagConditionKey",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="tag")
    @builtins.classmethod
    def tag(cls, tag_name: builtins.str) -> "AwsPrincipalTagConditionKey":
        '''
        :param tag_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63105a32ff71051a6c3cc27b2839db2f72f20682827817c48a187a7bf39c8dfd)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        return typing.cast("AwsPrincipalTagConditionKey", jsii.sinvoke(cls, "tag", [tag_name]))


class AwsRequestTagConditionKey(
    ConditionKey,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.AwsRequestTagConditionKey",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="tag")
    @builtins.classmethod
    def tag(cls, tag_name: builtins.str) -> "AwsRequestTagConditionKey":
        '''
        :param tag_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9d1a0a21b769887be63db19eb4f8f4e07e88a05fb96e194758b0f6b6ba8c15)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        return typing.cast("AwsRequestTagConditionKey", jsii.sinvoke(cls, "tag", [tag_name]))


class AwsResourceTagConditionKey(
    ConditionKey,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.AwsResourceTagConditionKey",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="tag")
    @builtins.classmethod
    def tag(cls, tag_name: builtins.str) -> "AwsResourceTagConditionKey":
        '''
        :param tag_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f5027064337667f0800910638b4d6ab2fa5bfae1200e99f94cb75c1a2383d7)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        return typing.cast("AwsResourceTagConditionKey", jsii.sinvoke(cls, "tag", [tag_name]))


class AwsSourceVpcConditionKey(
    ConditionKey,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.AwsSourceVpcConditionKey",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="toVpcConstraint")
    def to_vpc_constraint(
        self,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    ) -> GenericConstraint:
        '''
        :param vpc: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50ea1ebc36b9b83d2846758a38755f21b6f8fe320ee31399b9bd2fc1ecba54f)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        return typing.cast(GenericConstraint, jsii.invoke(self, "toVpcConstraint", [vpc]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Create")
    def CREATE(cls) -> "AwsSourceVpcConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("AwsSourceVpcConditionKey", jsii.sget(cls, "Create"))


class BoolConditionKey(
    ConditionKey,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/cdk-iam-utilities.BoolConditionKey",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        name: builtins.str,
        *,
        supported_operators: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: -
        :param supported_operators: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c112a49f3c459488620bb543f8e87a68ea99572eb957237b69c593faeb09d3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        settings = ConditionKeySettings(supported_operators=supported_operators)

        jsii.create(self.__class__, self, [name, settings])


class _BoolConditionKeyProxy(
    BoolConditionKey,
    jsii.proxy_for(ConditionKey), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, BoolConditionKey).__jsii_proxy_class__ = lambda : _BoolConditionKeyProxy


class BoolConstraint(
    Constraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.BoolConstraint",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="whenFalse")
    @builtins.classmethod
    def when_false(
        cls,
        key: ConditionKey,
        if_exists: typing.Optional[builtins.bool] = None,
    ) -> "BoolConstraint":
        '''
        :param key: -
        :param if_exists: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d5d597243c66776ca177a81a1762dfaf2654a2a5d83cf09acc5cac2ef78765)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument if_exists", value=if_exists, expected_type=type_hints["if_exists"])
        return typing.cast("BoolConstraint", jsii.sinvoke(cls, "whenFalse", [key, if_exists]))

    @jsii.member(jsii_name="whenTrue")
    @builtins.classmethod
    def when_true(
        cls,
        key: ConditionKey,
        if_exists: typing.Optional[builtins.bool] = None,
    ) -> "BoolConstraint":
        '''
        :param key: -
        :param if_exists: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51795feaeae3c10e9d4e69e13c4d509808ee38146f17cacdccadccbeeb527b4d)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument if_exists", value=if_exists, expected_type=type_hints["if_exists"])
        return typing.cast("BoolConstraint", jsii.sinvoke(cls, "whenTrue", [key, if_exists]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: PolicyType,
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0080cb7933ead24b0a2b94e2fe141f81ace8d955195e032d4314d09f29e377c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))


class CalledViaConstraint(
    Constraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.CalledViaConstraint",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="calledVia")
    @builtins.classmethod
    def called_via(cls, service: CalledViaServicePrincipal) -> "CalledViaConstraint":
        '''
        :param service: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d91c7098edf84f5aba8fa1d6894dca3c84c165cb08b49866c3e79ea1d0774000)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast("CalledViaConstraint", jsii.sinvoke(cls, "calledVia", [service]))

    @jsii.member(jsii_name="calledViaFirst")
    @builtins.classmethod
    def called_via_first(
        cls,
        service: CalledViaServicePrincipal,
    ) -> "CalledViaConstraint":
        '''
        :param service: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816104e2242cb9865a94a41de5c15dd32938f3bb60b9867cdc82ae4b4eafc609)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast("CalledViaConstraint", jsii.sinvoke(cls, "calledViaFirst", [service]))

    @jsii.member(jsii_name="calledViaFirstAndLast")
    @builtins.classmethod
    def called_via_first_and_last(
        cls,
        first_service: CalledViaServicePrincipal,
        last_service: CalledViaServicePrincipal,
    ) -> "CalledViaConstraint":
        '''
        :param first_service: -
        :param last_service: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e33c254fdb5bd3bad803f474feb40e30a6b3a03736885b1f23b9f3f347fca101)
            check_type(argname="argument first_service", value=first_service, expected_type=type_hints["first_service"])
            check_type(argname="argument last_service", value=last_service, expected_type=type_hints["last_service"])
        return typing.cast("CalledViaConstraint", jsii.sinvoke(cls, "calledViaFirstAndLast", [first_service, last_service]))

    @jsii.member(jsii_name="calledViaLast")
    @builtins.classmethod
    def called_via_last(
        cls,
        service: CalledViaServicePrincipal,
    ) -> "CalledViaConstraint":
        '''
        :param service: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9433bd06789d0ef8b4c3cf9684eee9b82e7c19630e6d58163183a76520736a0e)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast("CalledViaConstraint", jsii.sinvoke(cls, "calledViaLast", [service]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: PolicyType,
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2df4e2451b675bdd0d5e1696815d3813e0c31da3425cc6c05e400ead8f76aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))


class ClaimConstraint(
    Constraint,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/cdk-iam-utilities.ClaimConstraint",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        operator: ConditionOperator,
        claim: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: -
        :param claim: -
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e5a5771b4a78d946cd173873df7fe2bd2dde4bca81ffd231eee467f52f0160)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        jsii.create(self.__class__, self, [operator, claim, values])

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: PolicyType,
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937c46518c3bd6526a466ce359efb5979dfe39ac2ff510c717cec8917c3af4a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))

    @builtins.property
    @jsii.member(jsii_name="claim")
    def claim(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "claim"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> ConditionOperator:
        '''
        :stability: experimental
        '''
        return typing.cast(ConditionOperator, jsii.get(self, "operator"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))


class _ClaimConstraintProxy(
    ClaimConstraint,
    jsii.proxy_for(Constraint), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ClaimConstraint).__jsii_proxy_class__ = lambda : _ClaimConstraintProxy


class ClaimsIamResourcePathBuilder(
    IamResourcePathBuilder,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/cdk-iam-utilities.ClaimsIamResourcePathBuilder",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        options: typing.Union[ClaimsIamResourcePathBuilderSettings, typing.Dict[builtins.str, typing.Any]],
        path: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param options: -
        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97c0392fc4a278903c0ddf8753edc7c447ee758b97ff3124ab8bd53dab287c3)
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        jsii.create(self.__class__, self, [options, path])

    @jsii.member(jsii_name="appendClaim")
    def _append_claim(self, *claims: builtins.str) -> typing.List[builtins.str]:
        '''
        :param claims: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821be2f30043d4d25b7f44beb9183459cf7e7d44369e31037a46c98d0bf395d9)
            check_type(argname="argument claims", value=claims, expected_type=typing.Tuple[type_hints["claims"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "appendClaim", [*claims]))

    @jsii.member(jsii_name="appendValue")
    def _append_value(self, *values: builtins.str) -> typing.List[builtins.str]:
        '''
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc758c2e292d5075747beacabcbe8c7bb13e574769ca70e87124a99926a1f497)
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "appendValue", [*values]))

    @builtins.property
    @jsii.member(jsii_name="options")
    def _options(self) -> ClaimsIamResourcePathBuilderSettings:
        '''
        :stability: experimental
        '''
        return typing.cast(ClaimsIamResourcePathBuilderSettings, jsii.get(self, "options"))


class _ClaimsIamResourcePathBuilderProxy(
    ClaimsIamResourcePathBuilder,
    jsii.proxy_for(IamResourcePathBuilder), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ClaimsIamResourcePathBuilder).__jsii_proxy_class__ = lambda : _ClaimsIamResourcePathBuilderProxy


@jsii.implements(IConstraintsBuilder)
class ConstraintsBuilder(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/cdk-iam-utilities.ConstraintsBuilder",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        *,
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> None:
        '''
        :param claims_context: 

        :stability: experimental
        '''
        settings = ConstraintsBuilderSettings(claims_context=claims_context)

        jsii.create(self.__class__, self, [settings])

    @jsii.member(jsii_name="add")
    def add(
        self,
        constraint: Constraint,
        *additional_constraints: Constraint,
    ) -> "ConstraintsBuilder":
        '''
        :param constraint: -
        :param additional_constraints: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9832a043d3b84dff72d0770c1b08dfd899cfce638fe3f87af40335fcfd9555a9)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
            check_type(argname="argument additional_constraints", value=additional_constraints, expected_type=typing.Tuple[type_hints["additional_constraints"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ConstraintsBuilder", jsii.invoke(self, "add", [constraint, *additional_constraints]))

    @builtins.property
    @jsii.member(jsii_name="constraints")
    def constraints(self) -> typing.List[Constraint]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[Constraint], jsii.get(self, "constraints"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> ConstraintsBuilderSettings:
        '''
        :stability: experimental
        '''
        return typing.cast(ConstraintsBuilderSettings, jsii.get(self, "settings"))


class _ConstraintsBuilderProxy(ConstraintsBuilder):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ConstraintsBuilder).__jsii_proxy_class__ = lambda : _ConstraintsBuilderProxy


class GenericClaimsIamResourcePathBuilder(
    ClaimsIamResourcePathBuilder,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.GenericClaimsIamResourcePathBuilder",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        claims_context: IClaimsContext,
    ) -> "GenericClaimsIamResourcePathBuilder":
        '''
        :param claims_context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273f1cf752c89b3a54cb258d9b72261b56d868b8e8355ed8ced2aae69d2b28ac)
            check_type(argname="argument claims_context", value=claims_context, expected_type=type_hints["claims_context"])
        return typing.cast("GenericClaimsIamResourcePathBuilder", jsii.sinvoke(cls, "create", [claims_context]))

    @jsii.member(jsii_name="claim")
    def claim(
        self,
        claim: builtins.str,
        *additional_claims: builtins.str,
    ) -> "GenericClaimsIamResourcePathBuilder":
        '''
        :param claim: -
        :param additional_claims: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64530078bd711afdfc1ed667cf2a78457056b81738208eb9ef9cc773e98aeb2e)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument additional_claims", value=additional_claims, expected_type=typing.Tuple[type_hints["additional_claims"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("GenericClaimsIamResourcePathBuilder", jsii.invoke(self, "claim", [claim, *additional_claims]))

    @jsii.member(jsii_name="policyVariable")
    def policy_variable(
        self,
        value: PolicyVariable,
    ) -> "GenericClaimsIamResourcePathBuilder":
        '''
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6480e59b2c8ff931a655f8a5fa0c100dee7dabb59ba6588e14765e2b2d5e5e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("GenericClaimsIamResourcePathBuilder", jsii.invoke(self, "policyVariable", [value]))

    @jsii.member(jsii_name="text")
    def text(
        self,
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> "GenericClaimsIamResourcePathBuilder":
        '''
        :param value: -
        :param additional_values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8100ee3a1aa1449c267e890d11811c0bc3a34b449290e581f1cfb3cc26a3f785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("GenericClaimsIamResourcePathBuilder", jsii.invoke(self, "text", [value, *additional_values]))

    @jsii.member(jsii_name="value")
    def value(
        self,
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> "GenericClaimsIamResourcePathBuilder":
        '''
        :param value: -
        :param additional_values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a22a9b96555144009a8f776fb7c18fce95ea4da037a701ac4ef5b5502ecdec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("GenericClaimsIamResourcePathBuilder", jsii.invoke(self, "value", [value, *additional_values]))


class GlobalBoolConditionKey(
    BoolConditionKey,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.GlobalBoolConditionKey",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="toBoolFalseConstraint")
    def to_bool_false_constraint(
        self,
        if_exists: typing.Optional[builtins.bool] = None,
    ) -> BoolConstraint:
        '''
        :param if_exists: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236c930986fcc29cd7dc5c8558ec1bab9c90ccc99f361821cf6b0565ec2d771d)
            check_type(argname="argument if_exists", value=if_exists, expected_type=type_hints["if_exists"])
        return typing.cast(BoolConstraint, jsii.invoke(self, "toBoolFalseConstraint", [if_exists]))

    @jsii.member(jsii_name="toBoolTrueConstraint")
    def to_bool_true_constraint(
        self,
        if_exists: typing.Optional[builtins.bool] = None,
    ) -> BoolConstraint:
        '''
        :param if_exists: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83bddc77255df570cc6820ec266bb242bd9e90dbd48b1ffcab97d959f935f1a5)
            check_type(argname="argument if_exists", value=if_exists, expected_type=type_hints["if_exists"])
        return typing.cast(BoolConstraint, jsii.invoke(self, "toBoolTrueConstraint", [if_exists]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MultiFactorAuthPresent")
    def MULTI_FACTOR_AUTH_PRESENT(cls) -> "GlobalBoolConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalBoolConditionKey", jsii.sget(cls, "MultiFactorAuthPresent"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PrincipalIsAWSService")
    def PRINCIPAL_IS_AWS_SERVICE(cls) -> "GlobalBoolConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalBoolConditionKey", jsii.sget(cls, "PrincipalIsAWSService"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SecureTransport")
    def SECURE_TRANSPORT(cls) -> "GlobalBoolConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalBoolConditionKey", jsii.sget(cls, "SecureTransport"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ViaAWSService")
    def VIA_AWS_SERVICE(cls) -> "GlobalBoolConditionKey":
        '''
        :stability: experimental
        '''
        return typing.cast("GlobalBoolConditionKey", jsii.sget(cls, "ViaAWSService"))


class PrincipalTagConstraint(
    TagConstraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.PrincipalTagConstraint",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="stringEquals")
    @builtins.classmethod
    def string_equals(
        cls,
        tag_name: builtins.str,
        value: builtins.str,
        *values: builtins.str,
    ) -> "PrincipalTagConstraint":
        '''
        :param tag_name: -
        :param value: -
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceaf3dfc71e6e12a597a66192b395d17819740589858e7ad18220d7d6da8df33)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("PrincipalTagConstraint", jsii.sinvoke(cls, "stringEquals", [tag_name, value, *values]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: PolicyType,
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1bb239c940202e223b2120009114f831e2e9818ebc75c3294b3ffb17b89e4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))


class RequestTagConstraint(
    TagConstraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.RequestTagConstraint",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="stringEquals")
    @builtins.classmethod
    def string_equals(
        cls,
        tag_name: builtins.str,
        value: builtins.str,
        *values: builtins.str,
    ) -> "RequestTagConstraint":
        '''
        :param tag_name: -
        :param value: -
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0c972428d1b34ec550967834cd999dd27f133f321f3fce0acd3da06111c1f1)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RequestTagConstraint", jsii.sinvoke(cls, "stringEquals", [tag_name, value, *values]))

    @jsii.member(jsii_name="stringLike")
    @builtins.classmethod
    def string_like(
        cls,
        tag_name: builtins.str,
        value: builtins.str,
        *values: builtins.str,
    ) -> "RequestTagConstraint":
        '''
        :param tag_name: -
        :param value: -
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d7f1113cceac6a2ace4547b83a83cfa8fb73bd00e46ca12399c2161dcf58ed)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RequestTagConstraint", jsii.sinvoke(cls, "stringLike", [tag_name, value, *values]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: PolicyType,
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e3d08972f3798d79493327b670a8cb31d68263aa502a589c92475d93f27b52)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))


class ResourceTagConstraint(
    TagConstraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/cdk-iam-utilities.ResourceTagConstraint",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        operator: StringConditionOperator,
        tag_name: builtins.str,
        value: builtins.str,
        *values: builtins.str,
    ) -> "ResourceTagConstraint":
        '''
        :param operator: -
        :param tag_name: -
        :param value: -
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2817d1c353cac56ec38fca25cdb72c8ea37003abab27868eb4dc738914ab0178)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ResourceTagConstraint", jsii.sinvoke(cls, "create", [operator, tag_name, value, *values]))

    @jsii.member(jsii_name="stringEquals")
    @builtins.classmethod
    def string_equals(
        cls,
        tag_name: builtins.str,
        value: builtins.str,
        *values: builtins.str,
    ) -> "ResourceTagConstraint":
        '''
        :param tag_name: -
        :param value: -
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4002ac4f79d03824b891d4de4a6e03558a4b235738be383a4a0b8d394c8e9788)
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ResourceTagConstraint", jsii.sinvoke(cls, "stringEquals", [tag_name, value, *values]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: PolicyType,
        claims_context: typing.Optional[IClaimsContext] = None,
    ) -> typing.List[ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf454643235f2452c91af901a3ab5a6ec1f888a58c5f72fe752e535a3a9310e6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))


__all__ = [
    "ArnConditionOperator",
    "AwsFederatedProviderConditionKey",
    "AwsPrincipalTagConditionKey",
    "AwsRequestTagConditionKey",
    "AwsResourceTagConditionKey",
    "AwsSourceVpcConditionKey",
    "BoolConditionKey",
    "BoolConstraint",
    "CalledViaConstraint",
    "CalledViaServicePrincipal",
    "Claim",
    "ClaimConstraint",
    "ClaimsIamResourcePathBuilder",
    "ClaimsIamResourcePathBuilderSettings",
    "ClaimsUtility",
    "ConditionKey",
    "ConditionKeySettings",
    "ConditionOperator",
    "Constraint",
    "ConstraintAssembleContext",
    "ConstraintPolicyMutation",
    "ConstraintPolicyMutationType",
    "ConstraintUtilitySettings",
    "ConstraintsBuilder",
    "ConstraintsBuilderSettings",
    "ConstraintsUtility",
    "DateConstraint",
    "GenericClaimsIamResourcePathBuilder",
    "GenericConditionKey",
    "GenericConstraint",
    "GlobalBoolConditionKey",
    "GlobalConditionKey",
    "IClaimsContext",
    "IConstraintsBuilder",
    "IIamResourcePath",
    "IMappedClaims",
    "IamResourcePathBuilder",
    "IamResourceTagConditionKey",
    "IpAddressConditionOperator",
    "MappedClaims",
    "NullConstraint",
    "OperatorUtils",
    "PassClaimsConstraint",
    "PassClaimsConstraintSettings",
    "PolicyType",
    "PolicyVariable",
    "PrincipalTagConstraint",
    "PrincipalType",
    "RequestTagConstraint",
    "ResourcePolicyType",
    "ResourceTagConstraint",
    "StringConditionOperator",
    "StringMultiValueConditionOperator",
    "StsCognitoIdentityConstraint",
    "StsServiceConditionKey",
    "StsTransitiveTagKeysConstraint",
    "TagConstraint",
    "TagKeysConstraint",
]

publication.publish()

def _typecheckingstub__ab25c6309333e6584c398c621174042fdfb5012f94c17be42b53ab2cc9b266dc(
    *,
    name: builtins.str,
    tag_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0317f73650c04e91692ffec0edb82d3ce0a71629f2f57aa04cda5688fe984661(
    *,
    claims_context: IClaimsContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a356deb85e8c63ad361d1eb5f7e12a40c7326a862c7032f99a3a1553b91c1ba5(
    context: IClaimsContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5718b11866e4b3aab2dc7baa7263d4d6318f667c4a5d8d104785d87635d22e(
    claim: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0583a87b24d891bb0df6eb7993caa44fd2374e6676bd75f4db18d4e1f1881043(
    claim: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8f0353c4210b3f52c4d274ae44921c9f937056c0c47c95c50b029eadbaf2be(
    scope: _constructs_77d1e7e8.Construct,
    claim: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ac86b0aed994242823fe1a55a5b5f1ad2ccb2bae3b64bc7fcee64891a6ed71(
    claim: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5412030d13299c5c30b54c36b080e24f1f859865109b8669b52374f6252be1d1(
    name: builtins.str,
    *,
    supported_operators: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d15eae8e900b27091d34838b9120d39b07b555eb7d984f5943081e6ae2300d(
    *,
    supported_operators: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3554a7416b8f4325bad1fcd245ed1b4a55aacd87adb9ae78b49ae1e9d4b2923c(
    key: ConditionKey,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78512b1ae9454b85939b9732af5a8c6e813419973de1d01fc7c98f805c9a9cc2(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2863a74feda187cf9c7428a7acb3c75561d377d334bbce8ebc9980cfb73f988(
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f4d85ef5f1e6942b1ccbff7fa8879ab6331a388eb63dff395619cf0e4eeb0a(
    *,
    key: ConditionKey,
    operator: ConditionOperator,
    type: ConstraintPolicyMutationType,
    value: typing.Sequence[typing.Any],
    actions_match_service: typing.Optional[builtins.str] = None,
    order: typing.Optional[jsii.Number] = None,
    strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8202a24804394817fbbdfa37ce377a9161710e16f06238342326944636ab46(
    *,
    policy_type: PolicyType,
    append_condition_values: typing.Optional[builtins.bool] = None,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0bb2cf82c461dbaed99d2b9387bf74b270114927f3b4500911fe2032887e59(
    *,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bff860b975c707fa9fd54d708b6ac2b5cf35ea2c2608acca3bd4b21c26490bd(
    constraints: typing.Sequence[Constraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325002ec7621292d99171ac86ec16036443d8414671cab78972916d40a137264(
    scope: _constructs_77d1e7e8.Construct,
    settings: typing.Union[ConstraintUtilitySettings, typing.Dict[builtins.str, typing.Any]],
    grant: _aws_cdk_aws_iam_ceddda9d.Grant,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2dfdf69b0d2e1a41d8274bec1b68b48b68db05fbb4acb7997fbc8949589707(
    scope: _constructs_77d1e7e8.Construct,
    settings: typing.Union[ConstraintUtilitySettings, typing.Dict[builtins.str, typing.Any]],
    policy_statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4992c18f8a0db5811b6d76506dbd028413eda56be7be629ab03aec38e2e4d85(
    key: ConditionKey,
    from_: datetime.datetime,
    to: datetime.datetime,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc8cfaa4a7e50633fa490fcfad37b0aa1e1b812f45133a9ef71b2a9c37a3b71(
    key: ConditionKey,
    date: datetime.datetime,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18eba81bcc8d9cecb2480c521f139d67172ef1e24866864bff6ce9f0c3de3ddc(
    key: ConditionKey,
    date: datetime.datetime,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b23c6608a91ebbb65c20252e74279635ccf77e22ee2acd1b266d9898d825f35(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3919b9b736f87daa6d0e2684a80fc75b05b31f28edf68f9016ca7d3a36984640(
    name: builtins.str,
    *,
    supported_operators: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc6d56ac9755bf1c9d32d04f4b771dbe5c3e436767a17a8bea59c23010f0143(
    operator: ConditionOperator,
    key: ConditionKey,
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e18ea26ae53c1a58603c85c38641087e286d6db9153b9fd74d42ab6f55769f(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aefa7245f6d829948254ee45c80e68195f85098c711c878cacb3dfdb67d4479(
    tag_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3817ac0061bbb05b1fa3605c686b667f95aa4b4bb0043641016b74eeccd9fb6a(
    tag_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a171c8016e1c970bc8ff80e029f7183e923e1b4417fcec179055886649c2303d(
    tag_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6db3a31b14dc73a7ad1fbb2bd3ed0aef04ede0ab59b100cf638cddc64987a2(
    operator: ConditionOperator,
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba1e72ca0a3003f8df7f5496395661bfafc24cedfd038bf2e22c1067f90896ad(
    path: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d579f24ae2420110c9c7fff9581283e01cac2a05785b7ee0490e58d4cc8d60(
    policy_variable: PolicyVariable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7eb01baa4d9c06bf4268d443321102495cd9df3cf50b92db5350afd328998ce(
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030a7bfd41157f13c93d46727685067ac955c3140c95dcdf8b11b6b027044b1d(
    tag_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e711bf055273418ac3ba61f42de5b832c88a434f94d54c2d2b914647eeb61554(
    claim: builtins.str,
    *additional_claims: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bcc6095d8f2766a839d79d92afef176839c9e97fe75c204245ee2428729ace2(
    claims: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5999407d1006bcfcd695c3e91204050d66d5fca2a57aa8b0b2f364a1b510ac(
    key: ConditionKey,
    is_null: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4293d5f1c3aa4f036928c8834639298950ef25d6a46253f7e64ccfd3d1b1c8(
    key: ConditionKey,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b39095ecd276d15bab406a4d6b27214f44e0662fe5d5aaa692f2a1e307f4d3(
    key: ConditionKey,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e64cd196439f79b45dc041c976004a54872cad55227156ba3488b656f6584e(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d3f7b564d18a0f22f7b97e970c9e6dfa1d47339825a88598c2844533e9a410(
    value: ConditionOperator,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1dce653b1ac742d1f45816e7704a5f56a7cef1b8dba7fdafb34937386223c19(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31efcd8d4fbd78fef9330070e8016aaf02f4b0882626bfc2b088512203f336cd(
    supported_operators: typing.Sequence[builtins.str],
    operator: ConditionOperator,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be7b72649f14a5c461b6d971c62f67f4d66f0a8e9fd1583f81d480d9fc61a96(
    operator: ConditionOperator,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f387b0bc01f59b65dfc380d9b67da751e6b78ddb04ae9a970ee2f97db95653c(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed089b1d5517d7b95e7e69859d1f621cb27884a1dfbf2b81b7afec5d7aff152(
    *,
    allow_any_tags: builtins.bool,
    claims: typing.Mapping[builtins.str, builtins.str],
    specifically_allowed_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1488aab025da2f6ebe837b89cd7d4d152b1a9ede9a20d7f699aded9437cc3b(
    type: ResourcePolicyType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c35d7afcfe150bef534798fbf915f3bbf72ed6fcc34142e86ad7556b4034ef(
    principal_type: PrincipalType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929540b146757b024841c74dcecbcb001b2b0c94c3910ed102951d755674516b(
    service: ResourcePolicyType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bccd0b528f3b8e599b67953eafb64f9fab704c22221ad16dd6f3b51546e902ff(
    default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a3facd6bb8b1c1f9bb9306169f86328fb37f31579149f4c5e3b3f692706789(
    tag_name: builtins.str,
    default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a03101e09da0f49d5a1d6e3f636ca9ed765f56d0484fd8f8c22a903404d561(
    default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3638d25c3dc30d928c8d1bbe488b7152d1fab341bef38474160d9925506127(
    tag_name: builtins.str,
    default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883cda25eaf830ee9d8700fc6a11edeba6785a3280bc35df7fa5f34711f5505b(
    tag_name: builtins.str,
    default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08288fcc4d04360808bfb0a61c743a193ee5405701fd7a5aa3a65433f6d5a333(
    default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a1da200217adabcdc65a4c18e6d944df345f831bc517251ea247c586d34368(
    default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02db5ce86332fc29de0795c8c2d47dbe9d0d2b9205f06263b8d4acfee0b5fe52(
    identity_pool_id: builtins.str,
    amr: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8056bf07a1aa9c5c0884f21f5f45814a4cfb966c1657b8321e3a793ceecee0(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23405446a48da79d84427a4652cf6d05a247906574ad6abe1b5656f49de09201(
    tag_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02d97fabc6c222666aeaa70205e42ac5eca657ae270c8fccd3f0f18980795c0(
    value: builtins.str,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c46fa22e756540429e63a748dddbc3ba28221d1abc275d60cf3aefba145b524(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef7bb46e092f123fecb0a805198943cb6d59203ac304e40b656a63f121439ef(
    operator: StringMultiValueConditionOperator,
    is_not_null: builtins.bool,
    value: builtins.str,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ae7e09f0cf786d7b0154550eda9cbd7325103a8ada8589cb31865fe3007b63(
    value: builtins.str,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8786f6943acbde741df4330fb047d08591c1ea25a76842474c7f89ea3c8c1c8a(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e5f880a5a6fe3634905ff9ad29a9d68406f8420aa0965f8e003419e2f1e9da(
    operator: ConditionOperator,
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63105a32ff71051a6c3cc27b2839db2f72f20682827817c48a187a7bf39c8dfd(
    tag_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9d1a0a21b769887be63db19eb4f8f4e07e88a05fb96e194758b0f6b6ba8c15(
    tag_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f5027064337667f0800910638b4d6ab2fa5bfae1200e99f94cb75c1a2383d7(
    tag_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50ea1ebc36b9b83d2846758a38755f21b6f8fe320ee31399b9bd2fc1ecba54f(
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c112a49f3c459488620bb543f8e87a68ea99572eb957237b69c593faeb09d3(
    name: builtins.str,
    *,
    supported_operators: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d5d597243c66776ca177a81a1762dfaf2654a2a5d83cf09acc5cac2ef78765(
    key: ConditionKey,
    if_exists: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51795feaeae3c10e9d4e69e13c4d509808ee38146f17cacdccadccbeeb527b4d(
    key: ConditionKey,
    if_exists: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0080cb7933ead24b0a2b94e2fe141f81ace8d955195e032d4314d09f29e377c(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91c7098edf84f5aba8fa1d6894dca3c84c165cb08b49866c3e79ea1d0774000(
    service: CalledViaServicePrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816104e2242cb9865a94a41de5c15dd32938f3bb60b9867cdc82ae4b4eafc609(
    service: CalledViaServicePrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33c254fdb5bd3bad803f474feb40e30a6b3a03736885b1f23b9f3f347fca101(
    first_service: CalledViaServicePrincipal,
    last_service: CalledViaServicePrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9433bd06789d0ef8b4c3cf9684eee9b82e7c19630e6d58163183a76520736a0e(
    service: CalledViaServicePrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2df4e2451b675bdd0d5e1696815d3813e0c31da3425cc6c05e400ead8f76aa(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e5a5771b4a78d946cd173873df7fe2bd2dde4bca81ffd231eee467f52f0160(
    operator: ConditionOperator,
    claim: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937c46518c3bd6526a466ce359efb5979dfe39ac2ff510c717cec8917c3af4a6(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97c0392fc4a278903c0ddf8753edc7c447ee758b97ff3124ab8bd53dab287c3(
    options: typing.Union[ClaimsIamResourcePathBuilderSettings, typing.Dict[builtins.str, typing.Any]],
    path: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821be2f30043d4d25b7f44beb9183459cf7e7d44369e31037a46c98d0bf395d9(
    *claims: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc758c2e292d5075747beacabcbe8c7bb13e574769ca70e87124a99926a1f497(
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9832a043d3b84dff72d0770c1b08dfd899cfce638fe3f87af40335fcfd9555a9(
    constraint: Constraint,
    *additional_constraints: Constraint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273f1cf752c89b3a54cb258d9b72261b56d868b8e8355ed8ced2aae69d2b28ac(
    claims_context: IClaimsContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64530078bd711afdfc1ed667cf2a78457056b81738208eb9ef9cc773e98aeb2e(
    claim: builtins.str,
    *additional_claims: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6480e59b2c8ff931a655f8a5fa0c100dee7dabb59ba6588e14765e2b2d5e5e77(
    value: PolicyVariable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8100ee3a1aa1449c267e890d11811c0bc3a34b449290e581f1cfb3cc26a3f785(
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a22a9b96555144009a8f776fb7c18fce95ea4da037a701ac4ef5b5502ecdec1(
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236c930986fcc29cd7dc5c8558ec1bab9c90ccc99f361821cf6b0565ec2d771d(
    if_exists: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bddc77255df570cc6820ec266bb242bd9e90dbd48b1ffcab97d959f935f1a5(
    if_exists: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceaf3dfc71e6e12a597a66192b395d17819740589858e7ad18220d7d6da8df33(
    tag_name: builtins.str,
    value: builtins.str,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1bb239c940202e223b2120009114f831e2e9818ebc75c3294b3ffb17b89e4b(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0c972428d1b34ec550967834cd999dd27f133f321f3fce0acd3da06111c1f1(
    tag_name: builtins.str,
    value: builtins.str,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d7f1113cceac6a2ace4547b83a83cfa8fb73bd00e46ca12399c2161dcf58ed(
    tag_name: builtins.str,
    value: builtins.str,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e3d08972f3798d79493327b670a8cb31d68263aa502a589c92475d93f27b52(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2817d1c353cac56ec38fca25cdb72c8ea37003abab27868eb4dc738914ab0178(
    operator: StringConditionOperator,
    tag_name: builtins.str,
    value: builtins.str,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4002ac4f79d03824b891d4de4a6e03558a4b235738be383a4a0b8d394c8e9788(
    tag_name: builtins.str,
    value: builtins.str,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf454643235f2452c91af901a3ab5a6ec1f888a58c5f72fe752e535a3a9310e6(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: PolicyType,
    claims_context: typing.Optional[IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass
