from vfd import *

#====================================================================
# Main
#====================================================================

def main():
    # Prepare VFD
    vfd_boot()
    vfd_init(VFD_CS0)
    vfd_init(VFD_CS1)
    vfd_init(VFD_CS2)
    vfd_text(VFD_CS0, b"HELLO")
    vfd_show(VFD_CS0)
    vfd_text(VFD_CS1, b"WORLD")
    vfd_show(VFD_CS1)
    vfd_text(VFD_CS2, b"RASPI")
    vfd_show(VFD_CS2)
    while True:
        sleep(0.5)

if __name__ == "__main__":
    main()
