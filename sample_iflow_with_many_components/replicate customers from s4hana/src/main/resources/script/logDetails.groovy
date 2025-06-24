
import com.sap.gateway.ip.core.customdev.util.Message;
import groovy.json.JsonSlurper

def Message processData(Message message) {
   
    def body = message.getBody(String.class)
    def messageLog = messageLogFactory.getMessageLog(message);

    def jsonSlurper = new JsonSlurper();
    def jsonObject = jsonSlurper.parseText(body);

    def executionStatus = jsonObject['Execution Status'];
    def msg = jsonObject['Message'];
    def exceptionMessage = jsonObject['ExceptionMessage'];

    def details = "Execution Status: ${executionStatus}\n${msg}"
    details += exceptionMessage ? ":\n${exceptionMessage}" : "";
    
    if (messageLog != null) {
        // Add a custom header property to the message log
        messageLog.addCustomHeaderProperty("Execution Details", details);
    }

    return message
}