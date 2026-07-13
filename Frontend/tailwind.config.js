/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#14171A",
        muted: "#6B7178",
        surface: "#F4F5F2",
        line: "#E6E7E3",
        verified: {
          DEFAULT: "#2F5D50",
          soft: "#E7EEEC",
        },
        flagged: {
          DEFAULT: "#B5502F",
          soft: "#F6E9E4",
        },
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        body: ["IBM Plex Sans", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
      maxWidth: {
        app: "560px",
      },
    },
  },
  plugins: [],
};
