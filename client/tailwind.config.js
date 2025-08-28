/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Orbitron', 'sans-serif'],
      },
      colors: {
        'cream': '#FFF7F0',
        'coral': '#FF6F61',
        'mint': '#6BFFB8',
        'lavender': '#A491D3',
        'charcoal': '#2D2D2D',
        'slate-light': '#4A4A4A',
      }
    },
  },
  plugins: [],
}