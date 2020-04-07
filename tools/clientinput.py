import psutil
import platform


def process_exists(process_name):
	if is_win():
	    for proc in psutil.process_iter():
	        try:
	            if process_name.lower() in proc.name().lower():
	                return True
	        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
	            pass
	return False


def is_win():
	return platform.system() in ['Windows', 'Linux']
