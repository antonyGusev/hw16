import pytest
from bleak import BleakClient, BleakScanner

from config import LED_CHAR_UUID

BLE_DEVICE_NAME = 'SENTRY-BLE'


@pytest.mark.asyncio
async def test_ble_led_dual_channel(device):
  ble_target = await BleakScanner.find_device_by_name(
    BLE_DEVICE_NAME,
    timeout=10,
  )
  
  assert ble_target is not None, (
    f'BLE device {BLE_DEVICE_NAME!r} was not found'
  )

  async with BleakClient(ble_target) as client:
    assert client.is_connected, 'Failed to connect to BLE device'

    await client.write_gatt_char(
      LED_CHAR_UUID,
      b'\x01',
      response=True,
    )
    
    led_on_log = device.wait_for_log('LED ON!', timeout=5)    
    assert any('LED ON!' in line for line in led_on_log), (
      'LED ON! was not found in UART log'
    )
    
    await client.write_gatt_char(
      LED_CHAR_UUID,
      b'\x00',
      response=True,
    )

    led_off_log = device.wait_for_log('LED OFF!', timeout=5)    
    assert any('LED OFF!' in line for line in led_off_log), (
      'LED OFF! was not found in UART log'
    )
    