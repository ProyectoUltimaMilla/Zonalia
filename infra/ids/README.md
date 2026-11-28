# IDS Suricata (#24)

Suricata corre en N1 en modo pasivo: copia y analiza el tráfico que llega a Nginx, anota alertas y no bloquea nada. Comparte la red del contenedor de Nginx (`network_mode: service:nginx`), así ve las mismas peticiones que la API.

## Reglas

- De la comunidad: Emerging Threats Open, se descargan con `suricata-update` y se guardan en el volumen `suricata-reglas`.
- Propias: `zonalia.rules` (sqlmap y Nmap por User-Agent).
- `EXTERNAL_NET` se pone en `any` porque las laptops del equipo usan direcciones privadas (10.10.0.0/24); con el valor normal, Suricata no tomaría a un compañero como externo.

## Cómo se usa

En N1:

    docker compose --profile n1 up -d --build
    docker compose exec suricata suricata-update
    docker compose restart suricata

Ver las alertas:

    docker compose exec suricata tail -n 20 /var/log/suricata/fast.log

## Prueba

Desde otra laptop conectada a la VPN:

    curl.exe -A "sqlmap/1.8" http://10.10.0.1:8080/health

Debe aparecer `ZONALIA escaneo con sqlmap` en `fast.log`.