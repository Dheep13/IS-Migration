import React, { useState, useEffect } from "react"
import {
  ExternalLink,
  CheckCircle,
  XCircle,
  Clock,
  FileText,
  Code,
  Play,
  Download,
  Search,
  FileCode
} from "lucide-react"

import {
  getDocumentation,
  generateIflowMatch,
  getIflowMatchStatus,
  getIflowMatchFile,
  generateIflow,
  getIflowGenerationStatus,
  downloadGeneratedIflow,
  deployIflowToSap,
  directDeployIflowToSap
} from "@services/api"

import { toast } from "react-hot-toast"

// Get environment variables for polling configuration
const DISABLE_AUTO_POLLING = import.meta.env.VITE_DISABLE_AUTO_POLLING === 'true'
const MAX_POLL_COUNT = parseInt(import.meta.env.VITE_MAX_POLL_COUNT || '30')
const POLL_INTERVAL_MS = parseInt(import.meta.env.VITE_POLL_INTERVAL_MS || '5000')
const MAX_FAILED_ATTEMPTS = parseInt(import.meta.env.VITE_MAX_FAILED_ATTEMPTS || '3')

const JobResult = ({ jobInfo, onNewJob }) => {
  const [isGeneratingIflowMatch, setIsGeneratingIflowMatch] = useState(false)
  const [iflowMatchStatus, setIflowMatchStatus] = useState(null)
  const [iflowMatchMessage, setIflowMatchMessage] = useState(null)
  const [iflowMatchFiles, setIflowMatchFiles] = useState(null)
  const [isGeneratingIflow, setIsGeneratingIflow] = useState(false)
  const [isIflowGenerated, setIsIflowGenerated] = useState(false)
  const [isDeploying, setIsDeploying] = useState(false)
  const [isDeployed, setIsDeployed] = useState(false)
  const [downloading, setDownloading] = useState({
    html: false,
    markdown: false,
    iflowReport: false,
    iflowSummary: false,
    generatedIflow: false
  })
  const [showFileAnalysis, setShowFileAnalysis] = useState(false)

  // Check if iFlow match has been processed
  useEffect(() => {
    if (jobInfo.status === "completed" && jobInfo.id) {
      checkIflowMatchStatus()
    }
  }, [jobInfo])

  // Function to check iFlow match status
  const checkIflowMatchStatus = async () => {
    try {
      const result = await getIflowMatchStatus(jobInfo.id)
      if (result.status !== "not_started") {
        setIflowMatchStatus(result.status)
        setIflowMatchMessage(result.message)
        setIflowMatchFiles(result.files || null)
      }
    } catch (error) {
      console.error("Error checking iFlow match status:", error)
      // Don't show an error toast here as this is just a status check
    }
  }

  // Function to generate iFlow match
  const handleGenerateIflowMatch = async () => {
    try {
      setIsGeneratingIflowMatch(true)
      setIflowMatchStatus("processing")
      setIflowMatchMessage(
        "Starting SAP Integration Suite equivalent search..."
      )

      const result = await generateIflowMatch(jobInfo.id)
      toast.success("SAP Integration Suite equivalent search started")

      // Check if auto-polling is disabled in production
      if (DISABLE_AUTO_POLLING) {
        console.log("Auto-polling is disabled by environment configuration. Making a single status check.");

        // Make a single status check after a short delay
        setTimeout(async () => {
          try {
            const statusResult = await getIflowMatchStatus(jobInfo.id);
            setIflowMatchStatus(statusResult.status);
            setIflowMatchMessage(statusResult.message);

            if (statusResult.status === "completed") {
              setIflowMatchFiles(statusResult.files || null);
              setIsGeneratingIflowMatch(false);
              toast.success("SAP Integration Suite equivalent search completed!");
            } else {
              setIsGeneratingIflowMatch(false);
              toast.info("SAP Integration Suite equivalent search is in progress. Check back later for results.");
            }
          } catch (error) {
            console.error("Error checking SAP equivalents status:", error);
            setIsGeneratingIflowMatch(false);
            toast.info("SAP Integration Suite equivalent search is in progress. Check back later for results.");
          }
        }, 5000); // Wait 5 seconds before checking

        return;
      }

      // Start polling for status
      const intervalId = setInterval(async () => {
        try {
          const statusResult = await getIflowMatchStatus(jobInfo.id)
          setIflowMatchStatus(statusResult.status)
          setIflowMatchMessage(statusResult.message)

          if (statusResult.status === "completed") {
            setIflowMatchFiles(statusResult.files || null)
            clearInterval(intervalId)
            setIsGeneratingIflowMatch(false)
            toast.success("SAP Integration Suite equivalent search completed!")
          } else if (statusResult.status === "failed") {
            clearInterval(intervalId)
            setIsGeneratingIflowMatch(false)
            toast.error(
              `SAP Integration Suite equivalent search failed: ${statusResult.message}`
            )
          }
        } catch (error) {
          console.error("Error polling iFlow match status:", error)
        }
      }, POLL_INTERVAL_MS) // Use configured polling interval

      // Clean up interval after 5 minutes (safety)
      setTimeout(() => {
        clearInterval(intervalId)
        if (iflowMatchStatus === "processing") {
          setIflowMatchStatus("unknown")
          setIflowMatchMessage(
            "Status check timed out. Please refresh the page."
          )
          setIsGeneratingIflowMatch(false)
        }
      }, 300000) // 5 minutes
    } catch (error) {
      console.error("Error generating iFlow match:", error)
      toast.error("Failed to start SAP Integration Suite equivalent search")
      setIsGeneratingIflowMatch(false)
      setIflowMatchStatus("failed")
      setIflowMatchMessage(
        "Failed to start SAP Integration Suite equivalent search"
      )
    }
  }

  const [iflowJobId, setIflowJobId] = useState(null)
  const [iflowGenerationStatus, setIflowGenerationStatus] = useState(null)
  const [iflowGenerationMessage, setIflowGenerationMessage] = useState(null)
  const [iflowGenerationFiles, setIflowGenerationFiles] = useState(null)
  const [statusCheckInterval, setStatusCheckInterval] = useState(null)

  // Clean up any existing intervals when component unmounts or when starting a new job
  useEffect(() => {
    return () => {
      if (statusCheckInterval) {
        console.log("Cleaning up status check interval on unmount");
        clearInterval(statusCheckInterval);
      }
    };
  }, [statusCheckInterval]);

  const handleGenerateIflow = async () => {
    try {
      // Clear any existing interval first
      if (statusCheckInterval) {
        console.log("Clearing existing status check interval");
        clearInterval(statusCheckInterval);
        setStatusCheckInterval(null);
      }

      setIsGeneratingIflow(true)
      setIflowGenerationStatus("processing")
      setIflowGenerationMessage("Starting SAP API/iFlow generation...")

      console.log(`Generating iFlow for job ${jobInfo.id}...`)
      console.log(`Platform detected: ${jobInfo.platform || 'mulesoft'}`)

      // Call the API to generate the iFlow with platform information
      const result = await generateIflow(jobInfo.id, jobInfo.platform || 'mulesoft')

      // Check if the result has an error status
      if (result.status === 'error') {
        console.error("Error from iFlow generation API:", result.message);
        toast.error(`Failed to start SAP API/iFlow generation: ${result.message}`);
        setIsGeneratingIflow(false);
        setIflowGenerationStatus("failed");
        setIflowGenerationMessage(result.message);
        return;
      }

      toast.success("SAP API/iFlow generation started")

      // Store the iFlow job ID
      setIflowJobId(result.job_id)

      // Check if auto-polling is disabled in production
      if (DISABLE_AUTO_POLLING) {
        console.log("Auto-polling is disabled by environment configuration. Making a single status check.");

        // Make a single status check after a short delay
        setTimeout(async () => {
          try {
            const statusResult = await getIflowGenerationStatus(result.job_id, jobInfo.platform || 'mulesoft');

            if (statusResult.status === "completed") {
              setIflowGenerationStatus("completed");
              setIflowGenerationMessage("iFlow generation completed successfully");
              setIsGeneratingIflow(false);
              setIsIflowGenerated(true);
              toast.success("iFlow generated successfully!");
            } else {
              // If not completed yet, show a message to check back later
              setIsGeneratingIflow(false);
              toast.info("iFlow generation is in progress. Check back later for results.");
            }
          } catch (error) {
            console.error("Error checking iFlow status:", error);
            setIsGeneratingIflow(false);
            toast.info("iFlow generation is in progress. Check back later for results.");
          }
        }, 5000); // Wait 5 seconds before checking

        return;
      }

      // Start polling for status
      let failedAttempts = 0;
      let pollCount = 0;

      console.log(`Starting polling for iFlow generation job ${result.job_id}`);
      console.log(`Polling configuration: Max polls: ${MAX_POLL_COUNT}, Interval: ${POLL_INTERVAL_MS}ms, Max failed attempts: ${MAX_FAILED_ATTEMPTS}`);

      const intervalId = setInterval(async () => {
        try {
          pollCount++;
          console.log(`Polling attempt ${pollCount} for job ${result.job_id}`);

          // If we've reached the maximum number of polls, stop polling
          if (pollCount >= MAX_POLL_COUNT) {
            console.log(`Reached maximum number of polls (${MAX_POLL_COUNT}). Stopping.`);
            clearInterval(intervalId);
            setStatusCheckInterval(null);

            // Try one final direct download
            try {
              await downloadGeneratedIflow(result.job_id, jobInfo.platform || 'mulesoft');
              setIflowGenerationStatus("completed");
              setIflowGenerationMessage("iFlow generation completed successfully");
              setIsGeneratingIflow(false);
              setIsIflowGenerated(true);
              toast.success("iFlow generated successfully!");
            } catch (finalDownloadError) {
              setIflowGenerationStatus("unknown");
              setIflowGenerationMessage("Status check timed out. The iFlow may still be generating.");
              setIsGeneratingIflow(false);
              toast.warning("Status check timed out. Try downloading the iFlow manually.");
            }
            return;
          }

          const statusResult = await getIflowGenerationStatus(result.job_id, jobInfo.platform || 'mulesoft')

          // If the result has an error status, handle it but don't stop polling yet
          if (statusResult.status === 'error') {
            console.warn("Error from status check:", statusResult.message);
            failedAttempts++;

            // Only if we've had multiple consecutive failures, try direct download
            if (failedAttempts >= MAX_FAILED_ATTEMPTS) {
              await handleDirectDownloadCheck(result.job_id, intervalId);
            }
            return;
          }

          // Reset failed attempts counter on successful API call
          failedAttempts = 0;

          setIflowGenerationStatus(statusResult.status)
          setIflowGenerationMessage(statusResult.message)

          if (statusResult.status === "completed") {
            setIflowGenerationFiles(statusResult.files || null)
            clearInterval(intervalId)
            setStatusCheckInterval(null)
            setIsGeneratingIflow(false)
            setIsIflowGenerated(true)
            toast.success("iFlow generated successfully!")
          } else if (statusResult.status === "failed") {
            clearInterval(intervalId)
            setStatusCheckInterval(null)
            setIsGeneratingIflow(false)
            toast.error(`iFlow generation failed: ${statusResult.message}`)
          }
        } catch (error) {
          console.error("Error polling iFlow generation status:", error)
          failedAttempts++;

          // If we've had multiple consecutive failures, try to download the file directly
          if (failedAttempts >= MAX_FAILED_ATTEMPTS) {
            await handleDirectDownloadCheck(result.job_id, intervalId);
          }
        }
      }, POLL_INTERVAL_MS) // Use configured polling interval

      // Store the interval ID for cleanup
      setStatusCheckInterval(intervalId)
    } catch (error) {
      console.error("Error generating iFlow:", error)
      toast.error("Failed to start SAP API/iFlow generation")
      setIsGeneratingIflow(false)
      setIflowGenerationStatus("failed")
      setIflowGenerationMessage("Failed to start SAP API/iFlow generation")
    }
  }

  // Helper function to check if the file exists by trying to download it
  const handleDirectDownloadCheck = async (jobId, intervalId) => {
    console.log(`Multiple consecutive status check failures. Trying direct download for job ${jobId}...`);

    try {
      // Try to download the file directly to see if it exists
      await downloadGeneratedIflow(jobId, jobInfo.platform || 'mulesoft');

      // If download succeeds, the file exists and job is complete
      clearInterval(intervalId);
      setStatusCheckInterval(null);
      setIflowGenerationStatus("completed");
      setIflowGenerationMessage("iFlow generation completed successfully");
      setIsGeneratingIflow(false);
      setIsIflowGenerated(true);
      toast.success("iFlow generated successfully!");
      console.log("Direct download successful - assuming job is complete");
      return true;
    } catch (downloadError) {
      console.error("Direct download failed:", downloadError);
      return false;
    }
  }

  const handleDeployToSap = async () => {
    try {
      setIsDeploying(true)

      // ONLY use the iFlow job ID - don't fall back to the documentation job ID
      if (!iflowJobId) {
        toast.error("iFlow job ID not found. Please generate the iFlow first.")
        setIsDeploying(false)
        return
      }

      const deployJobId = iflowJobId

      console.log(`Deploying iFlow for job ${deployJobId} to SAP Integration Suite...`)

      // Get the iFlow name from the job ID or use a default name
      const iflowName = `GeneratedIFlow_${deployJobId.substring(0, 8)}`
      const iflowId = iflowName.replace(/[^a-zA-Z0-9_]/g, '_')
      const packageId = "ConversionPackages"

      // Use the direct deployment approach with platform information
      console.log(`Using direct deployment with iflowId=${iflowId}, iflowName=${iflowName}, packageId=${packageId}, platform=${jobInfo.platform || 'mulesoft'}`)
      const result = await directDeployIflowToSap(deployJobId, packageId, iflowId, iflowName, jobInfo.platform || 'mulesoft')

      console.log("Direct deployment response:", result)

      if (result.status === 'success') {
        setIsDeployed(true)
        toast.success("Deployed to SAP Integration Suite successfully!")
      } else {
        toast.error(`Deployment failed: ${result.message}`)
      }
    } catch (error) {
      console.error("Error deploying to SAP:", error)
      toast.error("Failed to deploy to SAP Integration Suite. Please try again.")
    } finally {
      setIsDeploying(false)
    }
  }

  const getStatusIcon = () => {
    if (jobInfo.status === "completed") {
      return <CheckCircle className="h-5 w-5 text-green-500" />
    } else if (jobInfo.status === "failed") {
      return <XCircle className="h-5 w-5 text-red-500" />
    } else {
      return <Clock className="h-5 w-5 text-blue-500" />
    }
  }

  const downloadFile = async (fileType, filename) => {
    try {
      setDownloading(prev => ({ ...prev, [fileType]: true }))

      console.log(
        `Attempting to download ${fileType} file for job ${jobInfo.id}...`
      )

      // Get the file using our API service
      const blob = await getDocumentation(jobInfo.id, fileType)

      console.log(
        `File download response received, type: ${blob.type}, size: ${blob.size} bytes`
      )

      if (blob.size === 0) {
        toast.error(
          `Empty file received. No content available for ${fileType}.`
        )
        console.error(`Empty blob received for ${fileType}`)
        setDownloading(prev => ({ ...prev, [fileType]: false }))
        return
      }

      // Create a download link
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()

      // Clean up
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)

      toast.success(`${fileType} file downloaded successfully!`)
    } catch (error) {
      console.error(`Error downloading ${fileType} file:`, error)
      toast.error(`Failed to download ${fileType} file. Please try again.`)
    } finally {
      setDownloading(prev => ({ ...prev, [fileType]: false }))
    }
  }

  const downloadIflowMatchFile = async (fileType, filename) => {
    try {
      const downloadKey = fileType === "report" ? "iflowReport" : "iflowSummary"
      setDownloading(prev => ({ ...prev, [downloadKey]: true }))

      console.log(
        `Attempting to download iFlow match ${fileType} file for job ${jobInfo.id}...`
      )

      // Get the file using our API service
      const blob = await getIflowMatchFile(jobInfo.id, fileType)

      console.log(
        `iFlow match file download response received, type: ${blob.type}, size: ${blob.size} bytes`
      )

      if (blob.size === 0) {
        toast.error(
          `Empty file received. No content available for iFlow match ${fileType}.`
        )
        console.error(`Empty blob received for iFlow match ${fileType}`)
        setDownloading(prev => ({ ...prev, [downloadKey]: false }))
        return
      }

      // Create a download link
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()

      // Clean up
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)

      toast.success(`iFlow match ${fileType} file downloaded successfully!`)
    } catch (error) {
      console.error(`Error downloading iFlow match ${fileType} file:`, error)
      toast.error(
        `Failed to download iFlow match ${fileType} file. Please try again.`
      )
    } finally {
      const downloadKey = fileType === "report" ? "iflowReport" : "iflowSummary"
      setDownloading(prev => ({ ...prev, [downloadKey]: false }))
    }
  }

  const handleDownloadGeneratedIflow = async () => {
    try {
      if (!iflowJobId) {
        toast.error("iFlow job ID not found. Please try generating the iFlow again.")
        return
      }

      setDownloading(prev => ({ ...prev, generatedIflow: true }))

      console.log(`Downloading generated iFlow for job ${iflowJobId}...`)

      // Get the file using our API service
      const blob = await downloadGeneratedIflow(iflowJobId, jobInfo.platform || 'mulesoft')

      console.log(`iFlow download response received, size: ${blob.size} bytes`)

      if (blob.size === 0) {
        toast.error("Empty file received. No content available for iFlow.")
        console.error("Empty blob received for iFlow")
        setDownloading(prev => ({ ...prev, generatedIflow: false }))
        return
      }

      // Create a download link
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `sap_generated_iflow_${iflowJobId}.zip`
      document.body.appendChild(a)
      a.click()

      // Clean up
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)

      toast.success("Generated SAP iFlow downloaded successfully!")
    } catch (error) {
      console.error("Error downloading generated iFlow:", error)
      toast.error("Failed to download generated iFlow. Please try again.")
    } finally {
      setDownloading(prev => ({ ...prev, generatedIflow: false }))
    }
  }

  return (
    <div className="bg-white shadow-sm rounded-lg p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2">
          {getStatusIcon()}
          <h3 className="text-lg font-semibold text-gray-800">
            Job Status: <span className="capitalize">{jobInfo.status}</span>
          </h3>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div>
          <p className="text-gray-600">
            Job ID:{" "}
            <span className="font-medium text-gray-800">{jobInfo.id}</span>
          </p>
          <p className="text-gray-600">
            Created:{" "}
            <span className="font-medium text-gray-800">
              {new Date(jobInfo.created).toLocaleString()}
            </span>
          </p>
        </div>
        <div>
          <p className="text-gray-600">
            Last Updated:{" "}
            <span className="font-medium text-gray-800">
              {new Date(jobInfo.last_updated).toLocaleString()}
            </span>
          </p>
          <p className="text-gray-600">
            AI Enhancement:{" "}
            <span className="font-medium text-gray-800">
              {jobInfo.enhance ? "Enabled" : "Disabled"}
            </span>
          </p>
        </div>
      </div>

      {jobInfo.status === "completed" && (
        <>
          <div>
            <h4 className="font-semibold text-gray-800 mb-3">
              Documentation Files:
            </h4>
            <div className="space-y-2">
              <div className="flex flex-wrap items-center gap-2 p-3 bg-gray-50 rounded-md">
                <FileText className="h-5 w-5 text-blue-500" />
                <span className="font-medium text-gray-800">
                  HTML Documentation with Mermaid
                </span>

                <div className="flex gap-2 ml-auto">
                  <a
                    href={`${import.meta.env.VITE_API_URL}/docs/${jobInfo.id}/html`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-1.5 text-blue-600 hover:bg-blue-100 rounded transition-colors duration-200"
                    title="View in browser"
                  >
                    <ExternalLink className="h-4 w-4" />
                  </a>

                  <button
                    onClick={() =>
                      downloadFile(
                        "html",
                        `mulesoft_documentation_${jobInfo.id}.html`
                      )
                    }
                    disabled={downloading.html}
                    className="p-1.5 text-blue-600 hover:bg-blue-100 rounded transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                    title="Download file"
                  >
                    {downloading.html ? (
                      <div className="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                    ) : (
                      <Download className="h-4 w-4" />
                    )}
                  </button>
                </div>
              </div>

              {/* Markdown Documentation section removed */}
              {/* Flow Visualization section removed */}
              {/* Direct links section removed */}
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-gray-800 mb-3">
              SAP Integration Suite Options (Independent Actions):
            </h4>
            <p className="text-sm text-gray-600 mb-2">
              These actions can be performed independently. You can generate an iFlow directly from the documentation or find SAP equivalents first.
            </p>
            <div className="flex flex-wrap items-center">
              <button
                onClick={handleGenerateIflowMatch}
                disabled={
                  isGeneratingIflowMatch || iflowMatchStatus === "completed"
                }
                className={`
                  px-4 py-2 rounded-md font-medium flex items-center space-x-2
                  ${
                    isGeneratingIflowMatch || iflowMatchStatus === "completed"
                      ? "bg-green-100 text-green-800 cursor-not-allowed"
                      : "bg-green-600 text-white hover:bg-green-700"
                  }
                  transition-colors duration-200
                `}
              >
                {isGeneratingIflowMatch ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-current border-t-transparent" />
                    <span>Finding SAP Equivalents...</span>
                  </>
                ) : iflowMatchStatus === "completed" ? (
                  <>
                    <CheckCircle className="h-4 w-4" />
                    <span>SAP Equivalents Found</span>
                  </>
                ) : (
                  <>
                    <span className="inline-flex items-center justify-center w-6 h-6 bg-white text-green-600 rounded-full mr-1 font-bold">1</span>
                    <Search className="h-4 w-4" />
                    <span>Find SAP Integration Suite Equivalents</span>
                  </>
                )}
              </button>

              <div className="mx-2 text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14"></path>
                  <path d="m12 5 7 7-7 7"></path>
                </svg>
              </div>

              <button
                onClick={handleGenerateIflow}
                disabled={
                  isGeneratingIflow ||
                  isIflowGenerated
                }
                className={`
                  px-4 py-2 rounded-md font-medium flex items-center space-x-2
                  ${
                    isGeneratingIflow
                      ? "bg-blue-100 text-blue-800 cursor-not-allowed"
                      : isIflowGenerated
                      ? "bg-green-100 text-green-800 cursor-not-allowed"
                      : "bg-blue-600 text-white hover:bg-blue-700"
                  }
                  transition-colors duration-200
                `}
              >
                {isGeneratingIflow ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-current border-t-transparent" />
                    <span>Generating SAP API/iFlow...</span>
                  </>
                ) : isIflowGenerated ? (
                  <>
                    <CheckCircle className="h-4 w-4" />
                    <span>SAP API/iFlow Generated</span>
                  </>
                ) : (
                  <>
                    <span className="inline-flex items-center justify-center w-6 h-6 bg-white text-blue-600 rounded-full mr-1 font-bold">2</span>
                    <Code className="h-4 w-4" />
                    <span>Generate SAP API/iFlow</span>
                  </>
                )}
              </button>

              <div className="mx-2 text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14"></path>
                  <path d="m12 5 7 7-7 7"></path>
                </svg>
              </div>

              <button
                onClick={handleDeployToSap}
                disabled={!isIflowGenerated || isDeploying || isDeployed}
                className={`
                  px-4 py-2 rounded-md font-medium flex items-center space-x-2
                  ${
                    !isIflowGenerated
                      ? "bg-gray-100 text-gray-500 cursor-not-allowed"
                      : isDeploying
                      ? "bg-green-100 text-green-800 cursor-not-allowed"
                      : isDeployed
                      ? "bg-green-100 text-green-800 cursor-not-allowed"
                      : "bg-green-600 text-white hover:bg-green-700"
                  }
                  transition-colors duration-200
                `}
              >
                {isDeploying ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-current border-t-transparent" />
                    <span>Deploying...</span>
                  </>
                ) : isDeployed ? (
                  <>
                    <CheckCircle className="h-4 w-4" />
                    <span>Deployed</span>
                  </>
                ) : (
                  <>
                    <span className="inline-flex items-center justify-center w-6 h-6 bg-white text-green-600 rounded-full mr-1 font-bold">3</span>
                    <Play className="h-4 w-4" />
                    <span>Deploy to SAP Integration Suite</span>
                  </>
                )}
              </button>
            </div>

            {/* Show iFlow match status and results */}
            {iflowMatchStatus && (
              <div className="mt-4">
                <div
                  className={`p-4 rounded-md ${
                    iflowMatchStatus === "completed"
                      ? "bg-green-50"
                      : iflowMatchStatus === "failed"
                      ? "bg-red-50"
                      : "bg-blue-50"
                  }`}
                >
                  <p
                    className={`text-sm font-medium ${
                      iflowMatchStatus === "completed"
                        ? "text-green-800"
                        : iflowMatchStatus === "failed"
                        ? "text-red-800"
                        : "text-blue-800"
                    }`}
                  >
                    {iflowMatchMessage ||
                      "Processing SAP Integration Suite equivalent search..."}
                  </p>

                  {iflowMatchStatus === "completed" && iflowMatchFiles && (
                    <div className="mt-3 space-y-2">
                      <h5 className="text-sm font-semibold text-gray-700">
                        Available Files:
                      </h5>

                      <div className="flex flex-wrap items-center gap-2 p-3 bg-white rounded-md">
                        <FileText className="h-5 w-5 text-blue-500" />
                        <span className="font-medium text-gray-800">
                          Integration Match Report
                        </span>

                        <div className="flex gap-2 ml-auto">
                          <a
                            href={`${
                              import.meta.env.VITE_API_URL
                            }/iflow-match/${jobInfo.id}/report`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="p-1.5 text-blue-600 hover:bg-blue-100 rounded transition-colors duration-200"
                            title="View in browser"
                          >
                            <ExternalLink className="h-4 w-4" />
                          </a>

                          <button
                            onClick={() =>
                              downloadIflowMatchFile(
                                "report",
                                `sap_integration_match_${jobInfo.id}.html`
                              )
                            }
                            disabled={downloading.iflowReport}
                            className="p-1.5 text-blue-600 hover:bg-blue-100 rounded transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                            title="Download file"
                          >
                            {downloading.iflowReport ? (
                              <div className="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                            ) : (
                              <Download className="h-4 w-4" />
                            )}
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Show generated iFlow when available */}
            {isIflowGenerated && (
              <div className="mt-4">
                <div className="p-4 rounded-md bg-green-50">
                  <p className="text-sm font-medium text-green-800">
                    SAP API/iFlow has been generated successfully!
                  </p>

                  <div className="mt-3 space-y-2">
                    <h5 className="text-sm font-semibold text-gray-700">
                      Generated File:
                    </h5>

                    <div className="flex flex-wrap items-center gap-2 p-3 bg-white rounded-md">
                      <FileCode className="h-5 w-5 text-blue-500" />
                      <span className="font-medium text-gray-800">
                        SAP API/iFlow Definition
                      </span>

                      <div className="flex gap-2 ml-auto">
                        <button
                          onClick={handleDownloadGeneratedIflow}
                          disabled={downloading.generatedIflow}
                          className="p-1.5 text-blue-600 hover:bg-blue-100 rounded transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                          title="Download file"
                        >
                          {downloading.generatedIflow ? (
                            <div className="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                          ) : (
                            <Download className="h-4 w-4" />
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </>
      )}

      {jobInfo.file_info && (
        <div className="mt-6">
          <button
            onClick={() => setShowFileAnalysis(!showFileAnalysis)}
            className="flex items-center justify-between w-full font-semibold text-gray-800 mb-3 bg-gray-100 p-3 rounded-md hover:bg-gray-200 transition-colors"
          >
            <span>File Analysis</span>
            <span className="text-gray-500">
              {showFileAnalysis ? '▼' : '►'}
            </span>
          </button>

          {showFileAnalysis && (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      File Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Count
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      XML Files
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">
                      {jobInfo.file_info.xml_files}
                    </td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      Properties Files
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">
                      {jobInfo.file_info.properties_files}
                    </td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      JSON Files
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">
                      {jobInfo.file_info.json_files}
                    </td>
                  </tr>
                  {jobInfo.file_info.yaml_files !== undefined && (
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        YAML Files
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">
                        {jobInfo.file_info.yaml_files}
                      </td>
                    </tr>
                  )}
                  {jobInfo.file_info.raml_files !== undefined && (
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        RAML Files
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">
                        {jobInfo.file_info.raml_files}
                      </td>
                    </tr>
                  )}
                  {jobInfo.file_info.dwl_files !== undefined && (
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        DWL Files
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">
                        {jobInfo.file_info.dwl_files}
                      </td>
                    </tr>
                  )}
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      Other Files
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">
                      {jobInfo.file_info.other_files}
                    </td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-800">
                      Total Files
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-800">
                      {jobInfo.file_info.total_files}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {jobInfo.parsed_details && (
        <div>
          <h4 className="font-semibold text-gray-800 mb-3">
            Parsed MuleSoft Components:
          </h4>
          {/* Changed to flex layout for better responsiveness */}
          <div className="flex flex-wrap gap-4">
            <div className="bg-blue-50 p-4 rounded-md flex-1 min-w-[150px]">
              <p className="text-xs text-blue-600 uppercase font-semibold">
                Flows
              </p>
              <p className="text-2xl font-bold text-blue-800">
                {jobInfo.parsed_details.flows}
              </p>
            </div>
            <div className="bg-green-50 p-4 rounded-md flex-1 min-w-[150px]">
              <p className="text-xs text-green-600 uppercase font-semibold">
                Subflows
              </p>
              <p className="text-2xl font-bold text-green-800">
                {jobInfo.parsed_details.subflows}
              </p>
            </div>
            <div className="bg-purple-50 p-4 rounded-md flex-1 min-w-[150px]">
              <p className="text-xs text-purple-600 uppercase font-semibold">
                Configurations
              </p>
              <p className="text-2xl font-bold text-purple-800">
                {jobInfo.parsed_details.configs}
              </p>
            </div>
            <div className="bg-orange-50 p-4 rounded-md flex-1 min-w-[150px]">
              <p className="text-xs text-orange-600 uppercase font-semibold">
                Error Handlers
              </p>
              <p className="text-2xl font-bold text-orange-800">
                {jobInfo.parsed_details.error_handlers}
              </p>
            </div>
          </div>

          {/* Add a table view for better visibility on smaller screens */}
          <div className="mt-4 overflow-x-auto md:hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Component
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Count
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                <tr>
                  <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-blue-600">
                    Flows
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm font-bold text-gray-800">
                    {jobInfo.parsed_details.flows}
                  </td>
                </tr>
                <tr>
                  <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-green-600">
                    Subflows
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm font-bold text-gray-800">
                    {jobInfo.parsed_details.subflows}
                  </td>
                </tr>
                <tr>
                  <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-purple-600">
                    Configurations
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm font-bold text-gray-800">
                    {jobInfo.parsed_details.configs}
                  </td>
                </tr>
                <tr>
                  <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-orange-600">
                    Error Handlers
                  </td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm font-bold text-gray-800">
                    {jobInfo.parsed_details.error_handlers}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {jobInfo.status === "failed" && jobInfo.error && (
        <div className="bg-red-50 p-4 rounded-md">
          <h4 className="font-semibold text-red-800 mb-1">Error:</h4>
          <p className="text-red-700">{jobInfo.error}</p>
        </div>
      )}

      {/* Removed the Upload New File button */}
    </div>
  )
}

export default JobResult
