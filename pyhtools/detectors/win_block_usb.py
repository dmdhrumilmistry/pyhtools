from subprocess import PIPE, run
from shlex import split
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


def run_cmd(cmd:str, succ_msg:str, err_msg:str, succ_rcode:int=0) -> tuple:
    '''Run shell commands
    
    Args:
        cmd (str): command to be executed
        succ_msg (str): message to be logged if cmd is executed successfully
        err_msg (str): message to be logged if cmd is interrupted
        succ_rcode (int): return status code after successfully executing code

    Returns:
        tuple: returns executed command output/error along with status code
    '''
    result = run(split(cmd), stderr=PIPE, stdout=PIPE)
    res = result.stdout.decode('utf-8') or result.stderr.decode('utf-8')
    rcode = result.returncode

    if rcode == succ_rcode:
        logger.info(succ_msg)
    else:
        logger.error(err_msg)

    return (res, rcode)


def block_root_hubs():
    '''Blocks USB root hubs on windows machine
    
    Args:
        None
    
    Returns:
        None
    '''
    res, rcode = run_cmd(
        cmd='pnputil /enum-devices /class "USB"',
        succ_msg='Fetched USB devices ids list',
        err_msg='Error occurred while device ids list',
    )

    if rcode == 0:
        for line in res.splitlines():
            if "USB\ROOT_HUB" in line:
                device_id = line.split(':')[-1].strip()
                res, rcode = run_cmd(
                    cmd=f'pnputil /disable-device "{device_id}"',
                    succ_msg=f'USB {device_id} blocked',
                    err_msg=f'Cannot disable USB {device_id}'
                )

if __name__ == '__main__':
    block_root_hubs()