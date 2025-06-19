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



--- 

bus coruña
sergas
depor
abono renfe
celta
ikea porto
luces vigo
intermodal vigo
termas ourense
meteogalicia
tvg
xunta
galiña azul
usc
udc
uvigo
vacina gripe
vacuna gripe
magosto
san xoan
matrícula USC
Selectividade Galicia

---

"Camiño de Santiago"
"galicia"
"galiza"

INSERT INTO buscas VALUES (9, 'bus coruña', 1, null);
INSERT INTO buscas VALUES (10, 'sergas', 1, null);
INSERT INTO buscas VALUES (11, 'depor', 1, null);
INSERT INTO buscas VALUES (12, 'abono renfe', 1, null);
INSERT INTO buscas VALUES (13, 'celta', 1, null);
INSERT INTO buscas VALUES (14, 'ikea porto', 1, null);
INSERT INTO buscas VALUES (15, 'luces vigo', 1, null);
INSERT INTO buscas VALUES (16, 'intermodal vigo', 1, null);
INSERT INTO buscas VALUES (17, 'termas ourense', 1, null);
INSERT INTO buscas VALUES (18, 'meteogalicia', 1, null);
INSERT INTO buscas VALUES (19, 'tvg', 1, null);
INSERT INTO buscas VALUES (20, 'xunta', 1, null);
INSERT INTO buscas VALUES (21, 'galiña azul', 1, null);
INSERT INTO buscas VALUES (22, 'usc', 1, null);
INSERT INTO buscas VALUES (23, 'udc', 1, null);
INSERT INTO buscas VALUES (24, 'uvigo', 1, null);
INSERT INTO buscas VALUES (25, 'vacina gripe', 1, null);
INSERT INTO buscas VALUES (26, 'vacuna gripe', 1, null);
INSERT INTO buscas VALUES (27, 'magosto', 1, null);
INSERT INTO buscas VALUES (28, 'san xoan', 1, null);
INSERT INTO buscas VALUES (29, 'matrícula USC', 1, null);
INSERT INTO buscas VALUES (30, 'Selectividade Galicia', 1, null);
