const path = require('path');

module.exports = {
  devtool: 'eval-cheap-module-source-map',
  entry: {
    main: __dirname + '/dev/index.js'
  },
  output: {
    path: __dirname + '/public',
    filename: 'index.js',
    publicPath: '/public/'
  },
  module: {
    rules: [{
      test: /\.(js)$/,
      exclude: /(node_modules|bower_components)/,
      use: {
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env']
        }
      }
    }]
  },
  resolve: {
    extensions: ['*', '.js']
  },
  devServer: {
    contentBase: path.resolve(__dirname, './public'),
  }
}