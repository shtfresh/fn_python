import io
import json
import logging
import oci
from fdk import response


def handler(ctx, data: io.BytesIO=None):

    name = "World"


    try:
        logging.info("----------------------xxxxxxxxxxxxxxxxxxx--------------")
        #logging.info("data:"+data.getvalue())
        body = json.loads(data.getvalue())

        # logging.info(type(body))
        # for key, value in body.items():
        #      logging.info(key+":"+value)
        data=body.get("data")
        logging.info(type(data))
        #  for key, value in data.items():
        #       logging.info(key+":"+value)

        resourceId = data.get("resourceId")

        logging.info("--------resourceId:"+resourceId+":--------------")
    except (Exception, ValueError) as ex:
        logging.info(str(ex))

    source_backup_id = resourceId
    destination_region = "eu-frankfurt-1"
    source_config = oci.config.from_file("/function/key/config","tao-oci-profile")
    destination_config = source_config.copy()
    destination_config["region"] = destination_region
    source_blockstorage_client = oci.core.BlockstorageClient(source_config)
    destination_blockstorage_client = oci.core.BlockstorageClient(destination_config)
    # load config and create clients (one for the source region and one for the destination region).


    # print('Copying backup with ID {} from {} to {} using new display name: {} and kms key id: {} \n'.format(
    #     source_backup_id, source_config["region"], destination_region))
    result = source_blockstorage_client.copy_volume_backup(
        source_backup_id,
        oci.core.models.CopyVolumeBackupDetails(
            destination_region=destination_region
            # display_name=display_name,
            # kms_key_id=kms_key_id
        )
    )

    print('Copy backup response status: {}, copied backup: {}\n'.format(result.status, result.data))
    print('Waiting for the copied backup to be in available state...')

    # query the destination region for the copied' backup's status and wait for it to be available.

    copied_backup = oci.wait_until(
        destination_blockstorage_client,
        destination_blockstorage_client.get_volume_backup(result.data.id),
        'lifecycle_state',
        'AVAILABLE'
    ).data
    print('Backup successfully copied: {}'.format(copied_backup))
    print('Example script done')


    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Hello {0}".format(name)}),
        headers={"Content-Type": "application/json"}
    )

