# pykubeleader: Simpe Python Application which uses Kubernetes Leader Election

You can apply the `deployment.yaml` file. It will create a Kubernetes Deployment with several pods.

```console
kubectl apply deployment
```

Only one pod is the active leader.

Leader Election gets done via Kubernetes primitives.

You can show the logs of the pods with this command:

```console
kubectl logs -l app=pykubeleader
```

## Development

You can update the code and create a new container image, and restart the deployment:

```console
./build-and-push-container-image.sh; kubectl rollout restart deployment pykubeleader
```
