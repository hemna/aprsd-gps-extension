import logging
import threading

from aprsd.utils import objectstore
from oslo_config import cfg

CONF = cfg.CONF
LOG = logging.getLogger("APRSD")


class GPSSettingsStore(objectstore.ObjectStoreMixin):
    """Persist GPS beacon settings across restarts.

    Stores user-modified beacon settings (from the webchat UI) to disk
    as JSON. On startup, persisted settings take precedence over CONF
    values. If no persisted settings exist, CONF values are used.

    Saved to: {CONF.save_location}/gpssettingsstore.json
    """

    _instance = None
    data: dict = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.lock = threading.RLock()
            cls._instance.data = {}
        return cls._instance

    def get(self, key, default=None):
        """Get a persisted setting, or return default if not set."""
        with self.lock:
            return self.data.get(key, default)

    def set(self, key, value):
        """Set a setting and persist to disk."""
        with self.lock:
            self.data[key] = value
        self.save()

    def update_from_message(self, message):
        """Update all settings from a beaconing_settings_changed message."""
        with self.lock:
            self.data["beacon_type"] = message.get("beacon_type")
            self.data["beacon_interval"] = message.get("beacon_interval")
            self.data["smart_beacon_distance_threshold"] = message.get(
                "smart_beacon_distance_threshold",
            )
            self.data["smart_beacon_time_window"] = message.get(
                "smart_beacon_time_window",
            )
        self.save()
        LOG.info(f"GPS settings persisted: {self.data}")
