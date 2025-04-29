from web3 import Web3
import json

# Connect to the local Ganache network
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Ensure the connection is successful
if not w3.is_connected():
    print("Error: Unable to connect to Ganache")
    exit()

# Set the account and private key
account = w3.eth.accounts[0]
private_key = "0x7d08ff8254b45f9f145db01b0320e3464070f0f56637d78bf0fcd95bf9735708"  # Example, replace with your own private key

# Derive the address from the private key
derived_account = w3.eth.account.from_key(private_key).address

# Contract ABI and address (replace with your contract's ABI and address)
contract_address = "0x4f335cde8829d9dbc54af5ae246150d597522998"
contract_address = Web3.to_checksum_address(contract_address)

# ABI for the deployed contract
contract_abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "fips", "type": "uint256"},
            {"internalType": "uint256", "name": "areaOfLand", "type": "uint256"},
            {"internalType": "uint256", "name": "sumInsuredPerAcre", "type": "uint256"},
            {"internalType": "uint256", "name": "premiumRate", "type": "uint256"},
            {"internalType": "address", "name": "farmer", "type": "address"}
        ],
        "name": "addInsurance",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "fips", "type": "uint256"}],
        "name": "disperseInsurance",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Initialize the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def add_insurance(fips_code, area_of_land, sum_insured_per_acre, premium_rate, account, nonce):
    # Estimate gas for adding insurance
    estimated_gas = contract.functions.addInsurance(
        fips_code, area_of_land, sum_insured_per_acre, premium_rate, account
    ).estimate_gas({'from': account})
    print(f"Estimated Gas: {estimated_gas}")

    # Build the transaction
    tx = contract.functions.addInsurance(
        fips_code, area_of_land, sum_insured_per_acre, premium_rate, account
    ).build_transaction({
        'from': account,
        'gas': estimated_gas,
        'gasPrice': w3.to_wei('20', 'gwei'),
        'nonce': nonce
    })

    # Sign the transaction with the private key
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Add Insurance Tx Hash: {tx_hash.hex()}")
    return tx_hash

def process_eligibility_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Fixed value for sum insured per acre
    sum_insured_per_acre = 1000  # Fixed value for all records
    premium_rate = 10  # Example premium rate, you can adjust as needed

    # Initialize nonce
    nonce = w3.eth.get_transaction_count(derived_account)
    
    for record in data:
        if record['insurance_eligible'] == 1:
            fips_code = record['fips']
            area_of_land = record['areaofland']

            # Calculate premium and dispersal amounts
            premium_amount = area_of_land * sum_insured_per_acre * premium_rate / 100
            dispersal_amount = premium_amount + (area_of_land * sum_insured_per_acre * 10)  # Adding 10% buffer

            print(f"FIPS Code: {fips_code}")
            print(f"Area of Land: {area_of_land} acres")
            print(f"Premium Amount: {premium_amount} currency units")
            print(f"Calculated Dispersal Amount: {dispersal_amount} currency units")

            try:
                # Add insurance to the contract
                add_insurance_tx_hash = add_insurance(fips_code, area_of_land, sum_insured_per_acre, premium_rate, derived_account, nonce)
                nonce += 1  # Increment nonce after each transaction

                # Build the dispersal transaction
                disperse_tx = contract.functions.disperseInsurance(fips_code).build_transaction({
                    'from': derived_account,
                    'gas': 200000,
                    'gasPrice': w3.to_wei('20', 'gwei'),
                    'nonce': nonce
                })
                signed_disperse_tx = w3.eth.account.sign_transaction(disperse_tx, private_key)
                
                # Send the dispersal transaction
                disperse_tx_hash = w3.eth.send_raw_transaction(signed_disperse_tx.raw_transaction)
                print(f"Dispersal Tx Hash: {disperse_tx_hash.hex()}")
                nonce += 1  # Increment nonce after the second transaction

            except Exception as e:
                print(f"An error occurred: {e}")

            print("-" * 50)

# Path to the JSON file
file_path = r"C:\Users\leela\Desktop\implementation\EligibilityContract_data_updated.json"
process_eligibility_data(file_path)
