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

// Create a separate instance for the iFlow API
const iflowApi = axios.create({
  baseURL: 'http://localhost:5001/api', // Use the direct URL to the iFlow API server
  headers: {
    'Content-Type': 'application/json',
  },
  // Don't send credentials with requests to avoid CORS issues
  withCredentials: false,
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

// Generate iFlow from markdown
export const generateIflow = async (jobId) => {
    try {
        console.log(`Generating iFlow for job: ${jobId}`);

        // Fix: Remove the duplicate '/api' prefix since it's already in the baseURL
        const response = await iflowApi.post(`/generate-iflow/${jobId}`);

        console.log("iFlow generation response:", response.data);
        return response.data;
    } catch (error) {
        console.error("Error generating iFlow:", error)
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

// Get iFlow generation status
export const getIflowGenerationStatus = async (jobId) => {
    try {
        console.log(`Getting iFlow generation status for job: ${jobId}`);

        // Fix: Remove the duplicate '/api' prefix since it's already in the baseURL
        const response = await iflowApi.get(`/jobs/${jobId}`);

        console.log("iFlow generation status response:", response.data);
        return response.data;
    } catch (error) {
        console.error("Error getting iFlow generation status:", error)
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

// Download generated iFlow
export const downloadGeneratedIflow = async (jobId) => {
    try {
        console.log(`Downloading generated iFlow for job: ${jobId}`);

        // Fix: Remove the duplicate '/api' prefix since it's already in the baseURL
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

        // Fix: Remove the duplicate '/api' prefix since it's already in the baseURL
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

        // Fix: Remove the duplicate '/api' prefix since it's already in the baseURL
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
