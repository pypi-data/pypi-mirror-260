"""Bucket related functions."""
import io
import shutil
from typing import List, Union

import pandas as pd
from google.cloud import storage
from loguru import logger

from unicloud.gs import open_file


def get_bucket(
    client: storage.client.Client, bucket: str, project_id: str
) -> storage.bucket.Bucket:
    """get_bucket.

        get_bucket returns the bucket object

    Parameters
    ----------
    client : [google.cloud.storage.client.Client]
        google client object
    bucket : [str]
        bucket id
    project_id : [str]
        project name

    Returns
    -------
    storage.bucket.Bucket

    Examples
    --------
    >>> from unicloud.authenticate import create_client
    >>> your_service_key = "/service-key-gee-data-access.json"
    >>> client = create_client(your_service_key, project_id)
    >>> bucket = "-datasets"
    >>> project_id = "gee-data-access"
    >>> bucket_usr = get_bucket(client, bucket, project_id)
    """
    return storage.Bucket(client, bucket, user_project=project_id)


def get_bucket_list(client_usr: storage.client.Client) -> List[str]:
    """get_bucket_list.

        get_bucket_list returns a list of all the content of a bucket

    Parameters
    ----------
    client_usr: [google.cloud.storage.client.Client]
        google client object

    Returns
    -------
    bucket_list: [list]
        list of the names of the files exist in the bucket as a string

    Examples
    --------
    >>> from google.cloud import storage
    >>> project_id = "gee-data-access"
    >>> credentials = ""
    >>> client = storage.Client(project=project_id, credentials=credentials)
    >>> bucket_content = get_bucket_list(client)
    """
    buckets = list(client_usr.list_buckets())
    bucket_list = []
    for bucketi in buckets:
        # logger.debugprint(bucket.id)
        bucket_list.append(bucketi.id)
    return bucket_list


def get_bucket_contents(
    client_usr: storage.client.Client, bucket_id: str, project_id: str
) -> List[str]:
    """get_bucket_contents.

        get_bucket_contents returns the names of the buckets exists inside a project

    Parameters
    ----------
    client_usr: []

    bucket_id : [str]
        bucket id
    project_id: [str]
        project id
    Returns
    -------
    content : [list]
        list of the names of the buckets exist in the project as a string

    Examples
    --------
        >>> from google.cloud import storage
        >>> client = storage.Client(project=project_id, credentials=credentials)
        >>> bucket_content = get_bucket_list(client)
    """
    bucket_usr = storage.Bucket(client_usr, bucket_id, user_project=project_id)
    all_blobs = list(client_usr.list_blobs(bucket_usr))
    content = []
    for blobi in all_blobs:
        content.append(blobi.path.split("/")[-1])
    return content


def get_file_from_bucket(
    file: str, usr_bucket: storage.bucket.Bucket
) -> storage.blob.Blob:
    """get_file_from_bucket.

        get_file_from_bucket retrives a file from a given bucket object as a blob object

    Parameters
    ----------
    file: [str]
        file name you want to retrive from the bucket
    usr_bucket: [google.cloud.storage.bucket.Bucket]
        the bucket object

    Returns
    -------
    blob : [google.cloud.storage.blob.Blob]
        binary large object
    """
    # get the file from the bucket
    blob_usr = usr_bucket.get_blob(file)
    # logger.debug(blob.download_as_bytes())
    if blob_usr is None:
        raise ValueError(f"The {file} does not exist in the {usr_bucket.id} bucket")
    else:
        logger.info(
            f"The {file} is retrived successfully from the {usr_bucket.id} bucket"
        )

    return blob_usr


