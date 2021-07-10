import gpiozero as gz
from time import sleep

# https://pinout.xyz/
# https://pinout.xyz/pinout/spi
VFD_RST_PIN     = 5  # physical 29
VFD_MOSI_PIN    = 20 # physical 38
VFD_SCLK_PIN    = 21 # physical 40
VFD_CS0_PIN     = 18 # physical 12
VFD_CS1_PIN     = 17 # physical 11
VFD_CS2_PIN     = 16 # physical 36

VFD_RST     = gz.DigitalOutputDevice(pin = VFD_RST_PIN, active_high = False)
VFD_MOSI    = gz.DigitalOutputDevice(pin = VFD_MOSI_PIN)
VFD_SCLK    = gz.DigitalOutputDevice(pin = VFD_SCLK_PIN, active_high = False)
VFD_CS0     = gz.DigitalOutputDevice(pin = VFD_CS0_PIN, active_high = False)
VFD_CS1     = gz.DigitalOutputDevice(pin = VFD_CS1_PIN, active_high = False)
VFD_CS2     = gz.DigitalOutputDevice(pin = VFD_CS2_PIN, active_high = False)

VFD_CSs = [VFD_CS0, VFD_CS1, VFD_CS2]

def vfd_reset():
    VFD_RST.on()
    sleep(0.1)
    VFD_RST.off()
    sleep(0.1)

def vfd_boot():
    vfd_reset()

def _vfd_transfer_bit(x):
    VFD_SCLK.on()
    if x == 0:
        VFD_MOSI.off() 
    else:
        VFD_MOSI.on()
    #sleep(0.0000001)
    VFD_SCLK.off()
    #sleep(0.0000001)

def _vfd_transfer_byte(x):
    for _ in range(8):
        _vfd_transfer_bit(x & 0x01)
        x = x >> 1

def vfd_send_bytes(cs, cmd, data):
    cs.on()
    #sleep(0.000001)
    _vfd_transfer_byte(cmd)
    for x in data:
        _vfd_transfer_byte(x)
    cs.off()
    #sleep(0.000001)

def vfd_init(cs):
    # set display timing
    vfd_send_bytes(cs, 0xE0, [0x07])
    # set diming data
    vfd_send_bytes(cs, 0xE4, [0xFF])

def vfd_write_dcram(cs, addr, data):
    cmd = 0x20 | (addr & 0x1F)
    vfd_send_bytes(cs, cmd, data)

def vfd_write_cgram(cs, addr, data):
    cmd = 0x40 | (addr & 0x07)
    vfd_send_bytes(cs, cmd, data)

def vfd_show(cs):
    vfd_send_bytes(cs, 0xE8, [])

def vfd_text(cs, s):
    vfd_write_dcram(cs, 0, s)
