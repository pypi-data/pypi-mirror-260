# pylint: disable=too-many-public-methods
from string import Template


class MessageEndpoints:
    # devices feedback
    _device_status = "internal/devices/status"
    _device_read = "internal/devices/read"
    _device_read_configuration = "internal/devices/read_configuration"
    _device_readback = "internal/devices/readback"
    _device_limits = "internal/devices/limits"
    _device_req_status = "internal/devices/req_status"
    _device_progress = "internal/devices/progress"
    _device_async_readback = Template("internal/devices/async_readback/$scanID/$device")

    # device config
    _device_config_request = "internal/devices/config_request"
    _device_config_request_response = "internal/devices/config_request_response"
    _device_server_config_update = "internal/devices/device_server_config_update"
    _device_config_update = "internal/devices/config_update"
    _device_config = "internal/devices/config"
    _device_config_history = "internal/devices/config_history"
    _device_info = "internal/devices/info"
    _device_staged = "internal/devices/staged"

    # device monitoring
    _device_monitor = "internal/devices/monitor"

    # scan queue
    _scan_queue_modification = "internal/queue/queue_modification"
    _scan_queue_modification_request = "internal/queue/queue_modification_request"
    _scan_queue_insert = "internal/queue/queue_insert"
    _scan_queue_request = "internal/queue/queue_request"
    _scan_queue_request_response = "internal/queue/queue_request_response"
    _scan_queue_status = "internal/queue/queue_status"
    _scan_queue_history = "internal/queue/queue_history"

    # scan info
    _scan_number = "scans/scan_number"
    _dataset_number = "scans/dataset_number"
    _scan_status = "scans/scan_status"
    _scan_status_list = "scans/scan_status_list"
    _available_scans = "scans/available_scans"
    _scan_segment = "scans/scan_segment"
    _scan_baseline = "scans/scan_baseline"
    _bluesky_events = "scans/bluesky-events"
    _public_scan_info = Template("public/$scanID/scan_info")
    _public_scan_segment = Template("public/$scanID/scan_segment/$pointID")
    _public_scan_baseline = Template("public/$scanID/scan_baseline")
    _public_file = Template("public/$scanID/file/$name")
    _file_event = "public/file_event"
    _file_content = "internal/file_content"

    # instructions
    _device_instructions = "internal/devices/instructions"
    _device_rpc = "internal/devices/rpc"
    _pre_scan_macros = "internal/pre_scan_macros"
    _post_scan_macros = "internal/post_scan_macros"

    # log
    _log = "internal/log"
    _alarms = "internal/alarms"

    # service
    _services_status = "internal/services/status"
    _metrics = "internal/services/metrics"
    _service_response = "internal/services/response"

    # misc
    _public_global_vars = "public/vars"
    _observer = "internal/observer"
    _progress = "public/progress"

    # logbook
    _logbook = "internal/logbook"

    # scibec
    _scibec = "internal/scibec"

    # experiment
    _account = "internal/account"

    # data processing
    _processed_data = "public/processed_data"
    _dap_config = "internal/dap/config"
    _available_dap_plugins = "internal/dap/available_plugins"
    _dap_request = "internal/dap/request"
    _dap_response = "internal/dap/response"

    # GUI
    _gui_config = "public/gui/config"
    _gui_data = "public/gui/data"
    _gui_instructions = "public/gui/instruction"
    _gui_instruction_response = "public/gui/instruction_response"

    ##########

    # devices feedback
    @classmethod
    def device_status(cls, device: str) -> str:
        """
        Endpoint for device status. This endpoint is used by the device server to publish
        the device status using a messages.DeviceStatusMessage message.

        Args:
            device (str): Device name, e.g. "samx".
        """
        return f"{cls._device_status}/{device}"

    @classmethod
    def device_read(cls, device: str) -> str:
        """
        Endpoint for device readings. This endpoint is used by the device server to publish
        the device readings using a messages.DeviceMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device readings of the specified device.
        """
        return f"{cls._device_read}/{device}"

    @classmethod
    def device_read_configuration(cls, device: str) -> str:
        """
        Endpoint for device configuration readings. This endpoint is used by the device server
        to publish the device configuration readings using a messages.DeviceMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device configuration readings of the specified device.
        """
        return f"{cls._device_read_configuration}/{device}"

    @classmethod
    def device_readback(cls, device: str) -> str:
        """
        Endpoint for device readbacks. This endpoint is used by the device server to publish
        the device readbacks using a messages.DeviceMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device readbacks of the specified device.
        """
        return f"{cls._device_readback}/{device}"

    @classmethod
    def device_limits(cls, device: str) -> str:
        """
        Endpoint for device limits. This endpoint is used by the device server to publish
        the device limits using a messages.DeviceMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device limits of the specified device.
        """
        return f"{cls._device_limits}/{device}"

    @classmethod
    def device_req_status(cls, device: str) -> str:
        """
        Endpoint for device request status. This endpoint is used by the device server to publish
        the device request status using a messages.DeviceReqStatusMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device request status of the specified device.
        """
        return f"{cls._device_req_status}/{device}"

    @classmethod
    def device_progress(cls, device: str) -> str:
        """
        Endpoint for device progress. This endpoint is used by the device server to publish
        the device progress using a messages.ProgressMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device progress of the specified device.
        """
        return f"{cls._device_progress}/{device}"

    # device config
    @classmethod
    def device_config_request(cls) -> str:
        """
        Endpoint for device config request. This endpoint can be used to
        request a modification to the device config. The request is sent using
        a messages.DeviceConfigMessage message.

        Returns:
            str: Endpoint for device config request.
        """
        return cls._device_config_request

    @classmethod
    def device_config_request_response(cls, RID: str) -> str:
        """
        Endpoint for device config request response. This endpoint is used by the
        device server and scihub connector to inform about whether the device config
        request was accepted or rejected. The response is sent using a
        messages.RequestResponseMessage message.

        Args:
            RID (str): Request ID.

        Returns:
            str: Endpoint for device config request response.
        """
        return f"{cls._device_config_request_response}/{RID}"

    @classmethod
    def device_server_config_request(cls) -> str:
        """
        Endpoint for device server config request. This endpoint can be used to
        request changes to config. Typically used by the scihub connector following a
        device config request and validate a new configuration with the device server.
        The request is sent using a messages.DeviceConfigMessage message.

        Returns:
            str: Endpoint for device server config request.
        """
        return cls._device_server_config_update

    @classmethod
    def device_config_update(cls) -> str:
        """
        Endpoint for device config update. This endpoint is used by the scihub connector
        to inform about a change to the device config. The update is sent using a
        messages.DeviceConfigMessage message.

        Returns:
            str: Endpoint for device config update.

        """
        return cls._device_config_update

    @classmethod
    def device_config(cls) -> str:
        """
        Endpoint for device config. This endpoint is used by the scihub connector
        to set the device config.

        Returns:
            str: Endpoint for device config.
        """
        return cls._device_config

    @classmethod
    def device_config_history(cls) -> str:
        """
        Endpoint for device config history. This endpoint is used to keep track of the
        device config history using a messages.AvailableResourceMessage message. The endpoint is
        connected to a redis list.

        Returns:
            str: Endpoint for device config history.
        """
        return cls._device_config_history

    @classmethod
    def device_info(cls, device: str) -> str:
        """
        Endpoint for device info. This endpoint is used by the device server to publish
        the device info using a messages.DeviceInfoMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device info of the specified device.
        """
        return f"{cls._device_info}/{device}"

    @classmethod
    def device_staged(cls, device: str) -> str:
        """
        Endpoint for the device stage status. This endpoint is used by the device server
        to publish the device stage status using a messages.DeviceStatusMessage message.
        A device is staged when it is ready to be used in a scan. A DeviceStatus of 1 means
        that the device is staged, 0 means that the device is not staged.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for the device stage status of the specified device.
        """
        return f"{cls._device_staged}/{device}"

    @classmethod
    def device_async_readback(cls, scanID: str, device: str) -> str:
        """
        Endpoint for receiving an async device readback over Redis streams.
        This endpoint is used by the device server to publish async device
        readbacks using a messages.DeviceMessage. In addition tp scan metadata,
        the message metadata contains information on how to concatenate multiple readings.
        Further keyword arguments for GUI handling might be attached.

        Args:
            scanID (str): unique scan identifier
            device (str): Device name, e.g. "mcs".

        Returns:
            str: Endpoint for the async device readback.
        """
        return cls._device_async_readback.substitute(scanID=scanID, device=device)

    @classmethod
    def device_monitor(cls, device: str) -> str:
        """
        Endpoint for device monitoring.
        This endpoint is used to publish image or wavefrom data from a monitor. An
        example can be a 2D area dertector or a 1D waveform (XRF), for which we
        forward a subset from the data to the monitoring endpoing for visualization
        purposes. Details on shape and type of data need to be specified in
        dtype/dshape of the dev.<device>.describe() method.
        #TODO: Add here information that it should be a RedisStream?

        Args:
            device (str): Device name, e.g. "eiger".

        Returns:
            str: Endpoint for device monitor of the specified device.
        """
        return f"{cls._device_monitor}/{device}"

    # scan queue
    @classmethod
    def scan_queue_modification(cls) -> str:
        """
        Endpoint for scan queue modification. This endpoint is used to publish accepted
        scan queue modifications using a messages.ScanQueueModificationMessage message.

        Returns:
            str: Endpoint for scan queue modification.
        """
        return cls._scan_queue_modification

    @classmethod
    def scan_queue_modification_request(cls) -> str:
        """
        Endpoint for scan queue modification request. This endpoint is used to request
        a scan queue modification using a messages.ScanQueueModificationMessage message.
        If accepted, the modification is published using the scan_queue_modification
        endpoint.

        Returns:
            str: Endpoint for scan queue modification request.
        """
        return cls._scan_queue_modification_request

    @classmethod
    def scan_queue_insert(cls) -> str:
        """
        Endpoint for scan queue inserts. This endpoint is used to publish accepted
        scans using a messages.ScanQueueMessage message.
        The message will be picked up by the scan queue manager and inserted into the
        scan queue.

        Returns:
            str: Endpoint for scan queue inserts.
        """
        return cls._scan_queue_insert

    @classmethod
    def scan_queue_request(cls) -> str:
        """
        Endpoint for scan queue request. This endpoint is used to request the new scans.
        The request is sent using a messages.ScanQueueMessage message.

        Returns:
            str: Endpoint for scan queue request.
        """
        return cls._scan_queue_request

    @classmethod
    def scan_queue_request_response(cls) -> str:
        """
        Endpoint for scan queue request response. This endpoint is used to publish the
        information on whether the scan request was accepted or rejected. The response
        is sent using a messages.RequestResponseMessage message.

        Returns:
            str: Endpoint for scan queue request response.

        """
        return cls._scan_queue_request_response

    @classmethod
    def scan_queue_status(cls) -> str:
        """
        Endpoint for scan queue status. This endpoint is used to publish the scan queue
        status using a messages.ScanQueueStatusMessage message.

        Returns:
            str: Endpoint for scan queue status.
        """
        return cls._scan_queue_status

    @classmethod
    def scan_queue_history(cls) -> str:
        """
        Endpoint for scan queue history. This endpoint is used to keep track of the
        scan queue history using a messages.ScanQueueHistoryMessage message. The endpoint is
        connected to a redis list.

        Returns:
            str: Endpoint for scan queue history.
        """
        return cls._scan_queue_history

    # scan info
    @classmethod
    def scan_number(cls) -> str:
        """
        Endpoint for scan number. This endpoint is used to publish the scan number. The
        scan number is incremented after each scan and set in redis as an integer.

        Returns:
            str: Endpoint for scan number.
        """
        return cls._scan_number

    @classmethod
    def dataset_number(cls) -> str:
        """
        Endpoint for dataset number. This endpoint is used to publish the dataset number.
        The dataset number is incremented after each dataset and set in redis as an integer.

        Returns:
            str: Endpoint for dataset number.
        """
        return cls._dataset_number

    @classmethod
    def scan_status(cls) -> str:
        """
        Endpoint for scan status. This endpoint is used to publish the scan status using
        a messages.ScanStatusMessage message.

        Returns:
            str: Endpoint for scan status.
        """
        return cls._scan_status

    @classmethod
    def available_scans(cls) -> str:
        """
        Endpoint for available scans. This endpoint is used to publish the available scans
        using a direct msgpack dump of a dictionary containing the available scans.

        #TODO: Change this to a messages.AvailableScans message.

        Returns:
            str: Endpoint for available scans.
        """
        return cls._available_scans

    @classmethod
    def bluesky_events(cls) -> str:
        """
        Endpoint for bluesky events. This endpoint is used by the scan bundler to
        publish the bluesky events using a direct msgpack dump of the bluesky event.

        Returns:
            str: Endpoint for bluesky events.
        """
        return cls._bluesky_events

    @classmethod
    def scan_segment(cls) -> str:
        """
        Endpoint for scan segment. This endpoint is used by the scan bundler to publish
        the scan segment using a messages.ScanMessage message.

        Returns:
            str: Endpoint for scan segments.
        """
        return cls._scan_segment

    @classmethod
    def scan_baseline(cls) -> str:
        """
        Endpoint for scan baseline readings. This endpoint is used by the scan bundler to
        publish the scan baseline readings using a messages.ScanBaselineMessage message.

        Returns:
            str: Endpoint for scan baseline readings.
        """
        return cls._scan_baseline

    # instructions
    @classmethod
    def device_instructions(cls) -> str:
        """
        Endpoint for device instructions. This endpoint is used by the scan server to
        publish the device instructions using a messages.DeviceInstructionMessage message.
        The device instructions are used to instruct the device server to perform
        certain actions, e.g. to move a motor.

        Returns:
            str: Endpoint for device instructions.
        """
        return cls._device_instructions

    @classmethod
    def device_rpc(cls, rpc_id: str) -> str:
        """
        Endpoint for device rpc. This endpoint is used by the device server to publish
        the result of a device rpc using a messages.DeviceRPCMessage message.

        Args:
            rpc_id (str): RPC ID.

        Returns:
            str: Endpoint for device rpc.
        """
        return f"{cls._device_rpc}/{rpc_id}"

    @classmethod
    def pre_scan_macros(cls) -> str:
        """
        Endpoint for pre scan macros. This endpoint is used to keep track of the pre scan
        macros. The endpoint is connected to a redis list.

        Returns:
            str: Endpoint for pre scan macros.
        """
        return cls._pre_scan_macros

    @classmethod
    def post_scan_macros(cls) -> str:
        """
        Endpoint for post scan macros. This endpoint is used to keep track of the post scan
        macros. The endpoint is connected to a redis list.

        Returns:
            str: Endpoint for post scan macros.
        """
        return cls._post_scan_macros

    @classmethod
    def public_scan_info(cls, scanID: str) -> str:
        """
        Endpoint for scan info. This endpoint is used by the scan worker to publish the
        scan info using a messages.ScanStatusMessage message. In contrast to the scan_info endpoint,
        this endpoint is specific to a scan and has a retentioni time of 30 minutes.

        Args:
            scanID (str): Scan ID.

        Returns:
            str: Endpoint for scan info.

        """
        return cls._public_scan_info.substitute(scanID=scanID)

    @classmethod
    def public_scan_segment(cls, scanID: str, pointID: int) -> str:
        """
        Endpoint for public scan segments. This endpoint is used by the scan bundler to
        publish the scan segment using a messages.ScanMessage message. In contrast to the
        scan_segment endpoint, this endpoint is specific to a scan and has a retention time
        of 30 minutes.

        Args:
            scanID (str): Scan ID.
            pointID (int): Point ID to specify a single point in a scan.

        Returns:
            str: Endpoint for scan segments.

        """
        return cls._public_scan_segment.substitute(scanID=scanID, pointID=pointID)

    @classmethod
    def public_scan_baseline(cls, scanID: str) -> str:
        """
        Endpoint for public scan baseline readings. This endpoint is used by the scan bundler
        to publish the scan baseline readings using a messages.ScanBaselineMessage message.
        In contrast to the scan_baseline endpoint, this endpoint is specific to a scan and has
        a retention time of 30 minutes.

        Args:
            scanID (str): Scan ID.

        Returns:
            str: Endpoint for scan baseline readings.
        """
        return cls._public_scan_baseline.substitute(scanID=scanID)

    @classmethod
    def public_file(cls, scanID: str, name: str) -> str:
        """
        Endpoint for public file. This endpoint is used by the file writer to publish the
        status of the file writing using a messages.FileMessage message.

        Args:
            scanID (str): Scan ID.
            name (str): File name.

        Returns:
            str: Endpoint for public files.
        """
        return cls._public_file.substitute(scanID=scanID, name=name)

    @classmethod
    def file_event(cls, name: str) -> str:
        """
        Endpoint for public file_event. This endpoint is used by the file writer to publish the
        status of the file writing using a messages.FileMessage message.

        Args:
            name (str): File name.

        Returns:
            str: Endpoint for public file_events.
        """
        return f"{cls._file_event}/{name}"

    @classmethod
    def file_content(cls) -> str:
        """
        Endpoint for file content. This endpoint is used by the file writer to publish the
        file content using a messages.FileContentMessage message.

        Returns:
            str: Endpoint for file content.
        """
        return cls._file_content

    # log
    @classmethod
    def log(cls) -> str:
        """
        Endpoint for log. This endpoint is used by the redis connector to publish logs using
        a messages.LogMessage message.

        Returns:
            str: Endpoint for log.
        """
        return cls._log

    @classmethod
    def alarm(cls) -> str:
        """
        Endpoint for alarms. This endpoint is used by the redis connector to publish alarms
        using a messages.AlarmMessage message.

        Returns:
            str: Endpoint for alarms.
        """
        return cls._alarms

    # service
    @classmethod
    def service_status(cls, service_id: str) -> str:
        """
        Endpoint for service status. This endpoint is used by all BEC services to publish
        their status using a messages.StatusMessage message.
        The status message also contains the service info such as user, host, etc.

        Args:
            service_id (str): Service ID, typically a uuid4 string.
        """
        return f"{cls._services_status}/{service_id}"

    @classmethod
    def metrics(cls, service_id: str) -> str:
        """
        Endpoint for metrics. This endpoint is used by all BEC services to publish their
        performance metrics using a messages.ServiceMetricMessage message.

        Args:
            service_id (str): Service ID, typically a uuid4 string.

        Returns:
            str: Endpoint for metrics.
        """
        return f"{cls._metrics}/{service_id}"

    @classmethod
    def service_response(cls, RID: str) -> str:
        """
        Endpoint for service response. This endpoint is used by all BEC services to publish
        the result of a service request using a messages.ServiceResponseMessage message.

        Args:
            RID (str): Request ID.

        Returns:
            str: Endpoint for service response.
        """
        return f"{cls._service_response}/{RID}"

    # misc
    @classmethod
    def global_vars(cls, var_name: str) -> str:
        """
        Endpoint for global variables. This endpoint is used to publish global variables
        using a messages.VariableMessage message.

        Args:
            var_name (str): Variable name.

        Returns:
            str: Endpoint for global variables.
        """
        return f"{cls._public_global_vars}/{var_name}"

    @classmethod
    def observer(cls) -> str:
        """
        Endpoint for observer. This endpoint is used to keep track of observer states using a.
        messages.ObserverMessage message. This endpoint is currently not used.

        Returns:
            str: Endpoint for observer.
        """
        return cls._observer

    @classmethod
    def progress(cls, var_name) -> str:
        """
        Endpoint for progress. This endpoint is used to publish the current progress
        using a messages.ProgressMessage message.

        Args:
            var_name (str): Variable name.

        Returns:
            str: Endpoint for progress.
        """
        return f"{cls._progress}/{var_name}"

    # logbook
    @classmethod
    def logbook(cls) -> str:
        """
        Endpoint for logbook. This endpoint is used to publish logbook info such as
        url, user and token using a direct msgpack dump of a dictionary.

        Returns:
            str: Endpoint for logbook.
        """
        return cls._logbook

    # scibec
    @classmethod
    def scibec(cls) -> str:
        """
        Endpoint for scibec. This endpoint is used to publish scibec info such as
        url, user and token using a direct msgpack dump of a dictionary.

        Returns:
            str: Endpoint for scibec.
        """
        return cls._scibec

    # experiment
    @classmethod
    def account(cls) -> str:
        """
        Endpoint for account. This endpoint is used to publish the current account.
        The value is set directly as a string.
        """
        return cls._account

    # data processing
    @classmethod
    def processed_data(cls, process_id: str) -> str:
        """
        Endpoint for processed data. This endpoint is used to publish new processed data
        streams using a messages.ProcessedDataMessage message.

        Args:
            process_id (str): Process ID, typically a uuid4 string.

        Returns:
            str: Endpoint for processed data.
        """
        return f"{cls._processed_data}/{process_id}"

    @classmethod
    def dap_config(cls) -> str:
        """
        Endpoint for DAP configuration. This endpoint is used to publish the DAP configuration
        using a messages.DAPConfigMessage message.

        Returns:
            str: Endpoint for DAP configuration.
        """
        return cls._dap_config

    @classmethod
    def dap_available_plugins(cls, plugin_id: str) -> str:
        """
        Endpoint for available DAP plugins. This endpoint is used to publish the available DAP
        plugins using a messages.AvailableResourceMessage message.

        Args:
            plugin_id (str): Plugin ID.

        Returns:
            str: Endpoint for available DAP plugins.
        """
        return f"{cls._available_dap_plugins}/{plugin_id}"

    @classmethod
    def dap_request(cls) -> str:
        """
        Endpoint for DAP request. This endpoint is used to request a DAP using a
        messages.DAPRequestMessage message.

        Returns:
            str: Endpoint for DAP request.
        """
        return cls._dap_request

    @classmethod
    def dap_response(cls, RID: str) -> str:
        """
        Endpoint for DAP response. This endpoint is used to publish the DAP response using a
        messages.DAPResponseMessage message.

        Args:
            RID (str): Request ID.

        Returns:
            str: Endpoint for DAP response.
        """
        return f"{cls._dap_response}/{RID}"

    # GUI
    @classmethod
    def gui_config(cls, gui_id: str) -> str:
        """
        Endpoint for GUI configuration. This endpoint is used to publish the GUI configuration
        using a messages.GUIConfigMessage message.

        Returns:
            str: Endpoint for GUI configuration.
        """
        return f"{cls._gui_config}/{gui_id}"

    @classmethod
    def gui_data(cls, gui_id: str) -> str:
        """
        Endpoint for GUI data. This endpoint is used to publish the GUI data using a
        messages.GUIDataMessage message.

        Returns:
            str: Endpoint for GUI data.
        """
        return f"{cls._gui_data}/{gui_id}"

    @classmethod
    def gui_instructions(cls, gui_id: str) -> str:
        """
        Endpoint for GUI instructions. This endpoint is used to publish the GUI instructions
        using a messages.GUIInstructionMessage message.

        Returns:
            str: Endpoint for GUI instructions.
        """
        return f"{cls._gui_instructions}/{gui_id}"

    @classmethod
    def gui_instruction_response(cls, RID: str) -> str:
        """
        Endpoint for GUI instruction response. This endpoint is used to publish the GUI instruction response
        using a messages.RequestResponseMessage message.

        Returns:
            str: Endpoint for GUI instruction response.
        """
        return f"{cls._gui_instruction_response}/{RID}"
