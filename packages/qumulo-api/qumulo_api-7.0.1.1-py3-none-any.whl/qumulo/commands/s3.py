# Copyright (c) 2022 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import argparse
import json

from dataclasses import asdict
from typing import Any, Dict, List, Sequence

import qumulo.lib.opts
import qumulo.rest.s3 as s3

from qumulo.lib.identity_util import Identity
from qumulo.lib.request import pretty_json
from qumulo.lib.util import tabulate
from qumulo.rest_client import RestClient


class GetSettingsCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_get_settings'
    SYNOPSIS = 'Get S3 server settings'

    @staticmethod
    def main(rest_client: RestClient, _args: argparse.Namespace) -> None:
        print(rest_client.s3.get_settings().to_json())


class ModifySettingsCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_modify_settings'
    SYNOPSIS = 'Modify S3 server settings'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        enable_group = parser.add_mutually_exclusive_group()
        enable_group.add_argument(
            '--disable',
            '-d',
            dest='enabled',
            help='Disable S3 server',
            action='store_false',
            default=None,
        )
        enable_group.add_argument(
            '--enable',
            '-e',
            dest='enabled',
            help='Enable S3 server',
            action='store_true',
            default=None,
        )
        parser.add_argument(
            '--base-path',
            dest='base_path',
            help=(
                'The directory which will be the parent of all buckets created without an'
                ' explicitly specified path.'
            ),
            required=False,
        )
        parser.add_argument(
            '--multipart-upload-expiry-interval',
            dest='multipart_upload_expiry_interval',
            help=(
                'If a multipart upload is not modified in this amount of time, it is considered'
                ' stale and may be cleaned up automatically. The duration must be in the format'
                ' <quantity><units> where <quantity> is a positive integer less than 100 and'
                ' <units> is one of [months, weeks, days, hours] (e.g. 5days). To disable'
                " automatic cleanup, specify 'never' for the duration."
            ),
            required=False,
            default=None,
        )
        secure_group = parser.add_mutually_exclusive_group()
        secure_group.add_argument(
            '--secure',
            dest='secure',
            help='Configure the S3 server to only accept HTTPS connections',
            action='store_true',
            default=None,
        )
        secure_group.add_argument(
            '--insecure',
            dest='secure',
            help='Configure the S3 server to only accept HTTP connections',
            action='store_false',
            default=None,
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if (
            args.enabled is None
            and args.base_path is None
            and args.multipart_upload_expiry_interval is None
            and args.secure is None
        ):
            err_msg = (
                'At least one of the following arguments is required: [--disable, --enable,'
                ' --base-path, --multipart-upload-expiry-interval, --secure, --insecure]'
            )

            raise ValueError(err_msg)

        config = s3.ConfigPatch()

        if args.enabled is not None:
            config.enabled = args.enabled
        if args.base_path is not None:
            config.base_path = args.base_path
        if args.multipart_upload_expiry_interval is not None:
            config.multipart_upload_expiry_interval = args.multipart_upload_expiry_interval
        if args.secure is not None:
            config.secure = args.secure

        print(rest_client.s3.modify_settings(config).to_json())


def make_access_keys_table(
    keys: Sequence[s3.AccessKeyDescription], display_headers: bool = True
) -> str:
    headers = ['access_key_id', 'owner', 'creation_time'] if display_headers else None
    rows = []
    for key in keys:
        row = []
        row.append(key.access_key_id)
        row.append(str(Identity(key.owner)))
        row.append(key.creation_time)
        rows.append(row)
    return tabulate(rows, headers)


class ListAccessKeysCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_list_access_keys'
    SYNOPSIS = 'List S3 access keys'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--json', action='store_true', help='Output JSON instead of table.')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        def list_access_keys_tab(rest_client: RestClient) -> None:
            results = rest_client.s3.list_access_keys()
            print(make_access_keys_table(results.entries, True))
            while results.paging.next:
                results = rest_client.s3.list_access_keys(start_at=results.paging.next)
                print(make_access_keys_table(results.entries, False))

        def list_access_keys_json(rest_client: RestClient) -> None:
            def append_asdict(
                trg: List[Dict[str, Any]], src: Sequence[s3.AccessKeyDescription]
            ) -> None:
                for access_key in src:
                    trg.append(asdict(access_key))

            entries: List[Dict[str, Any]] = []
            response = rest_client.s3.list_access_keys()
            append_asdict(entries, response.entries)
            while response.paging.next is not None:
                response = rest_client.s3.list_access_keys(start_at=response.paging.next)
                append_asdict(entries, response.entries)

            print(pretty_json({'entries': entries}))

        if args.json:
            list_access_keys_json(rest_client)
        else:
            list_access_keys_tab(rest_client)


class CreateAccessKeyCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_create_access_key'
    SYNOPSIS = 'Create S3 access key'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        identity = parser.add_mutually_exclusive_group(required=True)
        identity.add_argument(
            'identifier',
            nargs='?',
            help=(
                'An auth_id, SID, or name optionally qualified with a domain prefix (e.g '
                '"local:name", "ad:name", "AD\\name") or an ID type (e.g. "auth_id:513", '
                '"SID:S-1-1-0"). Groups are not supported for access keys, must be a user.'
            ),
        )
        identity.add_argument('--auth-id', type=int, help='Auth ID of the qumulo user')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        client = rest_client

        if args.auth_id:
            identity = Identity({'auth_id': str(args.auth_id)})
        else:
            identity = Identity(args.identifier)

        print(pretty_json(asdict(client.s3.create_access_key(identity))))


class DeleteAccessKeyCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_delete_access_key'
    SYNOPSIS = 'Delete an S3 access key'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--id', type=str, help='The ID of the access key to be deleted', required=True
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        rest_client.s3.delete_access_key(args.id)


def make_buckets_table(buckets: Sequence[s3.BucketDescription]) -> str:
    headers = ['name', 'creation_time', 'path']
    rows = []
    for bucket in buckets:
        row = []
        row.append(bucket.name)
        row.append(bucket.creation_time)
        row.append(bucket.path)
        rows.append(row)
    return tabulate(rows, headers)


class ListBucketsCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_list_buckets'
    SYNOPSIS = 'List all S3 buckets'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--json', action='store_true', help='Output JSON instead of table')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        results = rest_client.s3.list_buckets()
        if args.json:
            buckets = asdict(results)
            for bucket in buckets['buckets']:
                bucket.pop('anonymous_access_enabled')  # DEPRECATED
            print(pretty_json(buckets))
        else:
            print(make_buckets_table(results.buckets))


class GetBucketCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_get_bucket'
    SYNOPSIS = 'Get details for an S3 bucket'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--name', help='The name of the bucket to retrieve', required=True)

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        results = rest_client.s3.list_buckets()
        for bucket in results.buckets:
            if bucket.name == args.name:
                bucket_dict = asdict(bucket)
                bucket_dict.pop('anonymous_access_enabled')  # DEPRECATED
                print(pretty_json(bucket_dict))
                return
        print(f'"{args.name}" not found.')


class CreateBucketCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_add_bucket'
    SYNOPSIS = 'Create an S3 bucket'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--name', help='The name of the bucket to be created', required=True)
        parser.add_argument(
            '--fs-path',
            help=(
                'The absolute path to be used as the root of the bucket. The user must have'
                ' permissions to read the directory.'
            ),
            required=False,
        )
        parser.add_argument(
            '--create-fs-path',
            help=(
                'Creates the bucket root if it does not exist. '
                'The user must have permission to create the directory.'
            ),
            action='store_true',
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.fs_path is None and args.create_fs_path:
            err_msg = '--create-fs-path can only be specified if --fs-path is provided.'
            raise ValueError(err_msg)

        results = rest_client.s3.create_bucket(
            name=args.name, path=args.fs_path, create_path=args.create_fs_path
        )
        bucket = asdict(results)
        bucket.pop('anonymous_access_enabled')  # DEPRECATED
        print(pretty_json(bucket))


class DeleteBucketCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_delete_bucket'
    SYNOPSIS = 'Delete an S3 bucket'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--name', help='The name of the bucket to be deleted', required=True)
        parser.add_argument(
            '--delete-root-dir',
            action='store_true',
            help=(
                'If set to true, the operation will only succeed if the bucket root directory is'
                ' empty, and the caller has the necessary permissions to unlink it. Otherwise, the'
                ' directory need not be empty.'
            ),
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        rest_client.s3.delete_bucket(name=args.name, delete_root_dir=args.delete_root_dir)


class ModifyBucketCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_modify_bucket'
    SYNOPSIS = '[DEPRECATED] Use s3_set_bucket_policy to enable anonymous access.'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--name', help='The name of the bucket to be modified', required=True)
        anonymous_group = parser.add_mutually_exclusive_group()
        anonymous_group.add_argument(
            '--disable-anonymous-access',
            dest='anonymous_access_enabled',
            help='Disallows unsigned S3 requests; will be refused with 403 Forbidden.',
            action='store_false',
            default=None,
        )
        anonymous_group.add_argument(
            '--enable-anonymous-access',
            dest='anonymous_access_enabled',
            help='Allows unsigned S3 requests; will execute with GUEST privilege.',
            action='store_true',
            default=None,
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.anonymous_access_enabled is None:
            err_msg = (
                'At least one of the following arguments is required: [--disable-anonymous-access,'
                ' --enable-anonymous-access]'
            )
            raise ValueError(err_msg)

        patch = s3.BucketPatch(anonymous_access_enabled=args.anonymous_access_enabled)
        results = rest_client.s3.modify_bucket(name=args.name, patch=patch)
        print(pretty_json(asdict(results)))


class ListUploadsCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_list_uploads'
    SYNOPSIS = (
        'List in-progress S3 uploads. This includes user initiated multi-part uploads, and system'
        ' initiated uploads that are used in PutObject and CopyObject actions.'
    )

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--bucket', help='The bucket for which uploads should be listed.', required=True
        )
        parser.add_argument(
            '--starts-with',
            help='Only output uploads for keys that start with the given string',
            required=False,
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        starts_with = args.starts_with

        def append_asdict(tgt: List[Dict[str, Any]], src: Sequence[s3.UploadDescription]) -> None:
            for upload in src:
                if starts_with and not upload.key.startswith(starts_with):
                    continue
                tgt.append(asdict(upload))

        uploads: List[Dict[str, Any]] = []

        response = rest_client.s3.list_uploads(bucket=args.bucket)
        append_asdict(uploads, response.uploads)
        while response.paging.next is not None:
            response = rest_client.s3.list_uploads(
                bucket=args.bucket, start_after=response.paging.next
            )
            append_asdict(uploads, response.uploads)

        print(pretty_json({'uploads': uploads}))


class AbortUploadCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_abort_upload'
    SYNOPSIS = (
        'Aborts an in-progress S3 upload. This can be applied to both user initiated multi-part'
        ' uploads, and system initiated uploads that are used in PutObject and CopyObject actions.'
    )

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--bucket', help='The bucket in which the upload was initiated.', required=True
        )
        parser.add_argument('--upload-id', help='The upload to abort.', required=True)

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        rest_client.s3.abort_upload(bucket=args.bucket, upload_id=args.upload_id)


class SetPolicyCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_set_bucket_policy'
    SYNOPSIS = 'Upload the access policy json stored at --file to --bucket.'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--bucket', help="The target bucket who's policy will be set.", required=True
        )
        parser.add_argument(
            '--file',
            help=(
                'The policy file to upload. Use s3_get_bucket_policy --example to get a policy'
                ' template.'
            ),
            required=True,
        )
        parser.add_argument(
            '--allow-remove-self',
            help='Allow the policy set to remove the ability for this user to change the policy.',
            action='store_true',
            default=None,
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        policy_string = ''
        with open(args.file) as f:
            policy_string = f.read()
        policy_json = json.loads(policy_string)
        policy = s3.Policy.from_dict(policy_json)
        rest_client.s3.put_bucket_policy(
            bucket=args.bucket, policy=policy, allow_remove_self=args.allow_remove_self
        )
        print('Upload Complete.')


def apply_statement_modifications(statement: s3.PolicyStatement, args: argparse.Namespace) -> None:
    if args.sid is not None:
        statement.sid = args.sid
    if args.type is not None:
        statement.effect = args.type
    if args.new_principals is not None:
        statement.principals = args.new_principals.split(',')
    if args.new_actions is not None:
        statement.action = args.new_actions.split(',')


class ModifyPolicyCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_modify_bucket_policy'
    SYNOPSIS = 'Modify the access policy for --bucket.'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--bucket', help="The bucket who's policy will be modified.", required=True
        )
        parser.add_argument(
            '--allow-remove-self',
            help='Allow the policy set to remove the ability for this user to change the policy.',
            action='store_true',
            default=None,
        )
        subparsers = parser.add_subparsers(dest='command')
        delete = subparsers.add_parser('delete_statement', help='Delete a policy statement.')
        delete.add_argument(
            '--index', help='The index of the statment to delete.', type=int, required=True
        )

        append = subparsers.add_parser(
            'append_statement',
            help='Append a policy statement granting full access to the `local:admin`.',
        )
        append.add_argument('--type', help='Specify Allow or Deny.', required=True)
        append.add_argument('--sid', help='Specify the optional SID string.', required=False)
        append.add_argument(
            '--principals',
            help='Use the provided comma separated list of principals.',
            required=True,
        )
        append.add_argument(
            '--actions', help='Use the provided comma separated list of actions.', required=True
        )

        modify = subparsers.add_parser('modify_statement', help='Modify a policy statement.')
        modify.add_argument(
            '--index', help='The index of the statment to modify.', type=int, required=True
        )
        modify.add_argument(
            '--new-principals',
            help='Set the provided comma separated list of principals.',
            required=False,
        )
        modify.add_argument(
            '--new-actions',
            help='Set the provided comma separated list of actions.',
            required=False,
        )
        modify.add_argument('--type', help='Specify Allow or Deny.', required=False)
        modify.add_argument('--sid', help='Specify the optional SID string.', required=False)

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        policy = rest_client.s3.get_bucket_policy(bucket=args.bucket)
        if policy is None:
            policy = s3.Policy(id='Default', version=s3.POLICY_VERSION_2012, statements=[])

        if args.command == 'append_statement':
            principals = args.principals.split(',')
            action = args.actions.split(',')
            statement = s3.PolicyStatement(
                effect=args.type, sid=args.sid, principals=principals, action=action
            )
            policy.statements.append(statement)

        elif args.command == 'delete_statement':
            count = len(policy.statements)
            if args.index == 0 or count < args.index:
                raise ValueError(f'Index {args.index} not found in policy of length {count}.')
            policy.statements = [
                s for (i, s) in enumerate(policy.statements) if i + 1 != args.index
            ]

        elif args.command == 'modify_statement':
            count = len(policy.statements)
            if args.index == 0 or count < args.index:
                raise ValueError(f'Index {args.index} not found in policy of length {count}.')
            apply_statement_modifications(policy.statements[args.index - 1], args)

        else:
            raise ValueError(
                f'One of append_statement, delete_statement, or modify_statement must be provided.'
            )

        print('Uploading The Following Policy:')
        print('===============================\n')
        print(pretty_json(policy.to_dict()))

        rest_client.s3.put_bucket_policy(
            bucket=args.bucket, policy=policy, allow_remove_self=args.allow_remove_self
        )


class GetPolicyCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_get_bucket_policy'
    SYNOPSIS = 'Retrieve entries of the access policy json stored at `BUCKET`.'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--bucket',
            help='The target bucket for which the access policy will be retrieved',
            required=False,
        )
        parser.add_argument(
            '--example', help='Print an example Policy.', required=False, action='store_true'
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.example:
            if args.bucket is not None:
                raise ValueError('Bucket name is not allowed with --example.')

            statement1 = s3.PolicyStatement(
                effect='Allow',
                sid='EveryoneGet',
                principals=['Everyone'],
                action=[
                    's3:GetBucketPolicy',
                    's3:GetBucketAcl',
                    's3:GetBucketLocation',
                    's3:GetBucketNotification',
                    's3:GetBucketObjectLockConfiguration',
                    's3:GetBucketReplication',
                    's3:GetBucketVersioning',
                    's3:GetEncryptionConfiguration',
                    's3:GetLifecycleConfiguration',
                    's3:GetObject',
                    's3:GetObjectAcl',
                    's3:GetObjectAttributes',
                    's3:GetObjectTagging',
                ],
            )
            statement2 = s3.PolicyStatement(
                effect='Allow',
                sid='AuthenticatedPut',
                principals=['Authenticated Users'],
                action=[
                    's3:AbortMultipartUpload',
                    's3:DeleteBucket',
                    's3:DeleteObject',
                    's3:DeleteObjectTagging',
                    's3:GetBucketPolicy',
                    's3:ListBucket',
                    's3:ListBucketMultipartUploads',
                    's3:ListMultipartUploadParts',
                    's3:PutObject',
                    's3:PutObjectTagging',
                ],
            )
            statement3 = s3.PolicyStatement(
                effect='Allow',
                sid='AdminModifyPolicy',
                principals=['local:Admin'],
                action=['s3:PutBucketPolicy', 's3:DeleteBucketPolicy', 's3:*'],
            )
            example_policy = s3.Policy(
                id='DefaultPolicy',
                version=s3.POLICY_VERSION_2012,
                statements=[statement1, statement2, statement3],
            )
            pretty_policy = pretty_json(example_policy.to_dict())
            print(pretty_policy)
        else:
            if args.bucket is None:
                raise ValueError('A bucket name must be specified.')

            policy = rest_client.s3.get_bucket_policy(args.bucket)
            if policy is None:
                print('{}')
            else:
                pretty_str = pretty_json(policy.to_dict())
                print(pretty_str)


class DeletePolicyCommand(qumulo.lib.opts.Subcommand):
    NAME = 's3_delete_bucket_policy'
    SYNOPSIS = 'Remove the access policy stored at `BUCKET`.'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--bucket',
            help='The target bucket for which the access policy will be removed.',
            required=True,
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        rest_client.s3.delete_bucket_policy(args.bucket)
