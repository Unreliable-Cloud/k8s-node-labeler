# node-labeler

![Version: 0.0.8](https://img.shields.io/badge/Version-0.0.8-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: v01acc64](https://img.shields.io/badge/AppVersion-v01acc64-informational?style=flat-square)

A Helm chart for Kubernetes

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| apm.enabled | bool | `false` |  |
| fullnameOverride | string | `""` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"docker.io/youvegotmoxie/node-labeler"` |  |
| image.tag | string | `"v01acc64"` |  |
| imagePullSecrets[0].name | string | `"dockerhub-regcred"` |  |
| labelSelectors.SPOTS | string | `"cloud.google.com/gke-spot=true"` |  |
| labelSelectors.WORKERS | string | `"node-role.kubernetes.io/master!="` |  |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podAnnotations."ad.datadoghq.com/node-labeler.logs" | string | `"[{\"source\": \"docker\", \"service\": \"node-labeler\"}]"` |  |
| podLabels."tags.datadoghq.com/env" | string | `"prod"` |  |
| podLabels."tags.datadoghq.com/service" | string | `"node-labeler"` |  |
| podLabels.app | string | `"node-labeler"` |  |
| podSecurityContext | object | `{}` |  |
| replicaCount | int | `1` |  |
| resources.limits.cpu | string | `"100m"` |  |
| resources.limits.memory | string | `"128Mi"` |  |
| resources.requests.cpu | string | `"100m"` |  |
| resources.requests.memory | string | `"128Mi"` |  |
| securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| securityContext.readOnlyRootFilesystem | bool | `true` |  |
| securityContext.runAsNonRoot | bool | `true` |  |
| securityContext.runAsUser | int | `1000` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `"node-labeler"` |  |
| tolerations | list | `[]` |  |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.8.1](https://github.com/norwoodj/helm-docs/releases/v1.8.1)