def glob(
    search_criteria: Union[str, List[str]], content: list, function: str = "startswith"
) -> List[str]:
    """gcs_filenames.

    Parameters
    ----------
    search_criteria: [Union[str, List[str]]]
        a string that exists in the name, or a list of separate strings that each one of them exists in a separate
        location in the name.
    content: [list]
        content of the gcp bucket.
    function:
        function to be used to search for the file in the bucket content list
        default si "startswith", "__contains__"
        >>> function = "startswith".

    Returns
    -------
    list
    """
    # in case there are spaces in the search criteria
    if isinstance(search_criteria, str) and len(search_criteria.split(" ")) > 1:
        prefix_parts = search_criteria.split(" ")
        search_criteria = prefix_parts[0]
        for i in range(1, len(prefix_parts)):
            search_criteria = search_criteria + "%20" + prefix_parts[i]

    fnames = []
    for i in range(len(content)):
        whole_name = content[i]
        # without the .tif at the end
        # if whole_name.__contains__("."):
        name_without_tif = whole_name.split(".")[0]
        # else:
        #     name_without_tif = whole_name
        # if the search_criteria is a string
        if isinstance(search_criteria, str):
            # if you changed the search criteria variable name you have to change it in the next line also and it
            # has to stay as a string for the compile and eval function to work.
            if eval(
                compile(
                    f"'{name_without_tif}'.{function}(search_criteria)",
                    "<string>",
                    "eval",
                )
            ):
                fnames.append(whole_name)
        elif isinstance(search_criteria, list):
            if all(x in whole_name for x in search_criteria):
                fnames.append(whole_name)

    fnames = [i.replace("%2F", "/") for i in fnames]
    fnames = [i.replace("%20", " ") for i in fnames]
    return fnames


def get_file_names(
    location_id: str = "",
    search_criteria: str = "",
    date: bool = False,
    content: list = [],
    function: str = "__contains__",
):
    """get_file_names.

        get_file_names

    Parameters
    ----------
    location_id : [str]
        if there is a location related word, inserted at the beginning of the file name.
    search_criteria : [str]
        the dataset id
    date : [bool]
        if there is a time stamp in the file name.
    content : [list]
        list containing the file names in GCS
    function : [str]
        function to be used to search for the files

    Returns
    -------
    list[str]
        list of file names
    """
    if location_id == "":
        original_name = search_criteria
    else:
        print(f"polygon -  {location_id}")
        original_name = f"{location_id}_{search_criteria}"

    name_prefix = original_name

    "the name_prefix if unique for each group of data"
    # name_prefix = f"{original_name}"

    # name_prefix = f"{original_name}%2F{dataset}%2F{original_name}_"
    # get the old files names based on the unique name_prefix
    old_fnames = glob(name_prefix, content, function=function)
    return old_fnames


def check_file_in_bucket(
    file: str,
    client: storage.client.Client,
    bucket_id: str,
    option: int = 2,
    project_id: str = "",
    search_function: str = "startswith",
) -> bool:
    """check_file_in_bucket.

        check_file_in_bucket checks if a fiven file exists inside a bucket or not

    Parameters
    ----------
    file: [str]
        file name in the form of root2/root2/aoi-name_dataset-name_YYYY_MM_DD.tif
        >>> file = "Montana_ls7_ndvi_2000_08_20.tif"
    client: [storage.client.Client]
        storage client you get when initializing the gcs
        >>> from unicloud.authenticate import create_client
        >>> your_service_key = "<you-service-account>"
        >>> client = create_client(your_service_key, project_id)
    bucket_id: [str]
        bucket id
        >>> bucket_id = "testing_repos"
    option: [int]
        - option = 1 :
                    if you want give the whole name of the file, then the function
                     will try to retrieve it from the bucket
        - option = 2 :
                    if you want to search with the file name prefix only and not the full
                    name, and also gives you criteria to search for the name prefix
    project_id: [str]
        project id, needed only incase of option=2
        >>> project_id = "gee-data-access"
    search_function: [str]
        the way to search for the file name prefix in the string, i.e "startswith"
        or "__contains__"
        >>> search_function = "startswith"
    Returns
    -------
        [True/False] whether a file exists in the bucket or not.
    """
    if option == 1:
        bucket = client.get_bucket(bucket_id)
        try:
            get_file_from_bucket(file, bucket)
            exist = True
        except ValueError:
            exist = False
    else:
        content = get_bucket_contents(client, bucket_id, project_id)
        old_fnames: List = glob(file, content, function=search_function)
        if len(old_fnames) >= 1:
            exist = True
        else:
            exist = False
    return exist


