# Self-Security

Self security module will check network interfaces and will analyse traffic to check if there are cybersecurity attacks.

This module focuses on deploying an Intrusion Detection System (IDS) based on suricata. It aims to monitor network traffic towards the nodes of the kubernetes (or Docker) cluster as described above.

The following figure describe the self-security module inside the IE and the relationship with another self-* modules.

<figure>
  <img src="self-features-interaction.png" alt="aerOS sefl-features interaction diagram"/>
  <figcaption><b>Figure 1. aerOS sefl-features interaction diagram </b></figcaption>
</figure>

## Getting start / Use

The primary objective is to monitor the network traffic directed towards the nodes of our Kubernetes cluster. We can alternatively use two infrastructures to implement Suricata depending on our needs:

- [ ] [K8s infrastructure](k8s-infra)
- [ ] [Helm](k8s-infra/helm/)
- [ ] [Non K8s infrastructure](non-k8s-infra)

>NOTE: All the necessary resources and configurations are located within their respective folders.

## How to build, install, or deploy it
### [Helm](k8s-infra/helm/README.md#how-to-build-install-or-deploy-it)
efore deploying our file [values.yaml](k8s-infra/helm/self-security/values.yaml),  the URL of the endpoint should be configured, the Trust Manager endpoint server, in the:

  ```yaml
      etl:
      
      endpointURL: "http://ENDPOINT_URL/notification"

  ```
**Instalation**

In oder to deploy the self-security module with helm it can be done in two ways:

- [ ] Option 1: Deploy from source code
    ```shell
    helm install self-security self-security/
    ```


### [K8s infrastructure](k8s-infra/README.md#how-to-build-install-or-deploy-it)

Before deploying our file `suricata-daemonset.yaml`, we will have to configure the URL of the endpoint server in the:

```yaml
            - name: ENDPOINT_URL
              value: "http://ENDPOINT_URL"
```

>NOTE: The **ETL** configuration to send the Suricata data via the PUT method is located in the [etl k8s-infra](k8s-infra/Docker_image_files/etl) folder or [etl non-k8sinfra](non-k8s-infra/etl.py)

In the case of a k8s infrastructure, we can choose the Suricata implementation through:

- [ ] [Setting up](k8s-infra/README.md#setting-up):
  >**1 Setting up the configuration:**<br>
  >We can modify the `suricata.yaml`/`suricata-suricata.yaml` and `suricata.rules`/`suricata-rules.yaml` configuration files as required depending on the *Option* we use to apply the configuration, as seen below.<br><br>
  >**2 Applying settings**:<br>
  >There are two options to apply the configuration to the Kubernetes cluster:
  >- [ ] Option 1:
  >  	```shell
  >  	kubectl create -f suricata-suricata.yaml
  > 	kubectl create -f suricata-rules.yaml
  >  	kubectl create -f suricata-daemonset.yaml
  >  	```
  >- [ ] Option 2:
  >  	```shell
  >  	kubectl create configmap suricata-config --from-file=suricata.yaml=suricata.yaml
  >  	kubectl create configmap suricata-rules --from-file=suricata.rules
  >  	kubectl create -f suricata-daemonset.yaml
  >  	```


### [Non K8s infrastructure](non-k8s-infra/README.md#how-to-build-install-or-deploy-it)

In the case of a non-k8s infrastructure, we have this configuration:

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

### Basic Test

#### [K8s infrastructure](k8s-infra/README.md#testing) / [Helm](k8s-infra/README.md#tutorial)

After deploying Suricata, you can test its functionality by sending ICMP packets using the Ping command. The rules configured in suricata.rules or suricata-rules.yaml will determine Suricata's response.

1. Use the following commands to test:

	```shell
	nmap <target_IP> -Pn -A -T4
	```

2. To verify Suricata's activity:

    ```shell
    kubectl exec -it <POD_NAME> -- cat /var/log/suricata/fast.log
    ```


#### [Non K8s infrastructure](non-k8s-infra/README.md#testing)

Run Suricata:
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
	nmap <target_IP> -Pn -A -T4
	```
  
4. To verify Suricata's activity:
    ```shell
    cat /var/log/suricata/fast.log
    ```


## Tutorial

### [Helm](k8s-infra/helm/README.md#tutorial)

1. Clone the repository.
2. Change the values in [values.yaml](k8s-infra/helm/self-security/values.yaml) and change the value for `http://ENDPOINT_URL`.
3. Deploy the suricata configuration and check firewall rules if we are using cloud services.
4. Perform the test using NMAP traffic.
6. Check Suricata activity.
7. Check the data on the endpoint (Trust Manager).

### [K8s infrastructure](k8s-infra/README.md#tutorial) 

1. Clone the repository.
2. Change the values we want in `suricata.yaml`/`suricata-suricata.yaml` and `suricata.rules`/`suricata-rules.yaml`.
3. Change the value for `http://ENDPOINT_URL` in `suricata-daemonset.yaml`.
4. Deploy the suricata configuration and check firewall rules if we are using cloud services.
5. Perform the test using Nmap.
6. Check Suricata activity.
7. Check the data on the endpoint (trust Manager).

### [Non K8s infrastructure](non-k8s-infra/README.md#tutorial)

1. Clone the repository.
2. Change the values we want in `suricata.yaml` and `suricata.rules`.
3. Install Suricata and the necessary dependencies and install Python library `requests`.
4. Copy `suricata.yaml` to path `/etc/suricata/` and `suricata.rules` to path `/var/lib/suricata/rules/`
5. Run Suricata.
6. Run the `etl.py`.
7. Perform the test using Nmap.
8. Check Suricata activity.
9. Check the data the endpoint (Trust Manager).

## Credits

This template has been created by: Ramiro Torres (@rtorres_S21Sec) and Jon Egaña (@jegana) as part of the S21Sec team.

This module is based on the project [jasonish/suricata](https://github.com/jasonish/docker-suricata).


## License

The module is distributed under the specified license. For detailed licensing information, refer to the [LICENCE.TXT](LICENCE.TXT) file in the repository.
