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
