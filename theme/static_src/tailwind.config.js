module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    light: '#6b7280', // Customize the light shade
                    DEFAULT: '#1f2937', // Customize the default shade
                    dark: '#111827', // Customize the dark shade
                },
                secondary: {
                    light: '#f3e8ff', // Example light shade
                    DEFAULT: '#9d4edd', // Example default shade
                    dark: '#3c096c', // Example dark shade
                },
                // Add more custom colors as needed
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
