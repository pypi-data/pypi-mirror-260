import csip
import cosu
import sys
from multiprocessing import Process, Queue
from queue import Empty
import threading
import time
import os

#from cosu.pso import global_best
from .recosu.pso import global_best

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def run_process(stdout_queue, stderr_queue, results_queue, cosu_queue, data, folder):
    steps = data['steps']
    args = data['arguments']
    calib = data['calibration_parameters']
    
    calibration_map = {}
    for param in calib:
        param_name = param['name']
        param_value = param['value']
        calibration_map[param_name] = param_value
        
    if not os.path.exists(folder):
        os.makedirs(folder)

    if (os.path.exists(os.path.join(folder, 'output.txt'))):
        os.remove(os.path.join(folder, 'output.txt'))
        
    if (os.path.exists(os.path.join(folder, 'error.txt'))):
        os.remove(os.path.join(folder, 'error.txt'))
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    read_stdout, write_stdout = os.pipe()
    read_stderr, write_stderr = os.pipe()
    
    sys.stdout = os.fdopen(write_stdout, 'w')
    sys.stderr = os.fdopen(write_stderr, 'w')
    
    stdour_thread = threading.Thread(target=enqueue_output, args=(os.fdopen(read_stdout, 'r'), stdout_queue))
    stderr_thread = threading.Thread(target=enqueue_output, args=(os.fdopen(read_stderr, 'r'), stderr_queue))
    stdour_thread.daemon = True
    stderr_thread.daemon = True
    stdour_thread.start()
    stderr_thread.start()
    
    options = {}
    oh_strategy = {}
    
    for key in calibration_map.keys():
        if "options_" in key:
            options[key.replace("options_", "")] = float(calibration_map[key])
        if "strategy_" in key:
            oh_strategy[key.replace("strategy_", "")] = calibration_map[key]

    print("\n")
    print(calibration_map)
    print("\n")
    print(options)
    print("\n")
    print(oh_strategy)
    print("\n")
    
    print("Running global_best...\n")

    optimizer, trace = global_best(steps,   
            rounds=(int(calibration_map['min_rounds']), int(calibration_map['max_rounds'])),              
            args=args,      
            n_particles=int(calibration_map['n_particles']),      
            iters=int(calibration_map['iters']),  
            n_threads=int(calibration_map['n_threads']),      
            # ftol=0.00000001,
            options=options,
            oh_strategy=oh_strategy, 
            conf={
                'service_timeout': int(calibration_map['service_timeout']),
                'http_retry': int(calibration_map['http_retry']),
                'http_allow_redirects': True if calibration_map['allow_redirects'] == "True" else False,
                'async_call': True if calibration_map['async_call'] == "True" else False,
                'http_conn_timeout': int(calibration_map['conn_timeout']),
                'http_read_timeout': int(calibration_map['read_timeout']),
                'particles_fail': int(calibration_map['particles_fail'])
                },
            result_queue = cosu_queue
        )
    
    
    stdour_thread.join()
    stderr_thread.join()
    
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    results_queue.put((optimizer, trace))




"""import csip
import cosu
import sys
import multiprocessing
import threading
import time
import os

from cosu.pso import global_best

def run_process(process_queue, data, folder):
    steps = data['steps']
    args = data['arguments']
    calib = data['calibration_parameters']
    
    calibration_map = {}
    for param in calib:
        param_name = param['name']
        param_value = param['value']
        calibration_map[param_name] = param_value
        
    if not os.path.exists(folder):
        os.makedirs(folder)

    if (os.path.exists(os.path.join(folder, 'output.txt'))):
        os.remove(os.path.join(folder, 'output.txt'))
        
    if (os.path.exists(os.path.join(folder, 'error.txt'))):
        os.remove(os.path.join(folder, 'error.txt'))

    sys.stdout = open(os.path.join(folder, 'output.txt'), 'w', buffering=1)
    sys.stderr = open(os.path.join(folder, 'error.txt'), 'w', buffering=1)
    
    options = {}
    oh_strategy = {}
    
    for key in calibration_map.keys():
        if "options_" in key:
            options[key.replace("options_", "")] = float(calibration_map[key])
        if "strategy_" in key:
            oh_strategy[key.replace("strategy_", "")] = calibration_map[key]

    print("\n")
    print(calibration_map)
    print("\n")
    print(options)
    print("\n")
    print(oh_strategy)
    print("\n")
    
    print("Running global_best...\n")

    optimizer, trace = global_best(steps,                 # step definition
            rounds=(int(calibration_map['min_rounds']), int(calibration_map['max_rounds'])),                              # min/max number of rounds
            args=args,                                  # static arguments    
            n_particles=int(calibration_map['n_particles']),                             # number of particle candidates for each param
            iters=int(calibration_map['iters']),                                   # max # of iterations
            n_threads=int(calibration_map['n_threads']),                               # number of threads to use
            # ftol=0.00000001,                          # min cost function delta for convergence
            options=options,       # hyperparameter
            oh_strategy=oh_strategy,   # adaptive hyperparameter adjustments based on current and max # of iterations 
            conf={
                'service_timeout': int(calibration_map['service_timeout']),
                'http_retry': int(calibration_map['http_retry']),
                'http_allow_redirects': True if calibration_map['allow_redirects'] == "True" else False,
                'async_call': True if calibration_map['async_call'] == "True" else False,
                'http_conn_timeout': int(calibration_map['conn_timeout']),
                'http_read_timeout': int(calibration_map['read_timeout']),
                'particles_fail': int(calibration_map['particles_fail'])
                },
        )  
    
    process_queue.put((optimizer, trace))

"""