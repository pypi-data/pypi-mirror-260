import argparse

from metaloop.client import MDS


def parse_args():
    parser = argparse.ArgumentParser(description='import download data to metaloop')
    parser.add_argument('--api_addr', required=True, help='address of metaloop API')
    parser.add_argument('--user_token', required=True, help='user token used to access metaloop API')
    parser.add_argument('--dataset_id', required=True, help='ID of dataset for importing')
    parser.add_argument('--file_path', required=True, help='local path of data to be uploaded')
    parser.add_argument('--import_type', default='none', help='import type of local data, includes "none", "evalmodels", "pre_annotation", "standard", "multiform".')
    parser.add_argument('--storage_type', default='local', help='Cloud storage type of imported data, includes "local", "cos".')
    return parser.parse_args()


def main(args):
    mds_client = MDS(args.user_token, args.api_addr)
    dataset = mds_client.get_dataset_by_id(args.dataset_id)
    dataset.import_data(args.file_path, args.import_type, args.storage_type)


if __name__ == '__main__':
    args = parse_args()
    main(args)
