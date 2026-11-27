# VPN WireGuard de Zonalia (#18)

Los 4 nodos se comunican solo por esta VPN. La base primaria, la réplica y MongoDB publican sus puertos únicamente en la IP de la VPN de su nodo.

## Plan de direcciones

Red `10.10.0.0/24`. El número del nodo es el último número de su IP.

| Nodo | IP | Qué corre |
| --- | --- | --- |
| N1 Servicios | 10.10.0.1 | API, Nginx y Suricata |
| N2 Base primaria | 10.10.0.2 | PostgreSQL primario |
| N3 Base secundaria | 10.10.0.3 | PostgreSQL réplica |
| N4 Analítica | 10.10.0.4 | MongoDB y monitoreo |

Qué laptop es cada nodo está en `docs/decisiones/ADR-003-nodos.md`.

## Topología: malla

Cada nodo tiene un `[Peer]` por cada uno de los otros tres, con su IP de la VPN en `AllowedIPs` y su dirección en la red local en `Endpoint`. Así ningún nodo tiene que reenviar tráfico de otro (Windows y macOS no lo hacen sin configuración extra). `PersistentKeepalive = 25` mantiene abierto el túnel aunque no haya tráfico.

## Llaves

- Cada laptop genera su par de llaves en la app de WireGuard (**Add empty tunnel**). La llave privada nunca sale de esa laptop.
- Solo la llave **pública** se comparte con el equipo.
- En el repo solo está `nodo.conf.ejemplo`, con textos de ejemplo. `.gitignore` bloquea `infra/vpn/*.conf` y `wg*.conf`.

## Firewall de cada nodo Windows

En PowerShell como administrador:

```powershell
New-NetFirewallRule -DisplayName "Zonalia WireGuard" -Direction Inbound -Protocol UDP -LocalPort 51820 -Action Allow
New-NetFirewallRule -DisplayName "Zonalia ping VPN" -Direction Inbound -Protocol ICMPv4 -IcmpType 8 -RemoteAddress 10.10.0.0/24 -Action Allow
```

El firewall completo y el endurecimiento de cada nodo llegan en el #34.

## Cómo agregar un nodo

1. Elige el siguiente número libre (por ejemplo, N5 = `10.10.0.5`) y anótalo en la tabla de arriba y en el ADR-003.
2. En la laptop nueva: instala WireGuard, **Add empty tunnel**, nombre `zonalia`, y comparte su llave pública.
3. Llena su túnel con `nodo.conf.ejemplo`: `Address = 10.10.0.5/24` y un `[Peer]` por cada nodo que ya existe.
4. En **cada** nodo que ya existe, agrega un `[Peer]` para el nuevo (su llave pública, `AllowedIPs = 10.10.0.5/32` y su `Endpoint`) y guarda.
5. En Windows, corre las reglas de firewall de arriba.
6. Desde el nodo nuevo, `ping` a cada uno de los demás. Todos deben mostrar **Latest handshake** reciente.

## Limitación conocida

WireGuard necesita que cada nodo pueda recibir paquetes UDP en el puerto 51820 de los otros. Hoy eso se cumple con las 4 laptops en la misma red local. Para nodos en casas o ciudades distintas hace falta un punto de encuentro con IP pública (por ejemplo, un servidor en la nube como nodo central), que queda para la etapa de inversión del presupuesto.