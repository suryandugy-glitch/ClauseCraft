module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        accent: 'var(--accent)',
        'accent-dark': 'var(--accent-dark)',
        card: 'var(--bg-card)',
        error: 'var(--error)',
        muted: 'var(--text-muted)',
        primary: 'var(--text-primary)',
      },
    },
  },
};
