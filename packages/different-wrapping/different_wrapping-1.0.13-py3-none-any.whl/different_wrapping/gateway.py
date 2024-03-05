from different_wrapping.utils import docker_port_string_get_external_port

def generate_gateway(service_name, service, challenge, args):
    # First we need to determine the port that the ingress is supposed to be pointed towards
    if "ports" not in service.container_dict:
        raise RuntimeError(
            f"Tried to create gateway for {service_name} but it has no ports exposed(and therefore no k8s service to point to)"
        )

    external_ports = [
        docker_port_string_get_external_port(port) for port in service.container_dict["ports"]
    ]

    if len(external_ports) == 0:
        raise RuntimeError(
            f"Unable to create gateway for {service_name} as there are no ports"
        )
    elif len(external_ports) > 1:
        raise RuntimeError(
            f"Unable to determine external port for {service_name} as there are more than one ports exposed"
        )

    # Determine DNS name
    host = service.get_dns_name(args.dns_host)

    return {
        "apiVersion": "gateway.networking.k8s.io/v1",
        "kind": "HTTPRoute",
        "metadata": {
            "name": f"gateway-{challenge.safe_name()}-{service_name}",
        },
        "spec": {
            "parentRefs": {
                "name": args.gateway_parent_name,
                "namespace": args.gateway_parent_namespace,
                "sectionName": "https",
                "kind": "Gateway",
                "group": "gateway.networking.k8s.io"
            },
            "hostnames": [ host ],
            "rules": [
                {
                    "matches": [
                        {
                            "path": {
                                "type": "PathPrefix",
                                "value": "/"
                            }
                        }
                    ],
                    "backendRefs": [
                        {
                            "name": service_name,
                            "port": int(external_ports[0]),
                            "weight": 1,
                            "group": '',
                            "kind": "Service"
                        }
                    ]
                }
            ],
        },
    }
