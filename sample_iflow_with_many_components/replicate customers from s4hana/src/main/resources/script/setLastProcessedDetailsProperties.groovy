/* Refer the link below to learn more about the use cases of script.
https://help.sap.com/viewer/368c481cd6954bdfa5d0435479fd4eaf/Cloud/en/148851bf8192412cba1f9d2c17f4bd25.html

If you want to know more about the SCRIPT APIs, refer the link below
https://help.sap.com/doc/a56f52e1a58e4e2bac7f7adbf45b2e26/Cloud/en/index.html */
import com.sap.gateway.ip.core.customdev.util.Message;
import java.util.HashMap;

import java.util.regex.*;

import groovy.xml.*;
import java.util.HashMap;
def Message processData(Message message) {
    //Properties
    def properties = message.getProperties();
    def lastProcessedVariable = properties.get("p_LastProcessedVariableValue");
    def initialStartDate = properties.get("p_InitialStartTime");
    
    def lastProcessedCreationDate = initialStartDate;
    def lastProcessedCreationTime = 'PT00H00M00S';
    def lastProcessedCreatedCustomerId = '0';
    def lastProcessedModifyDate = initialStartDate;
    def lastProcessedModifyTime = 'PT00H00M00S';
    def lastProcessedModifiedCustomerId = '0';
    
    if(lastProcessedVariable){
        def variableValues = lastProcessedVariable.tokenize("|");
        lastProcessedCreationDate = variableValues[0];
        lastProcessedCreationTime = variableValues[1];
        lastProcessedCreatedCustomerId = variableValues[2];
        lastProcessedModifyDate = variableValues[3];
        lastProcessedModifyTime = variableValues[4];
        lastProcessedModifiedCustomerId = variableValues[5];
        
    }
    
    message.setProperty("p_LastProcessedCreationDate", lastProcessedCreationDate);
    message.setProperty("p_LastProcessedCreationTime", lastProcessedCreationTime);
    message.setProperty("p_LastProcessedCreatedCustomerId", lastProcessedCreatedCustomerId);
    message.setProperty("p_LastProcessedModifyDate", lastProcessedModifyDate);
    message.setProperty("p_LastProcessedModifyTime", lastProcessedModifyTime);
    message.setProperty("p_LastProcessedModifiedCustomerId", lastProcessedModifiedCustomerId);
    
    return message;
}