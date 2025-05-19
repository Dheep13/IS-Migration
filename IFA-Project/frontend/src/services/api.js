import api from "../utils/api"

// Use relative URL to leverage Vite's proxy
const API_URL = '/api'

// Add this test function to check connectivity with proper error handling
export const testBackendConnection = async () => {
    try {
        console.log("Testing connection to backend at:", API_URL)

        // Use our axios instance which has the proper baseURL configuration
        const response = await api.get("/health")

        console.log("Backend connection test successful:", response.status)
        return true
    } catch (error) {
        console.error("Backend connection test failed:", error)

        // Try a direct fetch with mode: 'no-cors' as a fallback
        try {
            console.log("Attempting fallback connection test...")
            const response = await fetch(`${API_URL}/health`, {
                method: "GET",
                mode: "no-cors" // This will prevent CORS errors but won't give us response data
            })

            // With 'no-cors', we can't check status, but at least we didn't get a network error
            console.log("Fallback connection completed without network errors")
            return true
        } catch (fallbackError) {
            console.error("Fallback connection test failed:", fallbackError)
            return false
        }
    }
}

// Modify generateDocs to use axios
export const generateDocs = async (formData, signal) => {
    try {
        console.log("Sending request to generate documentation")

        const config = {
            headers: {
                "Content-Type": "multipart/form-data"
            },
            signal
        }

        const response = await api.post("/generate-docs", formData, config)
        console.log("Response received:", response.data)
        return response.data
    } catch (error) {
        console.error("Error generating docs:", error)
        throw error
    }
}

// Update getJobStatus to use axios
export const getJobStatus = async jobId => {
    try {
        const response = await api.get(`/jobs/${jobId}`)
        return response.data
    } catch (error) {
        console.error("Error getting job status:", error)
        throw error
    }
}

// Update getAllJobs to use axios
export const getAllJobs = async () => {
    try {
        const response = await api.get("/jobs")
        return response.data
    } catch (error) {
        console.error("Error getting all jobs:", error)
        throw error
    }
}

// Update getDocumentation to use axios with responseType blob
export const getDocumentation = async (jobId, fileType) => {
    try {
        const response = await api.get(`/docs/${jobId}/${fileType}`, {
            responseType: "blob"
        })
        return response.data
    } catch (error) {
        console.error("Error getting documentation:", error)
        throw error
    }
}

// Generate iFlow match for a job
export const generateIflowMatch = async jobId => {
    try {
        console.log(`Generating iFlow match for job: ${jobId}`)
        // Fix: Remove the duplicate '/api' prefix since it's already in the baseURL
        const response = await api.post(`/generate-iflow-match/${jobId}`)
        console.log("iFlow match generation response:", response.data)
        return response.data
    } catch (error) {
        console.error("Error generating iFlow match:", error)
        // Add more detailed error logging
        if (error.response) {
            console.error("Response error data:", error.response.data)
            console.error("Response error status:", error.response.status)
        } else if (error.request) {
            console.error("No response received:", error.request)
        } else {
            console.error("Error message:", error.message)
        }
        throw error
    }
}

// Get iFlow match status
export const getIflowMatchStatus = async jobId => {
    try {
        console.log(`Getting iFlow match status for job: ${jobId}`)
        // Fix: Remove the duplicate '/api' prefix since it's already in the baseURL
        const response = await api.get(`/iflow-match/${jobId}`)
        console.log("iFlow match status response:", response.data)
        return response.data
    } catch (error) {
        console.error("Error getting iFlow match status:", error)
        // Add more detailed error logging
        if (error.response) {
            console.error("Response error data:", error.response.data)
            console.error("Response error status:", error.response.status)
        } else if (error.request) {
            console.error("No response received:", error.request)
        } else {
            console.error("Error message:", error.message)
        }
        throw error
    }
}

// Get iFlow match file
export const getIflowMatchFile = async (jobId, fileType) => {
    try {
        console.log(`Getting iFlow match file for job: ${jobId}, file type: ${fileType}`)
        // Fix: Remove the duplicate '/api' prefix since it's already in the baseURL
        const response = await api.get(`/iflow-match/${jobId}/${fileType}`, {
            responseType: "blob"
        })
        console.log(`iFlow match file response received, size: ${response.data.size} bytes`)
        return response.data
    } catch (error) {
        console.error("Error getting iFlow match file:", error)
        // Add more detailed error logging
        if (error.response) {
            console.error("Response error data:", error.response.data)
            console.error("Response error status:", error.response.status)
        } else if (error.request) {
            console.error("No response received:", error.request)
        } else {
            console.error("Error message:", error.message)
        }
        throw error
    }
}

// Create a dedicated API instance for the iFlow API
import axios from 'axios'

