import com.sap.it.api.mapping.*;

def String getCustomerEmail(String emailIsDefaultField, String value, MappingContext context)
{
    if(emailIsDefaultField != null && 
	emailIsDefaultField.trim().length() > 0 && 
	value != null && 
	value.trim().length() > 0 &&
	emailIsDefaultField == 'true'){
		
		return value;
		   
    }
 	
	return "";
}
//Add Output parameter to assign the output value.
def void getFirstValueInContext(String[] values, Output output, MappingContext context) {
        output.addValue(values[0]);
}