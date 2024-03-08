import paramiko
from progressbar import ProgressBar, Percentage, Bar, FileTransferSpeed, ETA
import socket
import time
from datetime import datetime
import stat
import base64
import os
import io
import sys

output_buffer = io.StringIO()
error_buffer = io.StringIO()
original_stdout = sys.stdout
original_stderr = sys.stderr


def lock_output(lock):
    if lock is True:
        sys.stdout = output_buffer
        sys.stderr = error_buffer
    else:
        sys.stdout = original_stdout
        sys.stderr = original_stderr

def test_ping(host, port):
    try:
        start_time = time.time()
        with socket.create_connection((host, port), timeout=3) as connection:
            pass
        end_time = time.time()
        rtt = (end_time - start_time) * 1000
        return rtt
    except Exception as e:
        print("Error: ", str(e))
        return None

def is_remote_directory(remote_path, sftp):
    try:
        remote_attributes = sftp.stat(remote_path)
        return stat.S_ISDIR(remote_attributes.st_mode)
    except Exception as e:
        print('Failed to determine directory:', str(e))
        return False


def is_remote_reg(remote_path, sftp):
    try:
        remote_attributes = sftp.stat(remote_path)
        return stat.S_ISREG(remote_attributes.st_mode)
    except Exception as e:
        print('Failed to determine reg file:', str(e))
        return False


def is_sftp_supported(host, port, user, passwd):
    is_sftp = True
    lock_output(True)
    transport = paramiko.Transport((host, port))
    try:
        transport.connect(username=user, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        if is_remote_reg('.sophgo', sftp) is False:
            is_sftp = False
        sftp.close()
        transport.close()
        return is_sftp
    except Exception as e:
        is_sftp = False
    finally:
        try:
            transport.close()
        except Exception as e:
            pass
        lock_output(False)
        return is_sftp


def format_file_size(file_size_bytes):
    if file_size_bytes < 1024:
        return "{} B".format(file_size_bytes)
    elif file_size_bytes < 1024 ** 2:
        return "{:.2f} KB".format(file_size_bytes / 1024)
    elif file_size_bytes < 1024 ** 3:
        return "{:.2f} MB".format(file_size_bytes / (1024 ** 2))
    elif file_size_bytes < 1024 ** 4:
        return "{:.2f} GB".format(file_size_bytes / (1024 ** 3))
    else:
        return "{:.2f} TB".format(file_size_bytes / (1024 ** 4))

def get_server_info(username):
    server_info = {'hostname':None,'port':None,'username':None,'password':None}
    if username.startswith('sophgo'):
        # HDK account
        server_info['hostname'] = "219.142.246.77"
        server_info['port'] = 18822
        server_info['username'] = username
    else:
        server_list = [
            ("172.26.175.10", 32022, 'oponIn', 'oponIn', None),
            ("172.26.13.58", 12022, 'oponIn', 'oponIn', 30),
            ("172.26.166.66", 22022, 'oponIn', 'oponIn', None),
            ("106.37.111.18", 32022, 'open', 'open', None),
        ]
        
        for index, server in enumerate(server_list):
            ip, port_to_check, user, passwd, ping_limit = server
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((ip, port_to_check))
                if result == 0:
                    if is_sftp_supported(ip, port_to_check, user, passwd) is True:
                        ping_ret = test_ping(ip, port_to_check)
                        if ping_limit is not None:
                            if (ping_ret is None) or (ping_ret >= ping_limit):
                                continue
                        print('using connection scheme {}, ping {:.2f} ms'.format(
                            index, ping_ret))
                        server_info['hostname'] = ip
                        server_info['port'] = port_to_check
                        server_info['username'] = user
                        server_info['password'] = passwd
                        break
            except Exception as e:
                print('An error occurred in get available policies:', str(e))
            finally:
                try:
                    sock.close()
                    pass
                except Exception as e:
                    pass

    return server_info

def download_file_from_sophon_sftp(remote_path, local_path):
    server_info = get_server_info('open')
    
    if server_info['hostname'] is None or server_info['port'] is None \
        or server_info['username'] is None or server_info['password'] is None:
        print("No available servers found.")
        return False
    try:
        transport = paramiko.Transport((server_info['hostname'], server_info['port']))
        transport.connect(username=server_info['username'], password=server_info['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)

        if is_remote_directory(remote_path, sftp) is True:
            print("cannot find aim")
            return False
        local_path = os.path.normpath(local_path)
        local_item = os.path.basename(remote_path)
        if os.path.isdir(local_path) is True:
            local_path = os.path.join(local_path, local_item)
        directory = os.path.dirname(local_path)
        if os.path.isdir(directory) is False:
            os.makedirs(directory)
        remote_file_size = sftp.stat(remote_path).st_size
        print('download file from', remote_path, '->', local_path, ', size:',
              format_file_size(remote_file_size), '...')
        widgets = [ETA(), ' | ', Percentage(), Bar(), FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=remote_file_size).start()

        def progress_callback(x, y):
            pbar.update(x)
        sftp.get(remote_path, local_path, callback=progress_callback)
        pbar.finish()
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print('An error occurred in get file:', str(e))
        return False


def upload_file_to_sophon_sftp(remote_path, local_path):
    server_list = [
        ("106.37.111.18", 32022, 'customerUploadAccount', '1QQHJONFflnI2BLsxUvA'),
        ("172.26.175.10", 32022, 'customerUploadAccount', '1QQHJONFflnI2BLsxUvA'),
    ]

    hostname = None
    port = None
    username = None
    password = None

    for index, server in enumerate(server_list):
        ip, port_to_check, user, passwd = server
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port_to_check))
            if result == 0:
                print('using connection scheme {}'.format(index))
                hostname = ip
                port = port_to_check
                username = user
                password = passwd
                break
        except Exception as e:
            print('An error occurred in get available policies:', str(e))
        finally:
            sock.close()

    if hostname is None or port is None or username is None or password is None:
        print("No available servers found.")
        return False
    try:
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        local_path = os.path.normpath(local_path)
        if not os.path.isfile(local_path):
            print(local_path, 'is not a file.')
            exit(-1)
        remote_file_size = os.path.getsize(local_path)
        print('up file from', local_path, '-> open@sophgo.com:', remote_path, 'size:',
              format_file_size(remote_file_size), '...')
        widgets = [ETA(), ' | ', Percentage(), Bar(), FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=remote_file_size).start()

        def progress_callback(x, y):
            pbar.update(x)
        decoded_bytes = base64.b64decode(remote_path)
        decoded_string = decoded_bytes.decode('utf-8')
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        remote_path = os.path.join(
            decoded_string, current_time + '_' + os.path.basename(local_path))
        sftp.put(local_path, remote_path,
                 callback=progress_callback, confirm=False)
        pbar.finish()
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print('An error occurred in up file:', str(e))
        return False

def sftp_login(username):
    print('Login sftp server by user: ', username)
    server_info = get_server_info(username)
    cmdstr = 'sftp -P '+ str(server_info['port'])+' '+ username +'@'+server_info['hostname']
    # print(cmdstr)
    os.system(cmdstr)
    return True