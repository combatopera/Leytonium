from lagoon import sudo

def main_readjust():
    'Set system clock to correct time.'
    sudo.service.ntp.stop.print()
    sudo.ntpd._gq.print()
    sudo.service.ntp.start.print()
