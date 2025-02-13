import usb
import json
import fibre.protocol
from fibre.usbbulk_transport import USBBulkTransport
from fibre.utils import Logger

# Create logger
logger = Logger(verbose=False)

# Find all devices with specified vendor and product IDs
devices = usb.core.find(find_all=True, idVendor=0x1209, idProduct=0x0d32)

# Create dictionary to store devices by serial number
sn_to_device_dict = {}
for device in devices:
    sn_to_device_dict[device.serial_number] = device
print(sn_to_device_dict)
# Store json data for each device
sn_to_json_data = {}

# Get json data for each device
for serial_number, device in sn_to_device_dict.items():
    # Reset and configure device
    device.reset()
    device.set_configuration()
    
    # Create transport layer
    bulk_device = USBBulkTransport(device, logger)
    bulk_device.init()
    
    # Create channel
    channel = fibre.protocol.Channel(
        "USB device bus {} device {}".format(device.bus, device.address),
        bulk_device, bulk_device, None, logger
    )
    
    # Get and parse json data
    json_bytes = channel.remote_endpoint_read_buffer(0)
    json_string = json_bytes.decode("ascii")
    json_data = json.loads(json_string)
    
    # Store in dictionary
    sn_to_json_data[serial_number] = json_data
# Save to file
with open('sn_to_json_data.json', 'w') as f:
    json.dump(sn_to_json_data, f)