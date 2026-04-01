class IperfJob:
    def __init__(self, udp, download, duration, bandwidth=None, save=True):
        self.udp = udp
        self.download = download
        self.duration = duration
        self.bandwidth = bandwidth
        self.save = save

    def __repr__(self):
        proto = "UDP" if self.udp else "TCP"
        direction = "DL" if self.download else "UP"
        return f"<IperfJob {direction}-{proto}>"