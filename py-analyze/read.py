import sys
import serial
import crtk

serialPort = serial.Serial(
    port="COM8", baudrate=2000000, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)

tri = crtk.Trigger()

i = 0
data = b""
while 1:
    # Wait until there is data in the in-buffer
    if serialPort.in_waiting > 0:
        ch = serialPort.read()
        if i == 0:
            if ch == b'\n':
                i = 1
            continue
        else:
            data += ch
            if len(data) < 8:
                continue
            elif len(data) == 8:
                pass
            else:
                data = b''
                continue

        # print(data)
        a = int.from_bytes(data[:2], "big")
        b = int.from_bytes(data[2:4], "big")
        ts = int.from_bytes(data[4:8], "big")
        # print(a, b, ts)

        try:
            print(a, ',', b, ',', ts)
            dur = tri.check(a, b, ts)
            if dur is not None:
                print("dur = {} ms, speed = {:.4f} km/h".format(dur/1000, 0.2 / (dur/1000_000) * 3.6), file=sys.stderr)
        except:
            pass