// Get environment variables
const ENV = import.meta.env.VITE_ENVIRONMENT || 'development';
const IFLOW_API_URL = import.meta.env.VITE_IFLOW_API_URL || 'http://localhost:5001/api';
const IFLOW_API_HOST = import.meta.env.VITE_IFLOW_API_HOST || 'localhost:5001';
const IFLOW_API_PROTOCOL = import.meta.env.VITE_IFLOW_API_PROTOCOL || 'http';
const MAX_POLL_COUNT = parseInt(import.meta.env.VITE_MAX_POLL_COUNT || '60');
const POLL_INTERVAL_MS = parseInt(import.meta.env.VITE_POLL_INTERVAL_MS || '2000');
const MAX_FAILED_ATTEMPTS = parseInt(import.meta.env.VITE_MAX_FAILED_ATTEMPTS || '3');

console.log(`Environment: ${ENV}`);
console.log('Using iFlow API URL:', IFLOW_API_URL);
console.log('Using iFlow API Host:', IFLOW_API_HOST);
console.log('Using iFlow API Protocol:', IFLOW_API_PROTOCOL);
console.log('Max Poll Count:', MAX_POLL_COUNT);
console.log('Poll Interval (ms):', POLL_INTERVAL_MS);
console.log('Max Failed Attempts:', MAX_FAILED_ATTEMPTS);

// Create a separate instance for the iFlow API
const iflowApi = axios.create({
  baseURL: IFLOW_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Set withCredentials based on environment
  // In production, we need to set this to true for Cloud Foundry
  withCredentials: ENV === 'production',
})

