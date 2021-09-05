module.exports = {
  reactStrictMode: true,
  async rewrites() {
    // https://nextjs.org/docs/api-reference/next.config.js/rewrites
    return [
      {
        source: '/api/:slug*',
        destination: `${(process.env.NODE_ENV = 'production'
          ? 'http://api.nftfactory.dev/:slug*'
          : 'https://localhost:5000')}/:slug*`
      }
    ];
  }
};
