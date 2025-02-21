import can
import struct 

def send_can_message():
    bus = can.Bus( 
        interface='slcan',
        channel='COM6',
        bitrate=1e6,
    )
    
    control_bytes = struct.pack('<i', 90*100)

    try:
        # Create the CAN message to send
        msg_to_send = can.Message(
            arbitration_id=0x141,
            # data=[0x81, 0, 0, 0, 0, 0, 0, 0],
            # data=[0xA2, 0, 0, 0, *control_bytes],
            data=[0xA3, 0, 0, 0, *control_bytes],
            # data=[0x34, 0, 0, 0, *control_bytes],
            # data=[0x33, 0, 0, 0, 0, 0, 0, 0],
            is_extended_id=False
        )
        
        # Send the message
        bus.send(msg_to_send)
        print(f"Message sent successfully on {bus.channel_info}")

        # Wait for a response (blocking call)
        print("Waiting for response...")
        response = bus.recv(timeout=1.0)

        if response is not None:
            print(f"Received response: ID={response.arbitration_id}, Data={response.data}")
        else:
            print("No response received within the timeout period.")

    except can.CanError as e:
        print(f"Error sending or receiving message: {e}")
    
    finally:
        bus.shutdown()

if __name__ == "__main__":
    send_can_message()