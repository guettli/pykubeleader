# pykubeleader: Simpe Python Application which uses Kubernetes Leader Election

You can apply the `deployment.yaml` file. It will create a Kubernetes Deployment with several pods.

```console
kubectl apply -f deployment.yaml
kubectl apply -f rbac.yaml
```

Only one pod is the active leader.

Leader Election gets done via Kubernetes primitives.

You can show the logs of the pods with this command:

```console
kubectl logs -l app=pykubeleader --follow --max-log-requests 6
```

In a second console, you can delete a pod which is currently the leader:

```console
kubectl delete pod pykubeleader-xxx-yyy
```

After the pod got deleted (this can take some seconds), you see that the leader changed:

```log
2025-06-13 13:54:21,732 pod=pykubeleader-688bb58544-bzmwr canditate=161769f0 - INFO - leader 161769f0-8c44-4e39-bd15-6fa7129ab44a has successfully acquired lease
2025-06-13 13:54:22,651 pod=pykubeleader-688bb58544-jpflb canditate=8be1011c - INFO - yet to finish lease_duration, lease held by 161769f0-8c44-4e39-bd15-6fa7129ab44a and has not expired
2025-06-13 13:54:23,332 pod=pykubeleader-688bb58544-6jgvd canditate=00157d7c - INFO - yet to finish lease_duration, lease held by 161769f0-8c44-4e39-bd15-6fa7129ab44a and has not expired
2025-06-13 13:54:27,659 pod=pykubeleader-688bb58544-jpflb canditate=8be1011c - INFO - yet to finish lease_duration, lease held by 161769f0-8c44-4e39-bd15-6fa7129ab44a and has not expired
2025-06-13 13:54:28,341 pod=pykubeleader-688bb58544-6jgvd canditate=00157d7c - INFO - yet to finish lease_duration, lease held by 161769f0-8c44-4e39-bd15-6fa7129ab44a and has not expired
2025-06-13 13:54:32,669 pod=pykubeleader-688bb58544-jpflb canditate=8be1011c - INFO - yet to finish lease_duration, lease held by 161769f0-8c44-4e39-bd15-6fa7129ab44a and has not expired
2025-06-13 13:54:33,351 pod=pykubeleader-688bb58544-6jgvd canditate=00157d7c - INFO - yet to finish lease_duration, lease held by 161769f0-8c44-4e39-bd15-6fa7129ab44a and has not expired
2025-06-13 13:54:37,679 pod=pykubeleader-688bb58544-jpflb canditate=8be1011c - INFO - yet to finish lease_duration, lease held by 161769f0-8c44-4e39-bd15-6fa7129ab44a and has not expired
2025-06-13 13:54:38,360 pod=pykubeleader-688bb58544-6jgvd canditate=00157d7c - INFO - yet to finish lease_duration, lease held by 161769f0-8c44-4e39-bd15-6fa7129ab44a and has not expired
2025-06-13 13:54:42,699 pod=pykubeleader-688bb58544-jpflb canditate=8be1011c - INFO - leader 8be1011c-3739-4540-a70d-ce1d9bca0699 has successfully acquired lease
2025-06-13 13:54:42,700 pod=pykubeleader-688bb58544-jpflb canditate=8be1011c - INFO - 8be1011c-3739-4540-a70d-ce1d9bca0699 successfully acquired lease
2025-06-13 13:54:42,700 pod=pykubeleader-688bb58544-jpflb canditate=8be1011c - INFO - I am leader.
2025-06-13 13:54:42,700 pod=pykubeleader-688bb58544-jpflb canditate=8be1011c - INFO - Leader has entered renew loop and will try to update lease continuously
2025-06-13 13:54:42,719 pod=pykubeleader-688bb58544-jpflb canditate=8be1011c - INFO - leader 8be1011c-3739-4540-a70d-ce1d9bca0699 has successfully acquired lease
2025-06-13 13:54:43,367 pod=pykubeleader-688bb58544-6jgvd canditate=00157d7c - INFO - Leader has switched to 8be1011c-3739-4540-a70d-ce1d9bca0699
```

## Development

You can update the code and create a new container image, and restart the deployment:

```console
./build-and-push-container-image.sh; kubectl rollout restart deployment pykubeleader
```
