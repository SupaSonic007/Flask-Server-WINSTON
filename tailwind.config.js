/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/templates/*.{html, js}'
  ],
  theme: {
    extend: {
      colors: {
        primary:'#fffaff',
        secondary: '#423E3B',
        accent: '#ffffff',
        main: '#30d2ff',
        maintwo: '#43ff59',
        mainthree: '#ff5757',
        // primary:'#fffaff',
        // secondary: '#423E3B',
        // accent: '#ffffff',
      }
    },
    },
  plugins: [
  ]
}