class DataHandler:
    @staticmethod
    def set_template(
        serverless,
        template_name,
        container_image,
        model_name,
        max_model_length,
        container_disk,
        volume_disk,
        volume_mount_path="",
        ports="",
        container_cmd="",
        readme="",
    ):
        data = {
            "query": f"""mutation {{
                saveTemplate(input: {{
                    containerDiskInGb: {container_disk},
                    dockerArgs: "{container_cmd}",
                    env: [
                        {{ key: "MODEL_NAME", value: "{model_name}" }},
                        {{ key: "MAX_MODEL_LENGTH", value: "{max_model_length}" }}
                    ],
                    imageName: "{container_image}",
                    isServerless: {serverless},
                    name: "{template_name}",
                    ports: "{ports}",
                    readme: "{readme}",
                    volumeInGb: {volume_disk},
                    volumeMountPath: "{volume_mount_path}"
                }}) {{
                    containerDiskInGb
                    dockerArgs
                    env {{
                        key
                        value
                    }}
                    id
                    imageName
                    name
                    ports
                    readme
                    volumeInGb
                    volumeMountPath
                }}
            }}"""
        }
        return data

    @staticmethod
    def create_serverless_endpoint(
        gpu_ids,
        idle_timeout,
        name,
        scaler_type,
        scaler_value,
        template_id,
        workers_max,
        workers_min,
        locations="",
        network_volume_id="",
    ):
        data = {
            "query": f"""mutation {{
            saveEndpoint(input: {{
                gpuIds: "{gpu_ids}",
                idleTimeout: {idle_timeout},
                locations: "{locations}",
                name: "{name}",
                networkVolumeId: "{network_volume_id}",
                scalerType: "{scaler_type}",
                scalerValue: {scaler_value},
                templateId: "{template_id}",
                workersMax: {workers_max},
                workersMin: {workers_min}
            }}) {{
                gpuIds
                id
                idleTimeout
                locations
                name
                scalerType
                scalerValue
                templateId
                workersMax
                workersMin
            }}
        }}"""
        }

        return data

    @staticmethod
    def check_endpoint():
        data = {
            "query": """
            query Endpoints {
                myself {
                    endpoints {
                        gpuIds
                        id
                        idleTimeout
                        locations
                        name
                        networkVolumeId
                        pods {
                            desiredStatus
                            id
                            lastStatusChange
                        }
                        scalerType
                        scalerValue
                        templateId
                        workersMax
                        workersMin
                    }
                    serverlessDiscount {
                        discountFactor
                        type
                        expirationDate
                    }
                }
            }
            """
        }

        return data
