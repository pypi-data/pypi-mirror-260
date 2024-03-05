# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
class SagemakerSQLError(Exception):
    """
    Generic exception that is the base exception for all other Errors from this lib
    """

    pass


class SagemakerSQLFault(Exception):
    """
    Generic exception that is the base exception for all other Faults from this lib
    """

    pass


class SagemakerSQLResponseAdapterFault(SagemakerSQLFault):
    """
    Fault thrown during response adapter operations
    """

    pass


class SagemakerSQLDataProviderServiceFault(SagemakerSQLFault):
    """
    Fault thrown during data provider service operations
    """

    pass


class SagemakerSQLDataProviderServiceError(SagemakerSQLError):
    """
    Error thrown during data provider service operations
    """

    pass


class SagemakerSQLApiServiceFault(SagemakerSQLFault):
    """
    Fault thrown during api service operations
    """

    pass


class SagemakerSQLApiServiceError(SagemakerSQLError):
    """
    Error thrown during api service operations
    """

    pass


class SagemakerSQLApiHandlerFault(SagemakerSQLFault):
    """
    Fault thrown during api handler operations
    """

    pass


class SagemakerSQLApiHandlerError(SagemakerSQLError):
    """
    Error thrown during api handler operations
    """

    pass


class SagemakerSQLPaginationError(SagemakerSQLError):
    """
    Error thrown during pagination operations
    """

    pass


class SagemakerSQLPaginationFault(SagemakerSQLFault):
    """
    Fault thrown during pagination operations
    """

    pass
