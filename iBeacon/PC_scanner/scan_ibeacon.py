import asyncio
import csv
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Tuple

from bleak import BleakScanner

CSV_FILE = "ibeacon_log.csv"
SCAN_SECONDS = 60  # 0以下なら無限
PRINT_DUPLICATES = False  # Trueにすると毎回表示


@dataclass
class IBeaconRecord:
    address: str
    name: str
    rssi: int
    uuid: str
    major: int
    minor: int
    measured_power: int
    last_seen: datetime


def ensure_csv_header(filepath: str) -> None:
    if os.path.exists(filepath):
        return

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "address",
            "name",
            "rssi",
            "uuid",
            "major",
            "minor",
            "measured_power",
        ])


def append_csv(filepath: str, rec: IBeaconRecord) -> None:
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            rec.last_seen.isoformat(timespec="seconds"),
            rec.address,
            rec.name,
            rec.rssi,
            rec.uuid,
            rec.major,
            rec.minor,
            rec.measured_power,
        ])


def parse_ibeacon(company_id: int, payload: bytes) -> Optional[Tuple[str, int, int, int]]:
    """
    Windows/Bleakの manufacturer_data は
    dict[company_id, payload] のことが多いので、
    company_id=0x004C, payload=02 15 + UUID(16) + Major(2) + Minor(2) + TxPower(1)
    を想定してデコードする。
    """
    if company_id != 0x004C:
        return None

    if len(payload) < 23:
        return None

    if payload[0] != 0x02 or payload[1] != 0x15:
        return None

    uuid_bytes = payload[2:18]
    major = (payload[18] << 8) | payload[19]
    minor = (payload[20] << 8) | payload[21]
    measured_power = int.from_bytes(bytes([payload[22]]), byteorder="big", signed=True)

    uuid = (
        f"{uuid_bytes[0]:02X}{uuid_bytes[1]:02X}{uuid_bytes[2]:02X}{uuid_bytes[3]:02X}-"
        f"{uuid_bytes[4]:02X}{uuid_bytes[5]:02X}-"
        f"{uuid_bytes[6]:02X}{uuid_bytes[7]:02X}-"
        f"{uuid_bytes[8]:02X}{uuid_bytes[9]:02X}-"
        f"{uuid_bytes[10]:02X}{uuid_bytes[11]:02X}{uuid_bytes[12]:02X}"
        f"{uuid_bytes[13]:02X}{uuid_bytes[14]:02X}{uuid_bytes[15]:02X}"
    )

    return uuid, major, minor, measured_power


def make_key(address: str, uuid: str, major: int, minor: int) -> str:
    return f"{address}|{uuid}|{major}|{minor}"


seen: Dict[str, IBeaconRecord] = {}


def detection_callback(device, advertisement_data) -> None:
    name = device.name or advertisement_data.local_name or ""
    address = getattr(device, "address", "UNKNOWN")
    rssi = advertisement_data.rssi
    now = datetime.now()

    for company_id, payload in advertisement_data.manufacturer_data.items():
        parsed = parse_ibeacon(company_id, bytes(payload))
        if parsed is None:
            continue

        uuid, major, minor, measured_power = parsed
        key = make_key(address, uuid, major, minor)

        rec = IBeaconRecord(
            address=address,
            name=name,
            rssi=rssi,
            uuid=uuid,
            major=major,
            minor=minor,
            measured_power=measured_power,
            last_seen=now,
        )

        is_new = key not in seen
        seen[key] = rec

        if is_new or PRINT_DUPLICATES:
            label = "NEW " if is_new else "UPD "
            print(
                f"[{label}] {now.strftime('%H:%M:%S')} "
                f"ADDR={rec.address} RSSI={rec.rssi:4d} "
                f"UUID={rec.uuid} MAJOR={rec.major} MINOR={rec.minor} TX={rec.measured_power}"
            )
            if rec.name:
                print(f"      NAME={rec.name}")

            append_csv(CSV_FILE, rec)


async def main() -> None:
    ensure_csv_header(CSV_FILE)

    print("##################")
    print("iBeacon scan start")
    print("##################")
    print(f"CSV log: {os.path.abspath(CSV_FILE)}")
    if SCAN_SECONDS > 0:
        print(f"Scan duration: {SCAN_SECONDS} sec")
    else:
        print("Scan duration: infinite")

    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()

    try:
        if SCAN_SECONDS > 0:
            await asyncio.sleep(SCAN_SECONDS)
        else:
            while True:
                await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await scanner.stop()
        print("scan stopped")


if __name__ == "__main__":
    asyncio.run(main())