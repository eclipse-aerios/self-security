# Self-Security

Self security module will check network interfaces and will analyse traffic to check if there are attacks or vulnerabilities. Potentially a example for simple use case will block the traffic if some rules/conditions are met.

This module focuses on deploying an Intrusion Detection System (IDS) based on suricata on a kubernetes cluster. It aims to monitor network traffic towards the nodes of the kubernetes cluster as described above.

The following figure describe the self-security module inside the IE and the relationship with another self-* modules.

<figure>
  <img src="self-features-interaction.png" alt="aerOS sefl-features interaction diagram"/>
  <figcaption><b>Figure 1. aerOS sefl-features interaction diagram </b></figcaption>
</figure>

## Getting start / Use

The main objective is to monitor the network traffic of our system. The essential configuration files for this module are:

- [suricata.yaml](suricata.yaml)
- [suricata.rules](suricata.rules)

With Suricata in our system, we can monitor network traffic through a network interface; we can do it using the command:

```
sudo suricata -c /etc/suricata/suricata.yaml -i <INTERFACE>
```

- `-c /etc/suricata/suricata.yaml`: with the `-c` feature, we indicate the PATH of the configuration file we will use to start Suricata.By default Suricata has the configuration file `/etc/suricata/suricata.yaml`.
- `-i`: with the `-i` feature, we can select the network interface, `<INTERFACE>` on which Suricata will be active.

## How to build, install, or deploy it

1. It would be advisable to update our system:
    ```bash
    sudo apt update && sudo apt upgrade
    ```

2. Install the necessary dependencies for Suricata and for the ETL script ([`etl.py`](etl.py)):
    ```bash
    sudo apt install libpcre3 libpcre3-dbg libpcre3-dev build-essential libpcap-dev \
        libnet1-dev libyaml-0-2 libyaml-dev pkg-config zlib1g zlib1g-dev \
        libcap-ng-dev libcap-ng0 make libmagic-dev libjansson-dev \
        libnss3-dev libgeoip-dev liblua5.1-dev libhiredis-dev libevent-dev \
        python3 python3-yaml
    ```

    ```bash
    pip3 install requests
    ```

3. Install Suricata:
    ```bash
    sudo apt install suricata
    ```

4. We can check the location of the Suricata configuration files on your system to obtain more information about its installation:
    ```bash
    ls /etc/suricata/
    ```

5. Put the [`etl.py`](etl.py) script in the directory we want to later execute it.

## Testing

Before starting Suricata, we need to make sure we configure Suricata. We have used the `suricata.yaml` file as the Suricata configuration file, which we will configure in `/etc/suricata/suricata.yaml`, and we have also used the custom rules `suricata.rules`, which we will have in `/var/ lib/suricata/rules/suricata.rules`. If we want to change the path from where Suricata acquires the rules that we are going to configure, we can do it in the `suricata.yaml` file in:

```yaml
default-rule-path: /var/lib/suricata/rules

rule-files:
  - suricata.rules
```

Now, we can start Suricata and check that it generates the data using some traffic, for example, ICMP.

1. Run Suricata:
    ```shell
    sudo suricata -c /etc/suricata/suricata.yaml -i <INTERFACE>
    ```

    >NOTE: select the network interface that we are going to use.

2. Run the [`etl.py`](etl.py) script where we will put the URL of our enpdoint.
    ```bash
    python3 etl.py
    ```

3. Now we can generate traffic to verify that Suricata is working and generating the necessary data
    ```shell
    ping <NODE-IP>
    ```

    To verify Suricata's activity:

    ```shell
    cat /var/log/suricata/fast.log
    ```

    ```shell
    cat /var/log/suricata/eve.json
    ```

4. Check the data on our endpoint.

### Nmap Test

We can simulate scanning by Nmap to verify that the alerts are generated and are being reflected on the API server. Here we can see some scanning examples that we can check:

- **Nmap SYN Scan**:
	```shell
	nmap -sS -p 80 <target_IP>
	```

- **Nmap FIN Scan**:
	```shell
	nmap -sF -p 80 <target_IP>
	```

- **Nmap NULL Scan**:
	```shell
	nmap -sN -p 80 <target_IP>
	```

## Tutorial

1. Clone the repository.
2. Change the values we want in `suricata.yaml` and `suricata.rules`.
3. Install Suricata and the necessary dependencies and install Python library `requests`.
4. Copy `suricata.yaml` to path `/etc/suricata/` and `suricata.rules` to path `/var/lib/suricata/rules/`
5. Run Suricata.
6. Run the `etl.py`.
7. Perform the test using ICMP traffic.
8. Check Suricata activity.
9. Check the data on our endpoint.

## Credits

This template has been created by: Ramiro Torres (@rtorres_S21Sec) as part of the S21Sec team

This module is based on the project [jasonish/suricata](https://github.com/jasonish/docker-suricata).

## License

The module is distributed under the specified license. For detailed licensing information, refer to the [LICENCE.TXT](LICENCE.TXT) file in the repository.


