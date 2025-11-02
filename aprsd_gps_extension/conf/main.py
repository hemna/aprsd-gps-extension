from oslo_config import cfg

extension_group = cfg.OptGroup(
    name="aprsd_gps_extension",
    title="APRSD gps extension settings",
)

extension_opts = [
    cfg.BoolOpt(
        "enabled",
        default=True,
        help="Enable the extension?",
    ),
    cfg.StrOpt(
        "gpsd_host",
        default="localhost",
        help="GPSD host to connect to. Ensure gpsd is running and listening on this host.",
    ),
    cfg.IntOpt(
        "gpsd_port",
        default=2947,
        help="GPSD port to connect to",
    ),
    cfg.IntOpt(
        "polling period",
        default=10,
        help="Polling period in seconds to get the GPS data",
    ),
    cfg.BoolOpt(
        "debug",
        default=False,
        help="Enable debug logging",
    ),
    cfg.BoolOpt(
        "enable_smart_beacon",
        default=False,
        help="Enable the smart beacon feature. If this is disabled, the beacon will be sent every"
        "CONF.beacon_interval seconds. When enabled, the beacon will be sent only if the"
        "device has moved a certain distance or time since the last beacon was sent.",
    ),
    cfg.IntOpt(
        "smart_beacon_distance_threshold",
        default=100,
        help="The distance in feet that the device must move before sending a beacon packet,"
        "when smart beaconing is enabled.",
    ),
    cfg.IntOpt(
        "smart_beacon_time_window",
        default=10,
        help="The time window in minutes that the device must be at the same position before sending a beacon packet, when smart beaconing is enabled.",
    ),
]

ALL_OPTS = extension_opts


def register_opts(cfg):
    cfg.register_group(extension_group)
    cfg.register_opts(ALL_OPTS, group=extension_group)


def list_opts():
    return {
        extension_group.name: extension_opts,
    }
