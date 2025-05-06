import os
from threading import BoundedSemaphore
from uuid import uuid4
from time import sleep
class Threading_params:
	MAX_THREADS = 140
	thread_limiter = BoundedSemaphore(MAX_THREADS)
class Villain:
	version = "2.2.1"
class Core_Server_Settings:
	bind_address = '0.0.0.0'
	bind_port = 6501	
	ping_siblings_sleep_time = 4
	timeout_for_command_output = 30
	insecure = False
class Hoaxshell_Settings:
	bind_address = '0.0.0.0'
	bind_port = 8080
	bind_port_ssl = 443
	ssl_support = None
	monitor_shell_state_freq = 3
	server_version = 'Apache/2.4.1'
	_header = 'Authorization'
	certfile = False # Add path to cert.pem here for SSL or parse it with -c
	keyfile = False  # Add path to priv_key.pem here for SSL or parse it with -k
class File_Smuggler_Settings:
	bind_address = '0.0.0.0'
	bind_port = 8888	
class Sessions_manager_settings:
	shell_state_change_after = 2.0 
class TCP_Sock_Handler_Settings:
	bind_address = '0.0.0.0'
	bind_port = 4443
	sentinel_value = uuid4().hex
	sock_timeout = 4
	recv_timeout = 14
	recv_timeout_buffer_size = 4096
	await_execution_timeout = 90
	alive_echo_exec_timeout = 2.5
	fail_count = 3
	hostname_filter = True
	hostname_filter_warning_delivered = False
class Payload_Generator_Settings:
	pass
class Logging_Settings:
	main_meta_folder_unix = f'{os.path.expanduser("~")}/.local/Villain_meta'
	main_meta_folder_windows = f'{os.path.expanduser("~")}/.local/Villain_meta'
class Loading:
	active = False
	finished = True
	@staticmethod
	def animate(msg):
		Threading_params.thread_limiter.acquire()
		Loading.finished = False
		animate = ['<  ', ' ^ ', '  >', ' _ ']
		while Loading.active:
			for item in animate:
				print(f'\r{msg} {item}', end = '')
				sleep(0.08)
		else:
			print(f'\r{msg}    ', end = '')
			Loading.finished = True
			Threading_params.thread_limiter.release()
			return
	@staticmethod
	def stop(print_nl = False):
		Loading.active = False
		while not Loading.finished:
			sleep(0.05)
		if print_nl:
			print()