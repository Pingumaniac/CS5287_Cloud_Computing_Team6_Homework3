# CS5287_Cloud_Computing_Team6_Homework3
Cloud-native Deployment of IoT Data Analytics Pipeline using Kubernetes and Docker

## Goals

1. **Ansible Playbooks Enhancement:**
   - Expand the master playbook by incorporating child playbooks that:
     - Install necessary Kubernetes (K8s) apt and pip packages.
     - Set up a private Docker registry on VM1 (designated as the master).
     - Modify the `config.toml` file to configure the private registry mirror, referencing the Week6B_K8s lecture slides.
     - Restart `containerd` and Docker services to apply the configuration changes.
     - Extend firewall rules to accommodate both K8s and the private registry, as per Week6B_K8s lecture guidance.
     - Disable swap, a requirement for Kubernetes to function correctly.
     - Ensure all additional steps are covered to enable smooth K8s cluster setup.

2. **Manual Kubernetes Cluster Setup:**
   - Manually establish a 4-VM Kubernetes cluster with VM1 acting as the master node.
   - Join the other three VMs as worker nodes, then taint the master to also function as a worker.
   - This results in a fully functional 4-node worker cluster.

3. **IoT Data Pipeline Execution:**
   - Deploy all pipeline components as Docker containers running in their individual K8s pods:
     - Reuse the Dockerfiles from PA2 (Producer, Consumer, ML Inference Server) to build images, and push them to the private registry.
     - Ensure the private registry is accessible from all worker machines.
     - Use Docker images for Kafka and your chosen database from [hub.docker.com](https://hub.docker.com/).
   - Deploy the pipeline:
     - Write YAML files for the Kafka, ML Inference, and database pods using deployment and service pod types.
     - For the producer and consumer, use Job pod types in YAML.
     - Use `kubectl apply` to deploy the components, allowing K8s to handle distribution across the cluster.
     - Ensure the producer sends at least 1,000 samples at a predefined frequency (e.g., one sample per second) and save the end-to-end latency results for further analysis.

4. **Workload Scaling via Kubernetes CLI:**
   - Scale the workload by increasing the number of producers running in separate pods:
     - Utilize Kubernetes’ replication features, such as `replicas: <number>`, or write multiple YAML deployment files to spawn multiple instances of the producer.
     - Ensure each producer instance has a unique ID to distinguish between them during operation.
     - Test the solution with up to 5 producers, as done in PA3, but this time leverage Kubernetes to automatically manage the placement of containers.


## How work was split

* Robert Sheng primarily worked on...
* Youngjae Moon primarily worked on...
* Lisa Liu primarily worked on...

## Team Members

* Young-jae Moon (MS, youngjae.moon@vanderbilt.edu
* Robert Sheng (BS/MS, robert.sheng@vanderbilt.edu
* Lisa Liu (BS, chuci.liu@vanderbilt.edu

under Professor Aniruddha Gokhale, a.gokhale@vanderbilt.edu
