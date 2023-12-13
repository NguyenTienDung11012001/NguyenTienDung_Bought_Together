'use strict'
const {VueLoaderPlugin} = require('vue-loader')
const path = require('path');
const webpack = require('webpack')

module.exports = (env) => {
    let mode = env.NODE_ENV
    return {
        mode: mode,
        entry: {
            index: {
                import: './app.js',
            },
            shopify_frontend: {
                import: './front_end.js',
            },
            test: {
                import: './test.js'
            },
        },
        output: {
            path: path.resolve(__dirname, '../static/js'),
            filename: '[name].js'
        },
        module: {
            rules: [
                {
                    test: /\.vue$/,
                    use: 'vue-loader'
                },
                {
                    test: /\.css$/,
                    use: [
                        'vue-style-loader',
                        'css-loader',

                    ]
                },
                {
                    test: /\.js$/,
                    exclude: [/node_modules/],
                    use: [{
                        loader: 'babel-loader',
                        options: {plugins: ['transform-vue-jsx']}
                    }]
                },
                {}
            ]
        },
        plugins: [
            new VueLoaderPlugin(),
            new webpack.DefinePlugin({
                __VUE_OPTIONS_API__: true,
                __VUE_PROD_DEVTOOLS__: false,
            }),
        ]
    };
};

