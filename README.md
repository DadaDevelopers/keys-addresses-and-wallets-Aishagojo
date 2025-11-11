# Assignment 2: Bitcoin Address Generation

## Overview

This project demonstrates how to generate Bitcoin addresses using different address formats and standards (BIP44, BIP84, BIP86) with Python. The script allows you to create multiple Bitcoin addresses for both mainnet and testnet, using either a randomly generated or user-supplied BIP39 mnemonic.

## Features

- Generates addresses in three formats:
  - **Legacy (P2PKH / BIP44)**
  - **Bech32 (P2WPKH / BIP84)**
  - **Bech32m (P2TR / BIP86)**
- Supports both Bitcoin mainnet and testnet.
- Allows custom mnemonic input or generates a new one.
- Outputs public addresses, public keys, and private keys (WIF format).
- Can generate multiple addresses at once and save output to a file.

## Usage

### 1. Set up the environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install bip-utils