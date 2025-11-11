

import argparse
from bip_utils import (
    Bip39MnemonicGenerator, Bip39SeedGenerator,
    Bip44, Bip44Coins, Bip44Changes,
    Bip84, Bip84Coins,
    Bip86, Bip86Coins
)


def coin_types(testnet: bool):
    if testnet:
        return Bip44Coins.BITCOIN_TESTNET, Bip84Coins.BITCOIN_TESTNET, Bip86Coins.BITCOIN_TESTNET
    return Bip44Coins.BITCOIN, Bip84Coins.BITCOIN, Bip86Coins.BITCOIN


def generate_addresses(mnemonic=None, acct_index=0, addr_start=0, count=1, testnet=False):
    if mnemonic is None:
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    bip44_coin, bip84_coin, bip86_coin = coin_types(testnet)

    results = {"mnemonic": mnemonic, "addresses": []}

    # Prebuild contexts once (correctly advance purpose/coin levels)
    bip44_ctx_base = Bip44.FromSeed(seed_bytes, bip44_coin).Purpose().Coin()
    bip84_ctx_base = Bip84.FromSeed(seed_bytes, bip84_coin).Purpose().Coin()
    bip86_ctx_base = Bip86.FromSeed(seed_bytes, bip86_coin).Purpose().Coin()

    for i in range(addr_start, addr_start + count):
        bip44_addr = bip44_ctx_base.Account(acct_index).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
        bip84_addr = bip84_ctx_base.Account(acct_index).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
        bip86_addr = bip86_ctx_base.Account(acct_index).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)

        results["addresses"].append({
            "index": i,
            "legacy": {
                "address": bip44_addr.PublicKey().ToAddress(),
                "pubkey_hex": bip44_addr.PublicKey().RawCompressed().ToHex(),
                "private_wif": bip44_addr.PrivateKey().ToWif()
            },
            "bech32": {
                "address": bip84_addr.PublicKey().ToAddress(),
                "pubkey_hex": bip84_addr.PublicKey().RawCompressed().ToHex(),
                "private_wif": bip84_addr.PrivateKey().ToWif()
            },
            "bech32m": {
                "address": bip86_addr.PublicKey().ToAddress(),
                "pubkey_hex": bip86_addr.PublicKey().RawCompressed().ToHex(),
                "private_wif": bip86_addr.PrivateKey().ToWif()
            }
        })

    return results


def main():
    p = argparse.ArgumentParser(description="Generate Bitcoin addresses (BIP44/BIP84/BIP86).")
    p.add_argument("--mnemonic", type=str, help="Provide a BIP39 mnemonic (12/18/24 words).")
    p.add_argument("--count", type=int, default=1, help="Number of address sets to generate (default 1).")
    p.add_argument("--start", type=int, default=0, help="Start index for address generation (default 0).")
    p.add_argument("--testnet", action="store_true", help="Generate testnet addresses instead of mainnet.")
    args = p.parse_args()

    data = generate_addresses(
        mnemonic=args.mnemonic,
        addr_start=args.start,
        count=args.count,
        testnet=args.testnet
    )

    print("====== MNEMONIC ======")
    print(data["mnemonic"])
    print("======================\n")

    for entry in data["addresses"]:
        idx = entry["index"]
        print(f"--- Address index {idx} ---")
        print("Legacy (P2PKH / BIP44):")
        for k, v in entry["legacy"].items():
            print(f"  {k}: {v}")
        print("\nBech32 (P2WPKH / BIP84):")
        for k, v in entry["bech32"].items():
            print(f"  {k}: {v}")
        print("\nBech32m (P2TR / BIP86):")
        for k, v in entry["bech32m"].items():
            print(f"  {k}: {v}")
        print("\n")

    print("NOTE: Do NOT use these keys/mnemonics with real funds unless you understand the risks.")
    print("Use --testnet to create addresses for Bitcoin testnet.")


if __name__ == "__main__":
    main()
