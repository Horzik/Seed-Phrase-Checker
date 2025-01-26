import os
import time
import requests
import argparse
from itertools import islice
from bip_utils import Bip39SeedGenerator, Bip32Secp256k1, Secp256k1PublicKey
from bip_utils.addr import P2PKHAddrEncoder
from bip_utils import Bip44Conf
from config import SEEDS, VALID_ADDS, ACTIVE_ADDS, FAILED_ADDS, START

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SEEDS_PATH = os.path.join(DATA_DIR, SEEDS)
VALID_ADDS_PATH = os.path.join(DATA_DIR, VALID_ADDS)
ACTIVE_ADDS_PATH = os.path.join(DATA_DIR, ACTIVE_ADDS)
FAILED_ADDS_PATH = os.path.join(DATA_DIR, FAILED_ADDS)


def check_seed_phrase(seed_phrase):
    try:
        # Generate seed from mnemonic phrase
        seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
        # Create BIP32 context from seed
        bip32_ctx = Bip32Secp256k1.FromSeed(seed_bytes)
        # Derive the child key with index 0
        child_key = bip32_ctx.ChildKey(0)
        # Get public key in bytes
        public_key_raw = bytes(child_key.PublicKey().RawCompressed())
        pub_key_bytes = Secp256k1PublicKey.FromBytes(public_key_raw)
        # Generate P2PKH address
        addr = P2PKHAddrEncoder.EncodeKey(pub_key_bytes, **Bip44Conf.BitcoinMainNet.AddrParams())
        return addr

    except Exception:
        return None


# max_retries = number of tries for one address, delay = delay between each retry
def check_address_activity(address, max_retries=3, delay=2):
    url = f"https://blockstream.info/api/address/{address}/txs"
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return "active" if len(response.json()) > 0 else "inactive"
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"[{address}] Failed after {max_retries} attempts: \n {e}")
                return "failed"
            time.sleep(delay * (attempt + 1))
    return False


def argparserism():
    parser = argparse.ArgumentParser(description="Options for Czecking")
    parser.add_argument(
        "--address",
        "-a",
        action="store_true",
        help="Check addresses"
    )
    return parser.parse_args()


def main():
    args = argparserism()
    start_timer = time.time()
    all_adds = 0
    valid_adds = 0
    active_adds = 0
    failed_adds = 0

    # Helper Function For Logging
    def log_summary():
        end_timer = time.time()
        elapsed = end_timer - start_timer
        print(f"Checked {all_adds} seed phrases")
        print(f"Found {valid_adds} valid and {active_adds} active addresses")
        print(f"The search took {elapsed:.2f} seconds")
        print(f"{failed_adds} failed to be checked")
        exit(0)

    # Helper Function For Continuing The Czeck
    def last_line_check():
        addies.seek(0)
        start_line = START
        last_address = None
        for line in addies:
            last_address = line
        print(last_address)
        if last_address:
            conf = input("Continue the search? (y/n): ")
            if conf.lower() == 'y':
                last_address_line = int(last_address.split("(Line: ")[1].split(")")[0])
                start_line = last_address_line + 1
                print(f"Continuing the search from line {start_line}")
        return start_line

    # Main Main Block
    try:
        with open(SEEDS_PATH, 'r') as seeds, \
                open(VALID_ADDS_PATH, 'a+') as addies, \
                open(ACTIVE_ADDS_PATH, 'a') as active, \
                open(FAILED_ADDS_PATH, "a") as failed:

            start = last_line_check()
            for line_number, input_data in enumerate(islice(seeds, start - 1, None), start=start):
                all_adds += 1
                input_data = input_data.strip()

                if args.address:
                    address = input_data
                else:
                    address = check_seed_phrase(input_data)

                if address:
                    addies.write(f"{address} (Line: {line_number})\n")
                    valid_adds += 1
                    print(f"Derived address: {address}")
                    status = check_address_activity(address)
                    if status == "active":
                        print(f"Active wallet found: {address}")
                        active_adds += 1
                        active.write(f"{address} (Line: {line_number})\n")
                    elif status == "failed":
                        failed_adds += 1
                        failed.write(f"{address} (Line: {line_number})\n")
                    else:
                        print(f"No activity: {address}")

        print("Finished the search")
        log_summary()

    except KeyboardInterrupt:
        print("/// Shutting down")
        log_summary()


if __name__ == "__main__":
    main()
