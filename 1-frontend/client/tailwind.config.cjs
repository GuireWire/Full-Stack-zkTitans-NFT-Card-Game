/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        siteblack: '#131519',
        siteDimBlack: '#191d23',
        siteOrange: '#FF8C00',
        siteWhite: '#9eacc7',
      },
      backgroundImage: {
        jungle: "url('/src/assets/background/jungle-battleground.jpg')",
        volcano: "url('/src/assets/background/volcano-battleground.jpg')",
        wasteland: "url('/src/assets/background/wasteland-battleground.jpg')",
        swamp: "url('/src/assets/background/swamp-battleground.jpg')",
        underwater: "url('/src/assets/background/underwater-battleground.jpg')",
        space: "url('/src/assets/background/space-battleground.jpg')",
        heroImg: "url('/src/assets/background/hero-img.jpg')",
        landing: "url('/src/assets/background/landing.jpg')",
      },
      fontFamily: {
        crash: ['Crash-A-Like', 'sans-serif'],
        rajdhani: ['Rajdhani', 'sans-serif'],
        baloo: ['"Baloo Bhaina 2"', 'cursive'],
        chau: ['"Chau Philomene One"', 'sans-serif'],
      },
    },
  },
  plugins: [require('tailwind-scrollbar')],
};