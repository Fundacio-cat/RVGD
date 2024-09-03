# Rede de Vixilancia do Galego Dixital 

## Versión 1.0 posta en marcha o 29-04-24

Cada sensor ten un contrasinal e un usuario personalizado.

git clone https://github.com/paufundacio/RVGD.git

### Crontab de cada sensor

```bash
*/15 9-21 * * 1-5 bash /home/galego/RVGD/executa_galego.bash
0 1 * * * sudo /sbin/shutdown -r # Reinicia á 1 da mañá todos os días
```

# Lingua

A librería utilizada para detectar a lingua de cada páxina web é a seguinte:

https://github.com/aboSamoor/polyglot

### Agradecementos

A Miguel Cabeza. Orgulloso vigués e afeccionado do Celta de Vigo.