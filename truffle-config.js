module.exports = {
  networks: {
    // Configuration for the local development network using Ganache
    development: {
      host: "127.0.0.1",     // Localhost for Ganache
      port: 8545,            // Standard Ethereum port used by Ganache
      network_id: "*",       // Any network ID (Ganache uses a random network ID)
    },

    // Configuration for Goerli test network (Example for public network)
    goerli: {
      provider: () => new HDWalletProvider(
        process.env.MNEMONIC,
        `https://goerli.infura.io/v3/${process.env.PROJECT_ID}`
      ),
      network_id: 5,          // Goerli's network ID
      confirmations: 2,       // Wait for 2 block confirmations
      timeoutBlocks: 200,     // Wait up to 200 blocks before timeout
      skipDryRun: true        // Skip dry run before migrations
    },

    // Additional network example for a private Ethereum network
    private: {
      provider: () => new HDWalletProvider(
        process.env.MNEMONIC,
        `https://your-private-network-url`
      ),
      network_id: 2111,       // Custom network ID
      production: true        // Treat as public network
    }
  },

  // Mocha testing framework configuration
  mocha: {
    timeout: 100000           // Increased timeout for slow tests
  },

  // Solidity compiler configuration
  compilers: {
    solc: {
      version: "0.8.21",       // Specify Solidity compiler version
      settings: {
        optimizer: {
          enabled: true,       // Enable optimization
          runs: 200            // Set optimization runs
        },
        evmVersion: "london"   // EVM version
      }
    }
  },

  // Truffle DB configuration (Optional)
  db: {
    enabled: false             // Disable Truffle DB by default
  }
};
