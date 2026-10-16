/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "sf-bg": "#05060a",
        "sf-accent": "#00f0ff",
        "sf-surface": "rgba(255,255,255,0.04)"
      },
      fontFamily: { sf: ["ui-sans-serif", "system-ui", "sans-serif"] }
    }
  },
  plugins: []
};