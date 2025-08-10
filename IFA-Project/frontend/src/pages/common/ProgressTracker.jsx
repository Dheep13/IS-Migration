import React, { useState, useEffect } from "react"
import { Clock } from "lucide-react"

const ProgressTracker = ({
  status,
  processingStep,
  isEnhancement,
  startTime,
  pollCount,
  statusMessage,
  deploymentStatus,
  deployedIflowName,
  deploymentDetails
}) => {
  const [elapsedTime, setElapsedTime] = useState("0s")

  useEffect(() => {
    let interval = null

    // Define active statuses that should keep the timer running
    const activeStatuses = [
      "processing",
      "documentation_ready",
      "ready_for_iflow_generation",
      "generating_iflow",
      "iflow_generation_started",
      "queued"
    ]

    // Define completed/stopped statuses
    const stoppedStatuses = [
      "completed",
      "failed",
      "iflow_generation_failed"
    ]

    const isActive = startTime && (
      activeStatuses.includes(status) ||
      deploymentStatus === "deploying" ||
      (status === "processing" && !stoppedStatuses.includes(status))
    )

    const isStopped = stoppedStatuses.includes(status) ||
                     deploymentStatus === "completed" ||
                     deploymentStatus === "failed"

    if (isActive && !isStopped) {
      interval = setInterval(() => {
        const now = new Date()
        const elapsed = Math.floor((now.getTime() - startTime.getTime()) / 1000)
        const minutes = Math.floor(elapsed / 60)
        const seconds = elapsed % 60
        setElapsedTime(`${minutes}m ${seconds}s`)
      }, 1000)
    } else if (isStopped) {
      // Set final elapsed time for completed jobs
      if (startTime) {
        const now = new Date()
        const elapsed = Math.floor((now.getTime() - startTime.getTime()) / 1000)
        const minutes = Math.floor(elapsed / 60)
        const seconds = elapsed % 60
        setElapsedTime(`${minutes}m ${seconds}s`)
      }
    }

    return () => {
      if (interval) {
        clearInterval(interval)
      }
    }
  }, [startTime, status, deploymentStatus])

  // Calculate progress percentage based on status and processing step
  const getProgressPercentage = () => {
    // Debug logging to see what status we're getting
    console.log("ProgressTracker - Status:", status, "ProcessingStep:", processingStep, "DeploymentStatus:", deploymentStatus);
    console.log("ProgressTracker - Deployment Info:", { deployedIflowName, deploymentDetails, statusMessage });

    // Check for deployment status first (highest priority)
    if (deploymentStatus === "deploying") {
      return 90 // Deployment in progress
    } else if (deploymentStatus === "completed") {
      return 100 // Deployment completed successfully
    } else if (deploymentStatus === "failed") {
      return 100 // Deployment failed (but progress bar shows complete)
    }

    // Documentation upload workflow - check for various status formats
    if (status === "queued") {
      return 5
    } else if (status === "documentation_ready" || status === "ready_for_iflow_generation" || processingStep === "documentation_ready") {
      return 50 // Document processed and ready for iFlow generation
    } else if (status === "generating_iflow" || status === "iflow_generation_started" || processingStep === "iflow_generation" || processingStep === "generating_iflow") {
      return 75 // iFlow generation in progress
    } else if (status === "completed" && !deploymentStatus) {
      return 85 // iFlow generation completed, ready for deployment
    } else if (status === "failed" || status === "iflow_generation_failed") {
      return 100 // Failed (but progress bar shows complete)
    }

    // Traditional XML processing workflow
    else if (status === "processing") {
      if (processingStep === "file_analysis") {
        return 15
      } else if (processingStep === "mule_parsing") {
        return 30
      } else if (processingStep === "visualization") {
        return 45
      } else if (processingStep === "llm_enhancing") {
        return 65
      } else if (processingStep === "llm_complete") {
        return 85
      } else if (processingStep === "llm_failed") {
        return 85
      } else {
        // Fallback based on poll count
        if (isEnhancement) {
          return Math.min(80, 10 + pollCount * 2)
        } else {
          return Math.min(90, 10 + pollCount * 5)
        }
      }
    }

    return 5 // Default fallback
  }

  // Get the progress text based on status and processing step
  const getProgressText = () => {
    // Check for deployment status first (highest priority)
    if (deploymentStatus === "deploying") {
      return "Deploying to SAP Integration Suite..."
    } else if (deploymentStatus === "completed") {
      // Get the deployed iFlow name from multiple sources
      const deployedName = deployedIflowName ||
                           deploymentDetails?.iflow_name ||
                           statusMessage?.match(/deployed as: (.+?)(?:\s|$)/i)?.[1] ||
                           statusMessage?.match(/deployed.*?name.*?[:\s](.+?)(?:\s|$)/i)?.[1] ||
                           statusMessage?.match(/iFlow.*?name.*?[:\s](.+?)(?:\s|$)/i)?.[1];

      if (deployedName) {
        return ` Deployed: ${deployedName}`;
      }
      return " Deployed to SAP Integration Suite!";
    } else if (deploymentStatus === "failed") {
      return "Deployment failed"
    }
    
    // Documentation upload workflow
    if (status === "queued") {
      return "Queued..."
    } else if (status === "documentation_ready" || status === "ready_for_iflow_generation" || processingStep === "documentation_ready") {
      return "Ready for iFlow generation"
    } else if (status === "generating_iflow" || status === "iflow_generation_started" || processingStep === "iflow_generation" || processingStep === "generating_iflow") {
      return "Generating iFlow..."
    } else if (status === "completed" && !deploymentStatus) {
      return "iFlow generated successfully!"
    } else if (status === "failed" || status === "iflow_generation_failed") {
      return "Failed"
    }

    // Traditional XML processing workflow
    else if (status === "processing") {
      if (processingStep === "file_analysis") {
        return "Analyzing files..."
      } else if (processingStep === "mule_parsing") {
        return "Parsing files..."
      } else if (processingStep === "visualization") {
        return "Creating visualization..."
      } else if (processingStep === "llm_enhancing") {
        return "AI enhancing..."
      } else if (processingStep === "llm_complete") {
        return "Finalizing..."
      } else if (processingStep === "llm_failed") {
        return "Finishing..."
      } else {
        return "Processing..."
      }
    } else if (status === "completed") {
      return "Completed!"
    } else if (status === "failed") {
      return "Failed"
    } else if (status === "iflow_generation_failed") {
      return "iFlow generation failed"
    } else {
      return "Unknown status"
    }
  }

  // Get progress bar color based on status
  const getProgressBarColor = () => {
    if (status === "failed") {
      return "bg-red-500"
    } else if (processingStep === "llm_failed") {
      return "bg-company-orange-500"
    } else {
      return "bg-company-orange-600"
    }
  }

  const percentage = getProgressPercentage()
  const progressText = getProgressText()
  const progressBarColor = getProgressBarColor()

  // Should we show the LLM enhancement message?
  const showLLMMessage =
    isEnhancement &&
    status === "processing" &&
    (processingStep === "llm_enhancing" || (!processingStep && pollCount > 15))

  // Determine if this is a documentation upload workflow
  const isDocumentationWorkflow = status === "documentation_ready" ||
                                   status === "ready_for_iflow_generation" ||
                                   status === "generating_iflow" ||
                                   status === "iflow_generation_started" ||
                                   processingStep === "documentation_ready" ||
                                   processingStep === "iflow_generation" ||
                                   processingStep === "generating_iflow"

  return (
    <div className="bg-white shadow-sm rounded-lg p-4 space-y-3">
      {/* Compact Header */}
      <div className="flex justify-between items-center">
        <h3 className="text-md font-medium text-gray-800">
          {isDocumentationWorkflow ? "Processing Status" : "Generation Progress"}
        </h3>
        <div className="flex items-center text-gray-500 text-xs">
          <Clock className="h-3 w-3 mr-1" />
          <span>{elapsedTime}</span>
        </div>
      </div>

      {/* Compact Workflow Steps for Documentation Upload */}
      {isDocumentationWorkflow && (
        <div className="flex items-center space-x-2 text-xs">
          {/* Step 1: Document Upload */}
          <div className="flex items-center">
            <div className="w-5 h-5 bg-green-500 text-white rounded-full flex items-center justify-center text-xs">
              ✓
            </div>
            <span className="ml-1 text-green-600 font-medium">Uploaded</span>
          </div>

          {/* Connector 1 */}
          <div className="flex-1 h-px bg-gray-300 relative">
            <div className={`h-full transition-all duration-500 ${
              status === "generating_iflow" || status === "iflow_generation_started" || status === "completed" ||
              processingStep === "iflow_generation" || processingStep === "generating_iflow" || deploymentStatus
                ? "bg-blue-500" : "bg-gray-300"
            }`} style={{
              width: (status === "documentation_ready" || status === "ready_for_iflow_generation") &&
                     !(status === "generating_iflow" || status === "iflow_generation_started" ||
                       processingStep === "iflow_generation" || processingStep === "generating_iflow")
                ? "0%" : "100%"
            }} />
          </div>

          {/* Step 2: iFlow Generation */}
          <div className="flex items-center">
            <div className={`w-5 h-5 rounded-full flex items-center justify-center text-xs ${
              status === "generating_iflow" || status === "iflow_generation_started" ||
              processingStep === "iflow_generation" || processingStep === "generating_iflow"
                ? "bg-blue-500 text-white animate-pulse"
                : status === "completed" || deploymentStatus
                ? "bg-green-500 text-white"
                : "bg-gray-300 text-gray-600"
            }`}>
              {(status === "completed" || deploymentStatus) ? "✓" :
               (status === "generating_iflow" || status === "iflow_generation_started" ||
                processingStep === "iflow_generation" || processingStep === "generating_iflow") ? "⚡" : "2"}
            </div>
            <span className={`ml-1 font-medium ${
              status === "generating_iflow" || status === "iflow_generation_started" ||
              processingStep === "iflow_generation" || processingStep === "generating_iflow"
                ? "text-blue-600"
                : status === "completed" || deploymentStatus
                ? "text-green-600"
                : "text-gray-500"
            }`}>
              {(status === "completed" || deploymentStatus) ? "Generated" :
               (status === "generating_iflow" || status === "iflow_generation_started" ||
                processingStep === "iflow_generation" || processingStep === "generating_iflow") ? "Generating" : "Pending"}
            </span>
          </div>

          {/* Connector 2 - Only show if iFlow is generated */}
          {(status === "completed" || deploymentStatus) && (
            <>
              <div className="flex-1 h-px bg-gray-300 relative">
                <div className={`h-full transition-all duration-500 ${
                  deploymentStatus === "deploying" || deploymentStatus === "completed"
                    ? "bg-blue-500" : "bg-gray-300"
                }`} style={{
                  width: deploymentStatus ? "100%" : "0%"
                }} />
              </div>

              {/* Step 3: Deployment */}
              <div className="flex items-center">
                <div className={`w-5 h-5 rounded-full flex items-center justify-center text-xs ${
                  deploymentStatus === "deploying"
                    ? "bg-blue-500 text-white animate-pulse"
                    : deploymentStatus === "completed"
                    ? "bg-green-500 text-white"
                    : "bg-gray-300 text-gray-600"
                }`}>
                  {deploymentStatus === "completed" ? "✓" :
                   deploymentStatus === "deploying" ? "" : "3"}
                </div>
                <span className={`ml-1 font-medium ${
                  deploymentStatus === "deploying"
                    ? "text-blue-600"
                    : deploymentStatus === "completed"
                    ? "text-green-600"
                    : "text-gray-500"
                }`}>
                  {deploymentStatus === "completed" ? "Deployed" :
                   deploymentStatus === "deploying" ? "Deploying" : "Deploy"}
                </span>
              </div>
            </>
          )}
        </div>
      )}

      {/* Compact Progress Bar */}
      <div className="relative h-4 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full ${progressBarColor} transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
        <div className="absolute inset-0 flex items-center justify-center text-xs font-medium text-gray-700">
          {progressText}
        </div>
      </div>

      {/* Compact Status Message */}
      {statusMessage && (
        <div className={`p-2 rounded text-xs ${
          status === "failed" || status === "iflow_generation_failed"
            ? "bg-red-50 text-red-700"
            : status === "completed"
            ? "bg-green-50 text-green-700"
            : "bg-blue-50 text-blue-700"
        }`}>
          <div className="flex items-center gap-2">
            {(status === "processing" || status === "generating_iflow" || status === "iflow_generation_started") && (
              <div className="animate-spin rounded-full h-3 w-3 border-2 border-current border-t-transparent" />
            )}
            <span>{statusMessage}</span>
          </div>

          {/* Show additional progress details for iFlow generation */}
          {(status === "generating_iflow" || status === "iflow_generation_started") && (
            <div className="mt-2 text-xs">
              <div className="flex items-center gap-1 opacity-80">
                <span>⚡</span>
                <span>AI is analyzing your integration requirements and generating components...</span>
              </div>
              <div className="mt-1 opacity-60">
                This process typically takes 2-5 minutes depending on complexity
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ProgressTracker