// Add request interceptor for debugging
iflowApi.interceptors.request.use(
  (config) => {
    console.log(`iFlow API Request to: ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('iFlow API Request Error:', error);
    return Promise.reject(error);
  }
)

// Add response interceptor for debugging
iflowApi.interceptors.response.use(
  (response) => {
    console.log(`iFlow API Response from: ${response.config.url}`, response.status);
    return response;
  },
  (error) => {
    if (error.response) {
      console.error('iFlow API Error Response:', error.response.status, error.response.data);
    } else if (error.request) {
      console.error('iFlow API No Response Error:', error.request);
    } else {
      console.error('iFlow API Request Setup Error:', error.message);
    }
    return Promise.reject(error);
  }
)

// Helper function to try the markdown approach for iFlow generation
async function tryMarkdownApproach(jobId) {
    console.log(`Fetching markdown content for job: ${jobId}`);
    const markdownBlob = await getDocumentation(jobId, 'markdown');
    const markdownContent = await markdownBlob.text();
    console.log(`Markdown content fetched, length: ${markdownContent.length} characters`);

    // Now send the markdown content directly to the iFlow API
    const response = await iflowApi.post(`/generate-iflow`, {
        markdown: markdownContent,
        iflow_name: `IFlow_${jobId.substring(0, 8)}`
    }, {
        timeout: 30000 // 30 second timeout
    });

    console.log("iFlow generation response:", response.data);
    return response.data;
}

// Generate iFlow from markdown
export const generateIflow = async (jobId) => {
    try {
        console.log(`Generating iFlow for job: ${jobId}`);
        console.log(`Environment: ${ENV}`);

        // Use a consistent approach for both development and production
        // First try the markdown approach, then fall back to direct approach if needed
        try {
            console.log("Trying markdown approach first...");

            // Add a health check first to verify the API is accessible
            try {
                console.log("Checking iFlow API health first...");
                const healthResponse = await iflowApi.get('/health');
                console.log("iFlow API health check response:", healthResponse.data);
            } catch (healthError) {
                console.error("iFlow API health check failed:", healthError);
                console.log("Continuing with iFlow generation despite health check failure");
            }

            // Try the markdown approach
            return await tryMarkdownApproach(jobId);
        } catch (markdownError) {
            console.error("Markdown approach failed:", markdownError);

            if (markdownError.response) {
                console.error("Response status:", markdownError.response.status);
                console.error("Response data:", markdownError.response.data);
            } else if (markdownError.request) {
                console.error("No response received from server");
            } else {
                console.error("Error message:", markdownError.message);
            }

            // If markdown approach fails, try the direct approach
            console.log("Trying direct iFlow generation with job ID...");

            // Log the full URL being used
            const fullUrl = `${iflowApi.defaults.baseURL}/generate-iflow/${jobId}`;
            console.log(`Calling iFlow API directly with job ID: ${jobId}`);
            console.log(`Full URL: ${fullUrl}`);

            // Log the baseURL to verify it's correct
            console.log(`iFlow API baseURL: ${iflowApi.defaults.baseURL}`);

            const directResponse = await iflowApi.post(`/generate-iflow/${jobId}`, {}, {
                timeout: 30000 // 30 second timeout
            });

            console.log("Direct iFlow generation response:", directResponse.data);
            return directResponse.data;
        }
    } catch (error) {
        console.error("Error generating iFlow:", error);

        // Add more detailed error logging
        if (error.response) {
            console.error("Response error data:", error.response.data)
            console.error("Response error status:", error.response.status)
            return {
                status: 'error',
                message: `Error: ${error.response.status} - ${error.response.data?.error || error.response.data?.message || 'Unknown error'}`,
                error: error.response.data
            };
        } else if (error.request) {
            console.error("No response received:", error.request)
            return {
                status: 'error',
                message: 'Error: Could not connect to the iFlow API server. Please make sure it is running.',
                error: 'CONNECTION_ERROR'
            };
        } else {
            console.error("Error message:", error.message)
            return {
                status: 'error',
                message: `Error: ${error.message}`,
                error: 'UNKNOWN_ERROR'
            };
        }
    }
}

// Get iFlow generation status
export const getIflowGenerationStatus = async (jobId) => {
    try {
        console.log(`Getting iFlow generation status for job: ${jobId}`);

        // Add a timeout to the request to prevent hanging
        const response = await iflowApi.get(`/jobs/${jobId}`, {
            timeout: 10000 // 10 second timeout
        });

        console.log("iFlow generation status response:", response.data);
        return response.data;
    } catch (error) {
        console.error("Error getting iFlow generation status:", error)
        // Add more detailed error logging
        if (error.response) {
            console.error("Response error data:", error.response.data)
            console.error("Response error status:", error.response.status)
            // Return a formatted error object instead of throwing
            return {
                status: 'error',
                message: `Error: ${error.response.status} - ${error.response.data?.error || 'Unknown error'}`,
                error: error.response.data
            };
        } else if (error.request) {
            console.error("No response received:", error.request)
            // Return a formatted error object for connection issues
            return {
                status: 'error',
                message: 'Error: Could not connect to the iFlow API server. Please make sure it is running.',
                error: 'CONNECTION_ERROR'
            };
        } else {
            console.error("Error message:", error.message)
            // Return a formatted error object for other errors
            return {
                status: 'error',
                message: `Error: ${error.message}`,
                error: 'UNKNOWN_ERROR'
            };
        }
    }
}

// Download generated iFlow
export const downloadGeneratedIflow = async (jobId) => {
    try {
        console.log(`Downloading generated iFlow for job: ${jobId}`);

        // Use the dedicated iflowApi instance with blob response type
        const response = await iflowApi.get(`/jobs/${jobId}/download`, {
            responseType: 'blob'
        });

        console.log(`Downloaded iFlow blob, size: ${response.data.size} bytes`);
        return response.data;
    } catch (error) {
        console.error("Error downloading generated iFlow:", error)
        // Add more detailed error logging
        if (error.response) {
            console.error("Response error data:", error.response.data)
            console.error("Response error status:", error.response.status)
        } else if (error.request) {
            console.error("No response received:", error.request)
        } else {
            console.error("Error message:", error.message)
        }
        throw error
    }
}

// Download iFlow debug file
export const downloadIflowDebugFile = async (jobId, fileName) => {
    try {
        console.log(`Downloading iFlow debug file for job: ${jobId}, file: ${fileName}`);

        // Use the dedicated iflowApi instance with blob response type
        const response = await iflowApi.get(`/jobs/${jobId}/debug/${fileName}`, {
            responseType: 'blob'
        });

        console.log(`Downloaded iFlow debug file blob, size: ${response.data.size} bytes`);
        return response.data;
    } catch (error) {
        console.error("Error downloading iFlow debug file:", error)
        // Add more detailed error logging
        if (error.response) {
            console.error("Response error data:", error.response.data)
            console.error("Response error status:", error.response.status)
        } else if (error.request) {
            console.error("No response received:", error.request)
        } else {
            console.error("Error message:", error.message)
        }
        throw error
    }
}

// Deploy iFlow to SAP Integration Suite
export const deployIflowToSap = async (jobId, packageId, description) => {
    try {
        console.log(`Deploying iFlow for job: ${jobId} to SAP Integration Suite`);

        // Use the dedicated iflowApi instance
        const response = await iflowApi.post(`/jobs/${jobId}/deploy`, {
            package_id: packageId,
            description: description
        });

        console.log("iFlow deployment response:", response.data);
        return response.data;
    } catch (error) {
        console.error("Error deploying iFlow to SAP:", error)
        // Add more detailed error logging
        if (error.response) {
            console.error("Response error data:", error.response.data)
            console.error("Response error status:", error.response.status)
        } else if (error.request) {
            console.error("No response received:", error.request)
        } else {
            console.error("Error message:", error.message)
        }
        throw error
    }
}
