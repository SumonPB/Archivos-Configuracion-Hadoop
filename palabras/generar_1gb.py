import random
import sys

print('=== INICIANDO GENERACIÓN DE ARCHIVO 1GB+ ===')
print('Este proceso tomará varios minutos...')

# Lista de palabras
base_words = ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'si', 'con', 'su', 'al', 'lo', 'como', 'mas', 'pero', 'sus', 'ya', 'o', 'este', 'ha', 'por', 'muy', 'sin', 'sobre', 'mi', 'tu', 'hay', 'que', 'quien', 'donde', 'cuando', 'como', 'estoy', 'esta', 'estas', 'estan']
hadoop_words = ['hadoop', 'mapreduce', 'hdfs', 'yarn', 'bigdata', 'cluster', 'datos', 'analisis', 'procesamiento', 'distribuido', 'almacenamiento', 'computo', 'nodemanager', 'resourcemanager', 'datanode', 'namenode', 'replicacion', 'bloques', 'metadata', 'framework', 'java', 'apache', 'escalable', 'eficiente']

all_words = base_words + hadoop_words
print(f'Usando {len(all_words)} palabras únicas...')

total_lines = 20000000  # 20M líneas ≈ 1GB

print(f'Generando {total_lines:,} líneas...')
with open('/tmp/archivo_1gb.txt', 'w', encoding='utf-8') as f:
    for i in range(total_lines):
        num_words = random.randint(8, 15)
        line = ' '.join(random.choices(all_words, k=num_words))
        f.write(line + '\n')
        
        if (i + 1) % 1000000 == 0:
            progress = (i + 1) // 1000000
            print(f'✅ Progreso: {progress}M/20M líneas')

print('=== GENERACIÓN COMPLETADA ===')