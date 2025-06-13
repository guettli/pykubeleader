# Copyright 2025 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import uuid
from kubernetes import config
from kubernetes.leaderelection import leaderelection
from kubernetes.leaderelection.resourcelock.configmaplock import ConfigMapLock
from kubernetes.leaderelection import electionconfig
import time
import random
import signal
import threading


import logging


# The function that a user wants to run once a candidate is elected as a leader
class Singleton:
    def __init__(self, pod_name):
        self.pod_name = pod_name

    def start(self):
        alive = random.uniform(5, 10)
        logging.info("I am leader. Working for {} seconds...".format(alive))

        # Stop the current process after 'alive' seconds without blocking
        pid = os.getpid()

        def terminate_process():
            os.kill(pid, signal.SIGTERM)

        t = threading.Timer(alive, terminate_process)
        t.start()

    def stop(self):
        logging.info("I am no longer the leader. Stopping ...")
        os.exit(0)


def usage():
    print(
        """Usage: %s pod-name

This script demonstrates leader election in Kubernetes using a ConfigMap lock.
Ensure you have a valid kubeconfig file set in the KUBECONFIG environment variable.
"""
        % sys.argv[0],
    )


def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    pod_name = sys.argv[1].strip()
    # Authenticate using config file
    kubeconfig = os.environ.get("KUBECONFIG")
    if kubeconfig:
        if not os.path.exists(kubeconfig):
            raise FileNotFoundError(
                f"Kubeconfig file not found at {kubeconfig} (use env var KUBECONFIG)"
            )
        print(f"Using kubeconfig file: {kubeconfig}")
        config.load_kube_config(kubeconfig)
    else:
        print("Using in-cluster configuration")
        config.load_incluster_config()

    # Parameters required from the user

    # A unique identifier for this candidate
    candidate_id = uuid.uuid4()
    # Name of the lock object to be created
    lock_name = "pykubeleader-example"  # TODO Change that!

    # Configure logging
    logging.basicConfig(
        format=f"{pod_name} %(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        force=True,
    )

    # Kubernetes namespace
    lock_namespace = "default"
    singleton = Singleton(pod_name)
    # Create config
    c = electionconfig.Config(
        ConfigMapLock(lock_name, lock_namespace, candidate_id),
        lease_duration=17,
        renew_deadline=15,
        retry_period=5,
        onstarted_leading=singleton.start,
        onstopped_leading=None,
    )

    # Enter leader election
    leaderelection.LeaderElection(c).run()

    # User can choose to do another round of election or simply exit
    logging.info("Exited leader election")


if __name__ == "__main__":
    main()
