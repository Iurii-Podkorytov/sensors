import can
import serial
import struct
import time

def sensor_to_angle(sensor, k=100.0, mechanical_factor=36000):
    """Convert sensor reading to motor angle units using virtual spring model."""
    force = sensor * (1023 / 98.1)
    displacement = force / k
    angle_units = int(displacement * mechanical_factor)
    return angle_units

def main():
    bus = can.Bus(interface='slcan', channel='COM11', bitrate=1e6)
    ser = serial.Serial('COM8', baudrate=115200, timeout=0.1)    
    try:
        motor_on_msg = can.Message(
            arbitration_id=0x141,
            data=[0x88, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            is_extended_id=False
        )
        bus.send(motor_on_msg)
        print("Motor powered ON.")
        
        # Virtual spring parameters
        SPRING_CONSTANT = 10.0  # N/m
        MECHANICAL_FACTOR = 1  # angle units per meter
        
        while True:
            raw_data = ser.readline().decode('utf-8', errors='replace').strip()
            if raw_data:
                try:
                    sensor = int(raw_data)
                    angle = sensor_to_angle(sensor, SPRING_CONSTANT, MECHANICAL_FACTOR)
                    angle_bytes = struct.pack('<i', angle*100)
                    can_data = [
                        0xA4,  # Command byte
                        0x00, 0xAA, 0x00,
                        *angle_bytes  # Unpack bytes into DATA[4]-DATA[7]
                    ]
                    msg = can.Message(
                        arbitration_id=0x141,
                        data=can_data,
                        is_extended_id=False
                    )
                    bus.send(msg)
                    print(f"Sensor: {sensor}, Angle: {angle}")
                except ValueError:
                    print(f"Invalid sensor data: {raw_data}")
                        
    except KeyboardInterrupt:
        print("\nUser interrupted.")
    finally:
        can.Message(
            arbitration_id=0x141,
            data=[0x81, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            is_extended_id=False
        )
        bus.shutdown()
        ser.close()

if __name__ == "__main__":
    main()