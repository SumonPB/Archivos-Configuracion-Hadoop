FROM ubuntu:22.04

ARG HADOOP_VERSION=3.4.2
ENV HADOOP_VERSION=${HADOOP_VERSION}
ENV HADOOP_URL=https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz
ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# 🔥 AÑADIR variable crítica
ENV HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk ssh rsync wget vim sudo net-tools iputils-ping && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget $HADOOP_URL -O /tmp/hadoop.tar.gz && \
    tar -xzf /tmp/hadoop.tar.gz -C /usr/local && \
    mv /usr/local/hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm /tmp/hadoop.tar.gz

RUN ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 0600 /root/.ssh/authorized_keys

ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root
ENV YARN_RESOURCEMANAGER_USER=root
ENV YARN_NODEMANAGER_USER=root

# 🔥 FORZAR configuración de Hadoop - AGREGAR ESTO AL FINAL
RUN echo 'export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
RUN echo 'export HADOOP_PREFIX=/usr/local/hadoop' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh

# 🔥 Crear enlaces simbólicos para forzar configuración
RUN ln -sf /usr/local/hadoop/etc/hadoop /etc/hadoop

# 🔥 Configurar alternativas del sistema
RUN update-alternatives --install /etc/hadoop conf /usr/local/hadoop/etc/hadoop 100

# 🔥 SCRIPT CORREGIDO - VERSIÓN DEFINITIVA
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "=== Iniciando contenedor: $(hostname) ==="\n\
\n\
# Crear directorios necesarios\n\
mkdir -p /usr/local/hadoop/logs\n\
mkdir -p /usr/local/hadoop/dfs/name\n\
mkdir -p /usr/local/hadoop/dfs/data\n\
\n\
# Iniciar SSH\n\
service ssh start\n\
\n\
# Configurar hosts PRIMERO\n\
echo "127.0.0.1 localhost" > /etc/hosts\n\
echo "172.20.0.2 namenode" >> /etc/hosts\n\
echo "172.20.0.3 datanode1" >> /etc/hosts\n\
echo "172.20.0.4 datanode2" >> /etc/hosts\n\
\n\
# 🔥 FORZAR variable de entorno en múltiples lugares\n\
export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop\n\
echo "export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop" >> /root/.bashrc\n\
\n\
# Solo NameNode inicia servicios Hadoop\n\
if [ "$(hostname)" = "namenode" ]; then\n\
    echo "=== Iniciando servicios en NameNode ==="\n\
    \n\
    # Esperar a que los DataNodes estén listos\n\
    echo "Esperando a DataNodes..."\n\
    sleep 45\n\
    \n\
    if [ ! -d /usr/local/hadoop/dfs/name/current ]; then\n\
        echo "=== Formateando HDFS ==="\n\
        HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop hdfs namenode -format -force -nonInteractive\n\
    fi\n\
    \n\
    echo "=== Iniciando DFS ==="\n\
    # 🔥 Forzar configuración en CADA comando\n\
    HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop /usr/local/hadoop/sbin/start-dfs.sh\n\
    \n\
    echo "=== Iniciando YARN ==="\n\
    HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop /usr/local/hadoop/sbin/start-yarn.sh\n\
    \n\
    echo "=== Hadoop iniciado ==="\n\
    echo "Web UI HDFS: http://localhost:9870"\n\
    echo "Web UI YARN: http://localhost:8088"\n\
    \n\
    # Verificar estado\n\
    sleep 20\n\
    HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop hdfs dfsadmin -report\n\
else\n\
    echo "=== DataNode $(hostname) listo ==="\n\
    echo "Esperando conexiones del NameNode..."\n\
    # 🔥 Los DataNodes se inician automáticamente por start-dfs.sh\n\
fi\n\
\n\
echo "=== Contenedor $(hostname) activo ===\n\
Manteniendo contenedor vivo..."\n\
\n\
# Mantener el contenedor activo\n\
tail -f /dev/null' > /usr/local/bin/start-hadoop.sh && chmod +x /usr/local/bin/start-hadoop.sh

EXPOSE 22 9870 8088 8020 9864 9865 9866

CMD ["/usr/local/bin/start-hadoop.sh"]