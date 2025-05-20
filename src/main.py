import os
import time
import tracemalloc
import sys
from algorithms.ecdsa.ecdsa import ECDSA
from algorithms.dilithium.dilithium import Dilithium
import reporting

MESSAGE_FILE_PATH = "message.txt"
RESULTS_DIR = "../results"
RESULTS_FILE = os.path.join(RESULTS_DIR, "results.txt")
DILITHIUM_SECURITY_LEVEL = 3
NUM_RUNS = 100

def read_message_file(filename=MESSAGE_FILE_PATH):
    with open(filename, "rb") as f:
        message = f.read()
    
    return message

def measure_operation(func, *args, **kwargs):
    result = None
    start_time = 0.0
    end_time = 0.0
    peak_mem = 0

    if tracemalloc.is_tracing():
        tracemalloc.stop()
    tracemalloc.start()
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    elapsed_time = end_time - start_time
    
    return result, elapsed_time, peak_mem

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    ecdsa_impl = ECDSA()
    dilithium_impl = Dilithium(security_level=DILITHIUM_SECURITY_LEVEL)

    results = {
        "ecdsa_sign_times": [],
        "ecdsa_sign_mems": [],
        "ecdsa_verify_times": [],
        "ecdsa_verify_mems": [],
        
        "dilithium_sign_times": [],
        "dilithium_sign_mems": [],
        "dilithium_verify_times": [],
        "dilithium_verify_mems": [],
    }
    
    message_bytes = read_message_file()
        
    for i in range(NUM_RUNS):
        dilithium_keys = dilithium_impl.keygen()
        ecdsa_keys = ecdsa_impl.keygen()
        
        if dilithium_keys and ecdsa_keys:
            dilithium_priv_key, dilithium_pub_key = dilithium_keys
            ecdsa_priv_key, ecdsa_pub_key = ecdsa_keys
            
            ecdsa_sig, time_s, mem_b = measure_operation(
                ecdsa_impl.sign, message_bytes, ecdsa_priv_key
            )
            
            if ecdsa_sig:
                results["ecdsa_sign_times"].append(time_s)
                results["ecdsa_sign_mems"].append(mem_b)
                
                _, time_s, mem_b = measure_operation(
                    ecdsa_impl.verify, message_bytes, ecdsa_sig, ecdsa_pub_key
                )
                results["ecdsa_verify_times"].append(time_s)
                results["ecdsa_verify_mems"].append(mem_b)
            
            dilithium_sig, time_s, mem_b = measure_operation(
                dilithium_impl.sign, message_bytes, dilithium_priv_key
            )
            
            if dilithium_sig:
                results["dilithium_sign_times"].append(time_s)
                results["dilithium_sign_mems"].append(mem_b)
                
                _, time_s, mem_b = measure_operation(
                    dilithium_impl.verify, message_bytes, dilithium_sig, dilithium_pub_key
                )
                results["dilithium_verify_times"].append(time_s)
                results["dilithium_verify_mems"].append(mem_b)
    
    config = {
        "num_runs": NUM_RUNS,
        "message_size": len(message_bytes)
    }
    
    reporting.print_results(results, config)
    reporting.save_results_to_file(results, config, RESULTS_FILE)
    
    reporting.generate_plots(results, config, RESULTS_DIR)

if __name__ == "__main__":
    main()