/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/templates/*.{html, js}'
  ],
  theme: {
    extend: {
      colors: {
        primary:'#f3eef3',
        secondary: '#423E3B',
        accent: '#ffffff',
        main: '#30d2ff',
        maintwo: '#43ff59',
        mainthree: '#ff5757',
        lightSecondary: '#4f4b49',
        tertiary: '#f9f9f9',
        // primary:'#fffaff',
        // secondary: '#423E3B',
        // accent: '#ffffff',
      }
    },
    },
    
  plugins: [
    require('@tailwindcss/typography'),
  ]
}