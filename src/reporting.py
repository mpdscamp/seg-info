import matplotlib.pyplot as plt
import numpy as np
import os

def calculate_averages(results):
    avg_results = {}
    for key, values in results.items():
        if values:
            avg_results[key] = sum(values) / len(values)
        else:
            avg_results[key] = 0
    return avg_results

def print_results(results, config):
    avg_results = calculate_averages(results)
    
    print("\n=== RESULTADOS DAS MEDIÇÕES ===")
    print(f"Média de {config['num_runs']} execuções:")
    print("\n-- TEMPO DE EXECUÇÃO (segundos) --")
    print(f"ECDSA Sign:      {avg_results['ecdsa_sign_times']:.6f}")
    print(f"ECDSA Verify:    {avg_results['ecdsa_verify_times']:.6f}")
    print(f"Dilithium Sign:  {avg_results['dilithium_sign_times']:.6f}")
    print(f"Dilithium Verify:{avg_results['dilithium_verify_times']:.6f}")
    
    print("\n-- USO DE MEMÓRIA (bytes) --")
    print(f"ECDSA Sign:      {avg_results['ecdsa_sign_mems']:.0f}")
    print(f"ECDSA Verify:    {avg_results['ecdsa_verify_mems']:.0f}")
    print(f"Dilithium Sign:  {avg_results['dilithium_sign_mems']:.0f}")
    print(f"Dilithium Verify:{avg_results['dilithium_verify_mems']:.0f}")

def save_results_to_file(results, config, filename):
    avg_results = calculate_averages(results)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("RESULTADOS DAS MEDIÇÕES: ECDSA vs DILITHIUM\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Número de execuções: {config['num_runs']}\n")
        f.write(f"Tamanho da mensagem: {config['message_size']} bytes\n\n")
        
        f.write("TEMPO DE EXECUÇÃO (segundos)\n")
        f.write("-" * 50 + "\n")
        f.write(f"ECDSA Sign:       {avg_results['ecdsa_sign_times']:.6f}\n")
        f.write(f"ECDSA Verify:     {avg_results['ecdsa_verify_times']:.6f}\n")
        f.write(f"Dilithium Sign:   {avg_results['dilithium_sign_times']:.6f}\n")
        f.write(f"Dilithium Verify: {avg_results['dilithium_verify_times']:.6f}\n\n")
        
        f.write("USO DE MEMÓRIA (bytes)\n")
        f.write("-" * 50 + "\n")
        f.write(f"ECDSA Sign:       {avg_results['ecdsa_sign_mems']:.0f}\n")
        f.write(f"ECDSA Verify:     {avg_results['ecdsa_verify_mems']:.0f}\n")
        f.write(f"Dilithium Sign:   {avg_results['dilithium_sign_mems']:.0f}\n")
        f.write(f"Dilithium Verify: {avg_results['dilithium_verify_mems']:.0f}\n")
    
def generate_plots(results, config, output_dir):
    avg_results = calculate_averages(results)
    
    ecdsa_color = '#1f77b4'
    dilithium_color = '#ff7f0e'
    
    operacoes = ['Sign', 'Verify']
    ecdsa_tempos = [avg_results['ecdsa_sign_times'], avg_results['ecdsa_verify_times']]
    dilithium_tempos = [avg_results['dilithium_sign_times'], avg_results['dilithium_verify_times']]
    
    ecdsa_memoria = [avg_results['ecdsa_sign_mems'], avg_results['ecdsa_verify_mems']]
    dilithium_memoria = [avg_results['dilithium_sign_mems'], avg_results['dilithium_verify_mems']]
    
    x = np.arange(len(operacoes))
    largura = 0.35
    
    plt.figure(figsize=(10, 6))
    plt.bar(x - largura/2, ecdsa_tempos, largura, label='ECDSA', color=ecdsa_color)
    plt.bar(x + largura/2, dilithium_tempos, largura, label='Dilithium', color=dilithium_color)
    
    plt.xlabel('Operação')
    plt.ylabel('Tempo (segundos)')
    plt.title('Comparação de Tempo de Execução')
    plt.xticks(x, operacoes)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    for i, v in enumerate(ecdsa_tempos):
        plt.text(i - largura/2, v, f'{v:.6f}', ha='center', va='bottom')
    for i, v in enumerate(dilithium_tempos):
        plt.text(i + largura/2, v, f'{v:.6f}', ha='center', va='bottom')
    
    tempo_output = os.path.join(output_dir, 'tempo_execucao.png')
    plt.tight_layout()
    plt.savefig(tempo_output)
    plt.close()
    
    plt.figure(figsize=(10, 6))
    plt.bar(x - largura/2, ecdsa_memoria, largura, label='ECDSA', color=ecdsa_color)
    plt.bar(x + largura/2, dilithium_memoria, largura, label='Dilithium', color=dilithium_color)
    
    plt.xlabel('Operação')
    plt.ylabel('Memória (bytes)')
    plt.title('Comparação de Uso de Memória')
    plt.xticks(x, operacoes)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.yscale('log')
    
    for i, v in enumerate(ecdsa_memoria):
        plt.text(i - largura/2, v, f'{int(v):,}', ha='center', va='bottom')
    for i, v in enumerate(dilithium_memoria):
        plt.text(i + largura/2, v, f'{int(v):,}', ha='center', va='bottom')
    
    memoria_output = os.path.join(output_dir, 'uso_memoria.png')
    plt.tight_layout()
    plt.savefig(memoria_output)
    plt.close()
    
    print(f"Gráficos gerados em {output_dir}:")
    print(f"- Tempo de execução: {tempo_output}")
    print(f"- Uso de memória: {memoria_output}")
