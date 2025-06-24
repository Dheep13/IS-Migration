import com.sap.it.api.mapping.*;

def String getProperty(String property_name, MappingContext context) {
    def propValue= context.getProperty(property_name) ? context.getProperty(property_name) : 'Default';
    return propValue;
}