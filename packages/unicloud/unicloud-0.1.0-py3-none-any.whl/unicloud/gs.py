"""gsutils."""
import os

from google.cloud import storage


def is_gs_uri(uri: str) -> bool:
    """Check whether the URI points to a Google Cloud Storage object."""
    return uri.startswith("gs://")


def parse_gs_uri(uri):
    """Parse the Google Cloud Storage URI into bucket and file name."""
    rel_path = uri.removeprefix("gs://")
    bucket_id = rel_path.split("/")[0]
    file_name = rel_path.removeprefix(bucket_id)[1:]
    return bucket_id, file_name


def file_exists(uri: str, gcp_client: storage.Client) -> bool:
    """Check whether a file exists locally or in a GCP bucket."""
    if is_gs_uri(uri):
        bucket_id, file_name = parse_gs_uri(uri)
        bucket = gcp_client.get_bucket(bucket_id)
        return bucket.get_blob(file_name) is not None
    else:
        return os.path.exists(uri)


def open_file(uri: str, mode: str, gcp_client: storage.Client):
    """Open a local or remote file."""
    if is_gs_uri(uri):
        bucket_id, file_name = parse_gs_uri(uri)
        bucket = gcp_client.get_bucket(bucket_id)
        blob = bucket.blob(file_name)
        outfile = blob.open(mode)
    else:
        outfile = open(uri, mode)
    return outfile
