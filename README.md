This repo provides the following:
1. A test application using Keras models (MobileNet and ResNet).
2. A modified version of Tensorflow with extra logs in the Op::Compute calls to Tensorflow operations.
3. The ability to trace the logs in the Op::Compute calls on running models using bpftrace and/or Pixie.

## Setup - local

1. Install bpftrace. These examples were built with version 0.14.1.

```
# Check to ensure the version is v0.14.1 or something close to it.
bpftrace -V
```

1. Run the test server.

```
cd server
# Optional: use a virtual environment
pip install -r requirements.txt
pip install tensorflow-2.9.0-cp38-cp38-linux_x86_64.whl
python3 server.py
```

2. Deploy a bpftrace probe in a new tab.

```
sudo bpftrace ../bpftrace/LogOpInfo.bt
```

3. Invoke the model in a new tab.

```
# To run the MobileNet model:
curl http://127.0.0.1:5000/execute/grace_hopper

#  To run the ResNet model:
curl http://127.0.0.1:5000/execute/elephant
```

4. Switch back to the bpftrace tab and observe the results of the tracing. The python server will also output logs, though this will be changed in a later versino.

## Setup - Kubernetes

1. Create a Kubernetes cluster with 1 node. Note that this demo is only supported for 1 node clusters.

2. Deploy Pixie to your cluster by following the instruction on docs.px.dev.

3. Create the test server.
```
kubectl apply -f server/server.yaml
```

4. Once server pod is running, check to make sure that it's working as expected.
```
kubectl get pods
# Make sure the mlexray pod is Running before continuing to this step.
kubectl port-forward service/mlexray-k8s-app 5000:5000

# Switch to a new tab

# To run the MobileNet model:
curl http://127.0.0.1:5000/execute/grace_hopper

#  To run the ResNet model:
curl http://127.0.0.1:5000/execute/elephant
```

5. Go to the Pixie UI. Scroll down to the `Pods` table. Click on the pod name for mlexray, it should take you to the `px/pod` script.

6. Find the process ID associated with the `/usr/bin/python3 /app/server.py` command (note: this is not the same as the one for the `python3 server.py` command). You may need to `curl` the server a few times to see it show up in the `Processes` table. Write down the process ID.

7.  Open the `pxl/Log*.pxl` files in a text editor. Update `/proc/2532969` to be `/proc/<your process ID>`. Some files have multiple instances of this.

8. Navigate to the `Scratch Pad` script from the Script dropdown in the Pixie UI. Open the script editor in Pixie.

9. For each of the 4 `Log*.pxl` scripts that you edited, do the following. Delete the contents of the PxL script in the scratch pad and replace it with the contents of the `Log*.pxl` file. Press run to deploy the probes. Note that if the probe fails, you will need to change the `table_name` value to a unique name when you redeploy.

10. Once your probes are deployed, paste in the contents of `top_ops.pxl` to the `PxL script` tab in the editor. Paste in the contents of `top_ops.json` to the `Vis spec` tab in the editor. Press Run.

11. Repeat the `curl` commands in the earlier step to execute the model of your choice.

12. Press Run again in the Pixie UI in order to see the results of your probes.

## Updating the server Dockerfile

```
cd server
docker build . -t <imagename>:<tag>
docker push <imagename>:<tag>
# Update server.yaml to point to the new image
```

