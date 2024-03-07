class IOConfig:
    _config = {
        "SPB100": {"in": 4, "out": 4, "ai": 0xA2, "ao": 0x91},
        "SPB110": {"in": 4, "out": 4, "ai": 0xA2, "ao": 0x91},
        "SPB400": {"in": 8, "out": 8, "ai": 0x82, "ao": 0x89},
        "SPB410": {"in": 8, "out": 8, "ai": 0x82, "ao": 0x89},
        "PowerTwin Pi5-6300U": {"in": 8, "out": 8, "ai": 0x82, "ao": 0x89}  # TODO: DMI Name
    }

    def __init__(self, config: dict):
        self.input_count = config["in"]
        self.output_count = config["out"]
        self.addr_di = config["ai"]
        self.addr_do = config["ao"]

    @classmethod
    def from_model_name(cls, name: str):
        return cls(cls._config[name])

    @classmethod
    def from_dmi(cls):
        with open("/sys/class/dmi/id/product_family", "r") as f:
            family = f.read().strip()
        with open("/sys/class/dmi/id/product_name", "r") as f:
            name = f.read().strip()

        if family not in ("PowerBox", "PowerTwin"):
            raise ValueError(f"Device not supported ({family})")

        if name not in cls._config.keys():
            raise ValueError(f"Device not supported ({family}/{name})")

        return cls(cls._config[name])
