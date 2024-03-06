import socketio
import argparse
import time
import util
import os
import click

parser = argparse.ArgumentParser(description='Python Socket.IO Client for Workers')
parser.add_argument('--worker_id', type=str, default=os.environ.get("CLUSTROAI_WORKER_ID", None),
                    help='the ID of the worker')
parser.add_argument('--server_url', type=str, default='http://api.clustro.ai:5000',
                    help='backend server url')
parser.add_argument('--api_key', type=str, default=os.environ.get("CLUSTROAI_API_KEY", None),
                    help='CLUSTROAI_API_KEY')
parser.add_argument('--db_host', type=str, default='localhost',
                    help='database db_host')
parser.add_argument('--db_name', type=str, default='',
                    help='database db_name')
parser.add_argument('--db_user', type=str, default='',
                    help='database db_user')
parser.add_argument('--db_password', type=str, default='',
                    help='database db_password')
parser.add_argument('--db_port', type=int, default=5432,
                    help='database db_port')
args = parser.parse_args()

if args.worker_id is None:
    click.echo("Error: --worker_id is required or CLUSTROAI_WORKER_ID should be set in environment variables.")
    os._exit(1)

api_key = args.api_key
if not api_key:
    click.echo("Error: CLUSTROAI_API_KEY should be set in environment variables.")
    os._exit(1)

worker_id = args.worker_id
server_url = args.server_url
db_host = args.db_host
db_name = args.db_name
db_user = args.db_user
db_password = args.db_password
db_port = args.db_port

sio = socketio.Client()

headers = {'Content-Type': 'application/json'}


@sio.event
def connect():
    click.echo(f'I am connected to the server! With namespace: {sio.namespaces}')


@sio.on('request_worker_id')
def on_request_worker_id(data):
    click.echo(data['data'])  # prints "Please provide worker id."
    worker_sys_info = util.get_system_info()
    while not sio.namespaces:
        click.echo('Waiting for namespace in other thread to be ready...')
        time.sleep(0.1)

    sio.emit('provide_worker_id', {'id': worker_id, 'gpu_name': worker_sys_info['gpu_name'],
                                   'api_key': api_key,
                                   'gpu_memory_gb': worker_sys_info['gpu_memory_gb'],
                                   'free_disk_gb': worker_sys_info['free_disk_gb'], 'ip': worker_sys_info['ip']})


@sio.on('worker_session_established')
def on_worker_session_established(data):
    click.echo(data)
    sio.emit('start')


@sio.on('prepare_model')
def on_prepare_model(data):
    click.echo(f"LOADING_MODEL - Preparing model... {data}")
    sio.emit('finish_model_deployment', {'model_code_repo_url': data['model_code_repo_url'], 'total_time_spent': 0})


@sio.on('message')
def on_message(data):
    click.echo(data)


@sio.on('execute_task')
def on_execute_task(data):
    task_id = str(data['task_id'])
    sql_input: str = str(data['input']).strip()
    click.echo(f'working on task {task_id} {sql_input}...')
    conn = util.get_conn(db_host, db_name, db_user, db_password, db_port)
    cursor = conn.cursor()
    try:
        if sql_input.startswith("select") or sql_input.startswith("SELECT"):
            cursor.execute(sql_input)
            result = cursor.fetchall()
        else:
            result = cursor.execute(sql_input)
            conn.commit()
        click.echo(f"{task_id} result {result}")
        sio.emit('finish_task',
                 {'task_id': task_id, 'result': result, 'worker_id': worker_id, 'error': ''})
    except Exception as e:
        sio.emit('finish_task',
                 {'task_id': task_id, 'result': "", 'worker_id': worker_id, 'error': str(e)})
        os._exit(1)
    finally:
        cursor.close()
        conn.close()


@sio.on('error')
def on_error(data):
    click.echo(data)
    sio.disconnect()


if __name__ == '__main__':
    sio.connect(server_url)
