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
        main: '#ffffff',
        main2: '#ffffff',
        main3: '#ffffff',
        // primary:'#fffaff',
        // secondary: '#423E3B',
        // accent: '#ffffff',
      }
    },
    },
  plugins: [
  ]
}