import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import * as path from 'path';

const SERVER_PATH = 'http://localhost:5000/'
const IFLOW_SERVER_PATH = 'http://localhost:5001/'

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
            '/auth': {
                target: SERVER_PATH,
                changeOrigin: true,
                secure: false
            },
            '/attachments': {
                target: SERVER_PATH,
                changeOrigin: true,
                secure: false
            },
            '/api/generate-docs': {
                target: SERVER_PATH,
                changeOrigin: true,
                secure: false
            },
            // Main route for jobs - this will handle all job requests to the main API
            '/api/jobs': {
                target: SERVER_PATH,
                changeOrigin: true,
                secure: false
            },
            '/api/docs': {
                target: SERVER_PATH,
                changeOrigin: true,
                secure: false
            },
            // This route is no longer needed since we're using direct URLs
            // '/api/generate-iflow': {
            //     target: IFLOW_SERVER_PATH,
            //     changeOrigin: true,
            //     secure: false
            // },
            '/api/generate-iflow-match': {
                target: SERVER_PATH,  // This should go to port 5000
                changeOrigin: true,
                secure: false
            },
            '/api/iflow-match': {
                target: SERVER_PATH,
                changeOrigin: true,
                secure: false
            },
            '/api': {
                target: SERVER_PATH,
                changeOrigin: true,
                secure: false
            }
        }
    }
})
