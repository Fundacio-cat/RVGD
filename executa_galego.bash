#!/bin/bash
#
# /home/galego/RVGD/executa_galego.bash
# Lanzamento de consultas aleatorias
# Versión 0.0.1
#
home_galego_monitor=/home/galego/RVGD
logs=$home_galego_monitor/logs/monitor.log
echo "Iniciando o proceso galego con logs en $logs"

# Calcula un atraso aleatorio entre 0 e 14 minutos
retard=$(($RANDOM%(14-1)+1))
#echo "Iniciando o proceso despois dun atraso de $retard minutos"
sleep ${retard}m

# Executa o script nun subshell, cambia ao directorio e executa o comando,
# redirixindo calquera saída a /dev/null (descarta a saída)
(cd $home_galego_monitor; xvfb-run -a python3 monitor.py) >> /dev/null  2>&1 &

# Rexistra a data e hora da execución
date >> $logs 2>&1
