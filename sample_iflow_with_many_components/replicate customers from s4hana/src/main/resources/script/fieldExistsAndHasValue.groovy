import com.sap.it.api.mapping.*;

def String ExistsAndHasValue(String Input)
{
       if (Input != null && Input.trim().length() > 0)
       {
             return true
       }
       else
       {
            return false
       }
}