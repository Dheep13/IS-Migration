import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import * as path from 'path';

const SERVER_PATH = 'http://localhost:5009/'

export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            '@pages': path.join(__dirname, 'src/pages'),
            '@layouts': path.join(__dirname, 'src/layouts'),
            '@assets': path.join(__dirname, 'src/assets'),
            '@styles': path.join(__dirname, 'src/styles'),
            '@components': path.join(__dirname, 'src/components'),
            '@contexts': path.join(__dirname, 'src/contexts'),
            '@hooks': path.join(__dirname, 'src/hooks'),
            '@services': path.join(__dirname, 'src/services'),
            '@utils': path.join(__dirname, 'src/utils'),
            '@': path.join(__dirname, 'src'),
        },
    },
    server: {
        proxy: {
            '/auth': {target: SERVER_PATH},
            '/attachments': {target: SERVER_PATH},
            '/api': {target: SERVER_PATH},
        }
    }
})