def upload_from_disk_to_gcs(
    file: str, folders: List[str], bucket: storage.bucket.Bucket
):
    """upload_from_disk_to_gcp.

        upload data from disk to gcs

    Parameters
    ----------
    file: [str]
        the file path on disk.
    folders: [list]
        rootdirectories in gcp, if these folders does not exit it will be created,
        the order of the folders is important,
        ex folders=[root1, root2]
        root1/
            root2
    bucket: [storage.bucket.Bucket]
        bucket object
        ex, bucket = storage.Bucket(bucket_name)

    Returns
    -------
    file will be uplaoded to the given bucket object
    """
    roots = [i + "/" for i in folders]
    rpath = ""
    for i in range(len(roots)):
        rpath += roots[i]

    fname = file.split("/")[-1]
    blob2 = bucket.blob(rpath + fname)

    blob2.upload_from_filename(filename=file)
    logger.info(f"The file is uploaded to the following path {rpath + fname}")


def download_from_gcs_to_disk(
    file: str, folders: List[str], bucket: storage.bucket.Bucket
):
    """download_from_gcs_to_disk.

        upload data from disk to gcs

    Parameters
    ----------
    file: [str]
        the file path on disk.
    folders: [list]
        root directories in gcp, if these folders does not exit it will be created,
        the order of the folders is important,
        ex folders=[root1, root2]
        root1/
            root2
    bucket: [storage.bucket.Bucket]
        bucket object
        ex, bucket = storage.Bucket(bucket_name)

    Returns
    -------
    file will be uplaoded to the given bucket object
    """
    # https://stackoverflow.com/questions/42555142/downloading-a-file-from-google-cloud-storage-inside-a-folder
    # TODO: not finished yet
    roots = [i + "/" for i in folders]
    rpath = ""
    for i in range(len(roots)):
        rpath += roots[i]

    fname = file.split("/")[-1]
    blob2 = bucket.blob(rpath + fname)

    blob2.upload_from_filename(filename=file)
    logger.info(f"The file is uploaded to the following path {rpath + fname}")


def move_files_to_folder(
    old_name: List[str],
    new_name: List[str],
    bucket_id: str,
    client_usr: storage.client.Client,
):
    """move_files_to_folder.

        move_files_to_folder renames/moves file in the same bucket into new names( inside folders)

    Parameters
    ----------
    old_name : list[str]
        list of the names of the files you want to move
    new_name : list[str]
        new file names including the whole path folder, if have to contain slash at the end ex ("fildername/")
    bucket_id: [str]
        bucket id
    client_usr: [client.client]
        client object from the google cloud storage module
        ex client = storage.Client(project=project_id, credentials=credentials)

    Returns
    -------
    True :[boolean]
        if the function finished the work successfully it will retun True

    Examples
    --------
    >>> old_name = ["modis_veg_20000101.tif"]
    >>> new_name = ["modis_veg_2000_01_01.tif"]
    >>> bucket_id = "testing-repos"
    >>> move_files_to_folder(old_name, new_name, bucket_id, client_usr)
    """
    # get the bucket you want
    usr_bucket = client_usr.get_bucket(bucket_id)
    # folder_name = "folder1/"
    for i in range(len(old_name)):
        logger.info(f"{i} / {len(old_name)} - {old_name[i]}")
        # create a blob for the file you want (file from the bucket)
        blobi = get_file_from_bucket(old_name[i], usr_bucket)
        # new_name = folder_name + files[i]
        usr_bucket.rename_blob(blobi, new_name[i])

    return True


