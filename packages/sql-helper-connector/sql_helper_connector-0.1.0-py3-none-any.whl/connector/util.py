import pg8000
import pymysql
import requests
import subprocess
import os
import click


def get_system_info():
    # Get GPU information using nvidia-smi
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'],
                                stdout=subprocess.PIPE)
        gpu_info = result.stdout.decode('utf-8').strip().split('\n')[0]
        gpu_name, gpu_memory = gpu_info.split(', ')
    except Exception as e:
        gpu_name, gpu_memory = "N/A", "N/A"

    if gpu_memory == "N/A":
        gpu_memory_gb = 0
    else:
        gpu_memory_gb = int(int(gpu_memory) / 1024)

    # Get free disk space
    st = os.statvfs('/')
    free_disk_gb = int(st.f_bavail * st.f_frsize / (1024 ** 3))

    # Get external IP using requests
    try:
        response = requests.get('http://ifconfig.me', timeout=10)
        response.raise_for_status()  # Raises an exception for HTTP errors
        ip = response.text.strip()
    except Exception as e:
        ip = "N/A"

    return {"gpu_name": gpu_name, "gpu_memory_gb": gpu_memory_gb, "free_disk_gb": free_disk_gb, "ip": ip}


def get_conn(db_host, db_name, db_user, db_password, db_port):
    # try to connect database
    conn = None
    try:
        conn = pg8000.connect(host=db_host, database=db_name, user=db_user, password=db_password,
                              port=db_port)
        return conn
    except Exception as e:
        click.echo(f"postgres server connection error {str(e)}")
        click.echo("try connect mysql server")
        try:
            conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=db_port)
            return conn
        except Exception:
            click.echo(f"mysql connection error {str(e)}")
    return conn
