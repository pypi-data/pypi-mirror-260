/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        'cerebri': ['Cerebri Sans'],
        "cerebribold": ['Cerebri Sans bold'],
        "cerebriregular": ['Cerebri Sans regular'],
        "cerebrisemibold": ['Cerebri Sans semibold'],
      },
    },
    screens: {
      xxl: { max: "1700px" },
      xl: { max: "1350px" },
      lg: { max: "1024px" },
      md: { max: "768px" },
      sm: { max: "640px" },
      xs: { max: "500px" },
      xxs: { max: "400px" },
    },
  },
  plugins: [],
};