def move_to_other_bucket(
    old_name: List[str],
    new_name: List[str],
    source_bucket_id: str,
    destination_bucket_id: str,
    client_usr: storage.client.Client,
    delete_old: bool = False,
):
    """move_to_other_bucket.

        the function does not check if a file with the same name already exists, but overwrite the old file if
        exists.
        # optimize: check if the file exists first in the destnation directory and warn the user

    Parameters
    ----------
    old_name : list[str]
        list of the names of the files you want to move
        >>> old_name = ["image_to_other_bucket.tif"]
    new_name : list[str]
        new file names including the whole path folder, if have to contain slash at the end ex ("fildername/")
        >>> new_name = ["root1/root2/image.tif"]
    source_bucket_id: [str]
        source bucket id
        >>> source_bucket_id = "testing_repos"
    destination_bucket_id: [str]
        destination bucket id
        >>> destination_bucket_id = "-datasets"
    client_usr: [client.client]
        client object from the google cloud storage module
        >>> from unicloud.authenticate import create_client
        >>> project_id = "gee-data-access"
        >>> your_service_key = <your_service_key>
        >>> client = create_client(your_service_key, project=project_id)
    delete_old : [bool]
        True if you want to delete the old files, True otherwise.
        >>> delete_old = False
    Returns
    -------
    None

    Examples
    --------
    >>> source_bucket_id = "testing_repos"
    >>> destination_bucket_id = "-datasets"
    >>> old_name = ["image_to_other_bucket.tif"]
    >>> client_usr = client
    >>> new_name = ["root3/image.tif"]
    """
    src_bucket = client_usr.get_bucket(source_bucket_id)
    dst_bucket = client_usr.get_bucket(destination_bucket_id)

    for i in range(len(old_name)):
        logger.info(f"{i} / {len(old_name)} - {old_name[i]}")
        # create a blob for the file you want (file from the bucket)
        src_blob = get_file_from_bucket(old_name[i], src_bucket)
        # new_name = folder_name + files[i]
        # src_bucket.rename_blob(source_blob, new_name[i])
        # copy to new destination
        src_bucket.copy_blob(src_blob, dst_bucket, new_name[i])
        if delete_old:
            # delete the old file
            src_blob.delete()


# TODO : create a function to rename a bucket


def delete_file(
    prefix: str,
    client: storage.client.Client,
    bucket: str,
    project_id: str,
    function: str = "startswith",
):
    """delete_file.

        delete_file deletes the files that their names resut from applying the function
        given to the function parameter

    Parameters
    ----------
    prefix : [str]
        prefix is any string that is included in the file name, it can be in the beginning, in the middle
        or in the end.
    client : [google.cloud.storage.client.Client]
        google client object
    bucket : [str]
        bucket id
    project_id : [str]
        project name
    function: [str]
        function to filter the files in the buckets. Default is "startswith"

    Returns
    -------
    None

    Examples
    --------
    >>> bucket = "-datasets"
    >>> prefix = "859932"
    >>> delete_file(prefix, client, bucket, project_id, function ="startswith")
    """
    contents = get_bucket_contents(client, bucket, project_id)
    files = glob(prefix, contents, function=function)
    bucket_usr = get_bucket(client, bucket, project_id)

    for i in range(len(files)):
        blob = get_file_from_bucket(files[i], bucket_usr)
        blob.delete()
        logger.info(f"File {files[i]} has been deleted")


def dataframe_to_file(df: pd.DataFrame, uri: str, gcp_client: storage.Client):
    """Store the DataFrame to a local or remote file."""
    buffer = io.BytesIO()
    df.to_csv(
        buffer,
        index=False,
        compression={
            "method": "gzip",
            "mtime": 1,  # For reproducibility: do not store timestamp.
        }
        if uri.endswith(".gz")
        else None,
    )
    buffer.seek(0)

    outfile = open_file(uri, mode="wb", gcp_client=gcp_client)
    shutil.copyfileobj(buffer, outfile)
    outfile.close()


def dataframe_from_file(uri: str, gcp_client: storage.Client):
    """Read a DataFrame from a local or remote file."""
    infile = open_file(uri, mode="rb", gcp_client=gcp_client)
    df = pd.read_csv(
        infile, index_col=False, compression="gzip" if uri.endswith(".gz") else None
    )
    infile.close()
    return df
