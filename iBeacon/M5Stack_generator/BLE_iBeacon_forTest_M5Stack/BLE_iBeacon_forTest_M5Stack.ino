/*
   iBeacon example
   - No custom GATT service / characteristic
   - Only advertising as iBeacon
*/
#include <M5Unified.h>

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEBeacon.h>

#define MAJOR_ID (5)
#define MINOR_ID (88)

#define DEVICE_NAME      "M5STACK"
#define BEACON_UUID  "A134D0B2-1DA2-1BA7-C94C-E8E00C9F7A2D"

static BLEAdvertising *g_pAdvertising = nullptr;

void init_ibeacon()
{
  BLEBeacon myBeacon;
  BLEAdvertisementData advertisementData;

  if (g_pAdvertising == nullptr)
  {
    return;
  }

  g_pAdvertising->stop();

  // iBeacon parameters
  myBeacon.setManufacturerId(0x4c00);                 // Apple Company ID
  myBeacon.setMajor(MAJOR_ID);                               // Major ID
  myBeacon.setMinor(MINOR_ID);                              // Minor ID
  myBeacon.setSignalPower(0xc5);                      // Measured Power (-59 dBm 相当)
  myBeacon.setProximityUUID(BLEUUID(BEACON_UUID));

  advertisementData.setFlags(0x1A);
  advertisementData.setManufacturerData(myBeacon.getData());

  g_pAdvertising->setAdvertisementData(advertisementData);

  // 任意: advertising interval
  g_pAdvertising->setMinInterval(160); // 160 * 0.625ms = 100ms
  g_pAdvertising->setMaxInterval(200); // 200 * 0.625ms = 125ms
}

void setup()
{
  M5.begin();
  M5.Lcd.fillScreen(TFT_WHITE);

  Serial.begin(115200);
  Serial.println();
  Serial.println("Initializing iBeacon only...");
  Serial.flush();

  BLEDevice::init(DEVICE_NAME);

  // GATT server は作らず、Advertising だけ使う
  g_pAdvertising = BLEDevice::getAdvertising();

  init_ibeacon();

  Serial.println("Please press A button to start iBeacon...");
  Serial.println("Major ID = 5, Minor ID = 88");

  M5.Lcd.setCursor(10, 10);
  M5.Lcd.setTextColor(BLACK);
  M5.Lcd.setTextSize(3);
  M5.Lcd.print("Please press A button\nto start iBeacon...\n");
}

void loop()
{
  if (M5.BtnA.wasPressed())
  {
    if (g_pAdvertising != nullptr)
    {
      g_pAdvertising->start();
    }

    M5.Display.clear();
    M5.Display.fillScreen(TFT_BLUE);
    M5.Display.setCursor(10, 10);
    M5.Display.setTextColor(YELLOW);
    M5.Display.setTextSize(3);
    M5.Display.print("Start iBeacon.\n");
    M5.Display.print("interval=100-125ms\n");
    M5.Display.print("Major ID=5\n");
    M5.Display.print("Minor ID=88\n");

    Serial.println("Start iBeacon! interval=100-125ms Major,Minor ID=5,88");
  }

  if (M5.BtnB.wasPressed())
  {
    if (g_pAdvertising != nullptr)
    {
      g_pAdvertising->stop();
    }

    M5.Display.clear();
    M5.Display.fillScreen(TFT_WHITE);
    M5.Display.setCursor(10, 10);
    M5.Display.setTextColor(BLACK);
    M5.Display.setTextSize(3);
    M5.Display.print("Stop iBeacon.\n");

    Serial.println("Stop iBeacon.");
  }

  delay(30);
  M5.update();
}