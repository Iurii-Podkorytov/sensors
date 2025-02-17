import can
import struct 

def send_can_message():
    bus = can.Bus( 
        interface='slcan',
        channel='COM11',
        bitrate=1e6,
    )
    
    angle = struct.pack('<i', 3000)

    try:
        # Create the CAN message to send
        msg_to_send = can.Message(
            arbitration_id=0x141,
            data=[0x19, 0, 0, 0, 0, 0, 0],
            # data=[0xA3, 0, 0, 0, *angle],
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