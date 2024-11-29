from web3 import Web3
from mnemonic import Mnemonic
from bip32utils import BIP32Key

# Read seed phrase from a .txt file
def read_seed_phrase(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Generate the Ethereum address and balance using the seed phrase
def get_balance_from_seed_phrase(seed_phrase):
    # Initialize the Mnemonic object
    mnemo = Mnemonic("english")
    
    # Convert the seed phrase into a seed
    seed = mnemo.to_seed(seed_phrase, passphrase="")

    # Derive the private key using BIP32
    bip32_root_key = BIP32Key.fromEntropy(seed)
    bip32_child_key = bip32_root_key.ChildKey(0).ChildKey(0)  # Standard first address

    # Get private key, public key, and address
    private_key = bip32_child_key.WalletImportFormat()  # Private key in WIF format
    address = bip32_child_key.Address()  # Wallet address in Ethereum format

    # Initialize Web3 instance to connect to Ethereum network (using Infura or other provider)
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/4dff746b327742df89dccb374dcda88c'))

    # Convert the address to checksum format
    checksum_address = w3.toChecksumAddress(address)

    # Get the balance in Wei (Ethereum base unit)
    balance_wei = w3.eth.get_balance(checksum_address)

    # Convert balance from Wei to Ether
    balance_eth = w3.fromWei(balance_wei, 'ether')

    return checksum_address, balance_eth

# Main function to load the seed and check balance
def main():
    # Path to the .txt file containing the seed phrase
    seed_phrase_file = 'seed_phrase.txt'

    # Read the seed phrase from the file
    seed_phrase = read_seed_phrase(seed_phrase_file)
    
    # Get the wallet balance
    address, balance = get_balance_from_seed_phrase(seed_phrase)

    print(f"Wallet Address: {address}")
    print(f"Balance: {balance} ETH")

if __name__ == "__main__":
    main()
	
