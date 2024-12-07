const webpack = require('webpack');

module.exports = {
  webpack: {
    configure: {
      resolve: {
        fallback: {
          "util": require.resolve("util/"),
          "buffer": require.resolve("buffer/"),
          "stream": false,
          "crypto": false,
          "http": false,
          "https": false,
          "os": false,
          "url": false,
        }
      }
    },
    plugins: {
      add: [
        new webpack.ProvidePlugin({
          process: 'process/browser',
          Buffer: ['buffer', 'Buffer'],
        }),
      ]
    }
  }
}; 