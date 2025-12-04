# Self-Security

Self security module will check network interfaces and will analyse traffic to check if there are attacks or vulnerabilities. Potentially a example for simple use case will block the traffic if some rules/conditions are met.

This module focuses on deploying an Intrusion Detection System (IDS) based on suricata on a kubernetes cluster. It aims to monitor network traffic towards the nodes of the kubernetes cluster as described above.

The following figure describe the self-security module inside the IE and the relationship with another self-* modules.

<figure>
  <img src="self-features-interaction.png" alt="aerOS sefl-features interaction diagram"/>
  <figcaption><b>Figure 1. aerOS sefl-features interaction diagram </b></figcaption>
</figure>

## Getting start / Use

The primary objective is to monitor the network traffic directed towards the nodes of our Kubernetes cluster. The configuration files essential for this module are:

- [values.yaml](self-security/values.yaml)
- [chart.yaml](self-security/Chart.yaml)
- [suricata-daemonset.yaml](self-security/templates/daemonset.yaml)
- [suricata.yaml](self-security/templates/suricata-suricata.yaml)
- [suricata.rules](self-security/templates/suricata-rules.yaml)



## How to build, install, or deploy it

Before deploying our file [values.yaml](self-security/values.yaml), we will have to configure the URL of the endpoint, the Trust Manager endpoint server, in the:

  ```yaml
      etl:
      
      endpointURL: "http://ENDPOINT_URL/notification"

  ```

>NOTE: the **ETL** configuration to send the Suricata data via the PUT method is located in the [etl](../Docker_image_files/etl/etl.pyself-security/templates/) folder

### Setting up

**Setting up the configuration**

The rules for the detection of different attacks can be added directly to [values.yaml](self-security/values.yaml). Here are some examples:
- [ ] **Detection of a network scanning attack**
```yaml
     alert tcp any any -> $HOME_NET any (content:"nmap"; nocase; msg:"Possible Nmap Script Scan"; detection_filter: track by_src, count 50, seconds 2; sid:1000007;)
```
- [ ] **Detection of a brute force attack (e.g. to the Keycloak endpoint**
```yaml
       alert http any any -> $HOME_NET any (msg:"Keycloak Brute Force Detected"; flow:to_server,established; content:"POST"; http_method; content:"/protocol/openid-connect/token"; http_uri; threshold:type both, track by_src, count 10, seconds 60; classtype:attempted-recon; sid:1000012; rev:1;)
```


**Instalation**

In oder to deploy the self-security module with helm it can be done in two ways:

- [ ] Option 1: Deploy from source code
    ```shell
    helm install self-security self-security/
    ```


## Testing

### Nmap Test

We can simulate scanning by Nmap to verify that the alerts are generated and are being reflected on the API server. Here we can see some scanning examples that we can check:

- **Nmap Scan**:
	```shell
	nmap <target_IP> -Pn -A -T4
	```

To verify Suricata's activity:

  ```shell
  kubectl exec -it <POD_NAME> -- cat /var/log/suricata/fast.log
  ```

And we will also have to check the data on the endpoint (Trust Manager) or the self-security API: [http://NodeIP:8000/events](http://nodeip:8000/events).
## Tutorial

1. Clone the repository.
2. Change the values in [values.yaml](self-security/values.yaml) and change the value for `http://ENDPOINT_URL`.
3. Deploy the suricata configuration and check firewall rules if we are using cloud services.
4. Perform the test using NMAP traffic.
6. Check Suricata activity.
7. Check the data on the endpoint (Trust Manager).

## Credits

This template has been created by: Ramiro Torres (@rtorres_S21Sec) and Jon Egaña (@jegana) as part of the S21Sec team.

This module is based on the project [jasonish/suricata](https://github.com/jasonish/docker-suricata).

## License

The module is distributed under the specified license. For detailed licensing information, refer to the [LICENCE.TXT](../LICENCE.TXT) file in the repository.


