from pingsafe_cli.psgraph.common.models.enums import CheckCategories
from pingsafe_cli.psgraph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck
from pingsafe_cli.psgraph.common.models.consts import ANY_VALUE


class MemoryDBEncryptionWithCMK(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure MemoryDB is encrypted at rest using KMS CMKs"
        id = "CKV_AWS_201"
        supported_resources = ['aws_memorydb_cluster']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return 'kms_key_arn'

    def get_expected_value(self):
        return ANY_VALUE


check = MemoryDBEncryptionWithCMK()
