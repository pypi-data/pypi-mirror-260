from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from loguru import logger
from ..utils import config


async def write(data, bucket=None):
    try:
        if bucket is None:
            bucket = config.homesolar_config['INFLUXDB']['default_bucket']

        async with InfluxDBClientAsync(
                url=f"{config.homesolar_config['INFLUXDB']['host']}:{config.homesolar_config['INFLUXDB']['port']}",
                token=config.homesolar_config['INFLUXDB']['token'],
                org=config.homesolar_config['INFLUXDB']['org']) as client:
            await client.ping()

            write_api = client.write_api()
            success = await write_api.write(bucket=bucket, record=data)
            if success:
                logger.debug(f"Data saved successfully!")
            else:
                logger.error(f"Something went wrong, fail to saved the data!")
    except Exception as e:
        logger.exception(f"Data not saved! [{e}]")


async def query(flux, url=None, token=None, org=None, timeout=None):
    if url is None:
        url = f"{config.homesolar_config['INFLUXDB']['host']}:{config.homesolar_config['INFLUXDB']['port']}"
    if token is None:
        token = config.homesolar_config['INFLUXDB']['token']
    if org is None:
        org = config.homesolar_config['INFLUXDB']['org']
    if timeout is None:
        timeout = config.homesolar_config['INFLUXDB']['read_timeout']

    async with InfluxDBClientAsync(
            url=url,
            token=token,
            org=org,
            timeout=timeout
    ) as client:
        await client.ping()

        query_api = client.query_api()
        result = await query_api.query(flux)
        return result
