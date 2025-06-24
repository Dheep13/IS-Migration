/* Refer the link below to learn more about the use cases of script.
https://help.sap.com/viewer/368c481cd6954bdfa5d0435479fd4eaf/Cloud/en/148851bf8192412cba1f9d2c17f4bd25.html

If you want to know more about the SCRIPT APIs, refer the link below
https://help.sap.com/doc/a56f52e1a58e4e2bac7f7adbf45b2e26/Cloud/en/index.html */
import com.sap.gateway.ip.core.customdev.util.Message;
import java.util.HashMap;
def Message processData(Message message) {
    //Properties
    def properties = message.getProperties();
    def lastProcessedCreationDate =  properties.get("p_CurrentExecutionCreationDate") ? properties.get("p_CurrentExecutionCreationDate") : properties.get("p_LastProcessedCreationDate");
    def lastProcessedCreationTime =  properties.get("p_CurrentExecutionCreationTime") ? properties.get("p_CurrentExecutionCreationTime") : properties.get("p_LastProcessedCreationTime");
    def lastProcessedCreatedCustomerId =  properties.get("p_CurrentExecutionCreatedCustomerId") ? properties.get("p_CurrentExecutionCreatedCustomerId") : properties.get("p_LastProcessedCreatedCustomerId");
    def lastProcessedModifyDate =  properties.get("p_CurrentExecutionModifyDate") ? properties.get("p_CurrentExecutionModifyDate") : properties.get("p_LastProcessedModifyDate");
    def lastProcessedModifyTime =  properties.get("p_CurrentExecutionModifyTime") ? properties.get("p_CurrentExecutionModifyTime") : properties.get("p_LastProcessedModifyTime");
    def lastProcessedModifiedCustomerId =  properties.get("p_CurrentExecutionModifiedCustomerId") ? properties.get("p_CurrentExecutionModifiedCustomerId") : properties.get("p_LastProcessedModifiedCustomerId");
    def creationVariablePart = lastProcessedCreationDate+"|"+lastProcessedCreationTime+"|"+lastProcessedCreatedCustomerId;
    def modifyVariablePart = lastProcessedModifyDate+"|"+lastProcessedModifyTime+"|"+lastProcessedModifiedCustomerId
    
    message.setProperty("p_LastProcessedVariableValue", creationVariablePart+"|"+modifyVariablePart);
    return message;
}