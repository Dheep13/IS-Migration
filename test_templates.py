#!/usr/bin/env python3
"""
Test if the templates are accessible
"""

import sys
sys.path.append('BoomiToIS-API')

try:
    from enhanced_iflow_templates import EnhancedIFlowTemplates
    templates = EnhancedIFlowTemplates()
    
    print('✅ SFTP template exists:', hasattr(templates, 'sftp_receiver_participant_template'))
    print('✅ SuccessFactors template exists:', hasattr(templates, 'successfactors_receiver_participant_template'))
    print('✅ Request-reply template exists:', hasattr(templates, 'request_reply_template'))
    
    # Test calling the methods
    try:
        sftp_result = templates.sftp_receiver_participant_template()
        print('✅ SFTP template callable:', 'definition' in sftp_result)
    except Exception as e:
        print('❌ SFTP template error:', e)
    
    try:
        sf_result = templates.successfactors_receiver_participant_template()
        print('✅ SuccessFactors template callable:', 'definition' in sf_result)
    except Exception as e:
        print('❌ SuccessFactors template error:', e)
        
    try:
        rr_result = templates.request_reply_template("test_id", "test_name")
        print('✅ Request-reply template callable:', len(rr_result) > 0)
    except Exception as e:
        print('❌ Request-reply template error:', e)

except Exception as e:
    print('❌ Import error:', e)
