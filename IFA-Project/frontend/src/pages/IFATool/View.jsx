import React, { useState, useRef, useEffect } from "react"
import { toast } from "react-hot-toast"
import FileUploadForm from "@pages/common/FileUploadForm"
import ProgressTracker from "@pages/common/ProgressTracker"
import JobResult from "@pages/common/JobResult"
import LLMProviderSelector from "@components/LLMProviderSelector"
import { generateDocs, getJobStatus } from "@services/api"
import { useLLMProvider } from "@/contexts/LLMProviderContext"
import { LLM_PROVIDER_LABELS } from "@utils/constants"

// Get environment variables for polling configuration
const DISABLE_AUTO_POLLING = import.meta.env.VITE_DISABLE_AUTO_POLLING === 'true'
const MAX_POLL_COUNT = parseInt(import.meta.env.VITE_MAX_POLL_COUNT || '30')
const POLL_INTERVAL_MS = parseInt(import.meta.env.VITE_POLL_INTERVAL_MS || '5000')
const INITIAL_POLL_INTERVAL_MS = 2000 // Start with a faster polling interval

const View = () => {
  const { selectedLLMProvider, setSelectedLLMProvider } = useLLMProvider();
  const [jobInfo, setJobInfo] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [startTime, setStartTime] = useState(null)
  const [pollInterval, setPollInterval] = useState(null)
  const [pollCount, setPollCount] = useState(0)
  const [consecutiveErrors, setConsecutiveErrors] = useState(0)
  const [showLLMSelector, setShowLLMSelector] = useState(false)

  const abortControllerRef = useRef(null)

  // No longer checking backend connectivity on mount for production

  const startJob = async (files, enhance, platform = 'mulesoft') => {
    setIsLoading(true)

    try {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
      abortControllerRef.current = new AbortController()

      const formData = new FormData()
      files.forEach(file => formData.append("files[]", file))
      formData.append("enhance", enhance.toString())
      formData.append("platform", platform)

      const result = await generateDocs(
        formData,
        abortControllerRef.current.signal
      )

      if (result) {
        // Initialize notification state for the new job
        setHasNotifiedCompletion({
          [result.job_id]: { status: false, iflow: false }
        })

        setJobInfo({
          id: result.job_id,
          status: "queued",
          created: new Date().toISOString(),
          last_updated: new Date().toISOString(),
          enhance: enhance,
          files: null,
          processing_step: null,
          processing_message: "Job started successfully. Processing files...",
          file_info: null,
          parsed_details: null,
          error: null
        })

        // Set the start time
        setStartTime(new Date())

        // Start polling
        startPolling(result.job_id, enhance)

        toast.success("Documentation generation started!")
      }
    } catch (error) {
      toast.error("Failed to start documentation generation")
      console.error("Error starting job:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const startPolling = (jobId, isEnhancement) => {
    // Clear any existing polling
    if (pollInterval) {
      clearInterval(pollInterval)
    }

    // Reset poll count and error count
    setPollCount(0)
    setConsecutiveErrors(0)

    // Check if auto-polling is disabled in production
    if (DISABLE_AUTO_POLLING) {
      console.log("Auto-polling is disabled by environment configuration")
      // Make a single request to get initial status
      checkJobStatus(jobId)

      // Schedule a single follow-up check after a short delay
      // This helps ensure we catch quick job completions
      setTimeout(() => {
        console.log("Performing one follow-up status check...")
        checkJobStatus(jobId)
      }, 5000)

      return
    }

    // Log if this is an enhanced job
    if (isEnhancement) {
      console.log("Enhanced documentation job detected - may take longer to complete")
    }

    // Function to perform a single poll
    const performPoll = async () => {
      // Increment poll count
      setPollCount(prev => {
        const newCount = prev + 1
        console.log(`Poll #${newCount} for job ${jobId}`)
        return newCount
      })

      // Check job status first
      await checkJobStatus(jobId)

      // After checking status, see if we've reached the maximum number of polls
      // This needs to be checked after setPollCount has been processed
      const currentPollCount = pollCount + 1 // Add 1 because setPollCount is asynchronous
      if (currentPollCount >= MAX_POLL_COUNT) {
        console.log(`Reached maximum poll count (${MAX_POLL_COUNT}). Stopping polling.`)
        if (pollInterval) {
          clearInterval(pollInterval)
          setPollInterval(null)
        }
      }
    }

    // Start with initial polling interval
    const interval = setInterval(performPoll, INITIAL_POLL_INTERVAL_MS)
    setPollInterval(interval)

    // After 15 polls, switch to the configured polling interval for slower polling
    setTimeout(() => {
      if (pollInterval === interval) { // Only if this interval is still active
        clearInterval(interval)
        const newInterval = setInterval(performPoll, POLL_INTERVAL_MS)
        setPollInterval(newInterval)
        console.log(`Switched to slower polling interval: ${POLL_INTERVAL_MS}ms`)
      }
    }, INITIAL_POLL_INTERVAL_MS * 15)
  }

  // Keep track of job completion notification state
  const [hasNotifiedCompletion, setHasNotifiedCompletion] = useState({})

  const checkJobStatus = async jobId => {
    try {
      console.log(`Checking status for job ${jobId}...`)
      const data = await getJobStatus(jobId)

      if (data) {
        // Reset consecutive errors counter on successful API call
        setConsecutiveErrors(0)

        // Check if the job ID has changed
        if (data.id && data.id !== jobId) {
          console.warn(`Job ID changed from ${jobId} to ${data.id}. This could cause polling issues.`)
        }

        // Log the job status for debugging
        console.log(`Job status: ${data.status}, Processing step: ${data.processing_step}, Message: ${data.processing_message}`)

        // Update job info state
        setJobInfo(data)

        // If job is complete or failed, stop polling
        if (data.status === "completed" || data.status === "failed") {
          console.log(`Job ${jobId} ${data.status}. Stopping polling.`)

          if (pollInterval) {
            clearInterval(pollInterval)
            setPollInterval(null)
          }

          // Initialize job notification state if needed
          if (!hasNotifiedCompletion[jobId]) {
            setHasNotifiedCompletion(prev => ({
              ...prev,
              [jobId]: { status: false, iflow: false }
            }))
          }

          // Only show toast notification if we haven't shown it before for this job's status
          if (
            hasNotifiedCompletion[jobId] &&
            !hasNotifiedCompletion[jobId].status
          ) {
            if (data.status === "completed") {
              toast.success("Documentation generation completed!")
            } else {
              toast.error(`Job failed: ${data.error || "Unknown error"}`)
            }

            // Mark this job's status as having been notified
            setHasNotifiedCompletion(prev => ({
              ...prev,
              [jobId]: { ...prev[jobId], status: true }
            }))
          }

          // Check for iFlow match completion
          if (
            data.iflow_match_status === "completed" &&
            hasNotifiedCompletion[jobId] &&
            !hasNotifiedCompletion[jobId].iflow
          ) {
            // Mark iFlow notification as completed to prevent future notifications
            setHasNotifiedCompletion(prev => ({
              ...prev,
              [jobId]: { ...prev[jobId], iflow: true }
            }))

            // Show iFlow completion notification
            toast.success("SAP Integration Suite equivalent search completed!")
          }
        } else {
          console.log(`Job ${jobId} status: ${data.status}`)
        }
      }
    } catch (error) {
      console.error("Error checking job status:", error)

      // Increment error count for consecutive failures
      setConsecutiveErrors(prev => prev + 1)

      // If we've had too many consecutive errors, stop polling
      if (consecutiveErrors > 3 && pollInterval) {
        console.error("Too many consecutive errors. Stopping polling.")
        clearInterval(pollInterval)
        setPollInterval(null)
        toast.error("Lost connection to the server. Please refresh the page.")
      }
    }
  }

  // Effect to handle job status changes
  useEffect(() => {
    if (jobInfo && (jobInfo.status === "completed" || jobInfo.status === "failed")) {
      console.log(`Job status changed to ${jobInfo.status}. Ensuring polling is stopped.`)
      if (pollInterval) {
        console.log("Cleaning up polling interval due to job completion")
        clearInterval(pollInterval)
        setPollInterval(null)
      }
    }
  }, [jobInfo, pollInterval])

  // Cleanup polling on unmount
  useEffect(() => {
    // Log the current polling configuration
    console.log(`Polling configuration: ${DISABLE_AUTO_POLLING ? 'Disabled' : 'Enabled'}, Max polls: ${MAX_POLL_COUNT}, Interval: ${POLL_INTERVAL_MS}ms`)

    return () => {
      // Clean up any active polling
      if (pollInterval) {
        console.log("Cleaning up polling interval on component unmount")
        clearInterval(pollInterval)
      }

      // Abort any in-flight requests
      if (abortControllerRef.current) {
        console.log("Aborting any in-flight requests on component unmount")
        abortControllerRef.current.abort()
      }
    }
  }, [])

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Integration Flow Analyzer</h1>
          <p className="text-gray-600">
            Convert integration flows to SAP Integration Suite using {LLM_PROVIDER_LABELS[selectedLLMProvider]}
          </p>
        </div>
        <button
          onClick={() => setShowLLMSelector(!showLLMSelector)}
          className="px-4 py-2 text-sm bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-colors"
        >
          AI Model: {LLM_PROVIDER_LABELS[selectedLLMProvider]}
        </button>
      </div>

      {showLLMSelector && (
        <div className="bg-gray-50 p-6 rounded-lg">
          <LLMProviderSelector
            selectedProvider={selectedLLMProvider}
            onProviderChange={(provider) => {
              setSelectedLLMProvider(provider);
              setShowLLMSelector(false);
              // Reset job info when provider changes
              setJobInfo(null);
              setHasNotifiedCompletion({});
              if (pollInterval) {
                clearInterval(pollInterval);
                setPollInterval(null);
              }
            }}
          />
        </div>
      )}

      {/* Connection status is hidden in production */}

      {!jobInfo || (jobInfo.status === "failed" && !isLoading) ? (
        <FileUploadForm onSubmit={startJob} isLoading={isLoading} />
      ) : (
        <div className="space-y-6 animate-fadeIn">
          <ProgressTracker
            status={jobInfo.status}
            processingStep={jobInfo.processing_step}
            isEnhancement={jobInfo.enhance}
            startTime={startTime}
            pollCount={pollCount}
            statusMessage={jobInfo.processing_message}
          />

          <JobResult
            jobInfo={jobInfo}
            onNewJob={() => {
              // Reset job info
              setJobInfo(null)
              // Reset notification state (initialize with empty object)
              setHasNotifiedCompletion({})
              // Clear any existing polling
              if (pollInterval) {
                clearInterval(pollInterval)
                setPollInterval(null)
              }
            }}
          />
        </div>
      )}
    </div>
  )
}

export default View
