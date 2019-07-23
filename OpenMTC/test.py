# Example 12a: Making Requests with error handling

from openmtc_onem2m.client.http import OneM2MHTTPClient
from openmtc_onem2m.transport import OneM2MRequest, OneM2MErrorResponse
from openmtc.exc import OpenMTCError
from openmtc_onem2m.model import AE,Group

client = OneM2MHTTPClient("http://localhost:8000", False)
def request():
 tmp_app = AE(labels=["foo", "bar", "coffee"])
 my_app = AE(App_ID="myApp",
                labels=["keyword1", "keyword3"],
                resourceName="MYAPP3",
                requestReachability=False)
 memberList =[]
 memberList.append("onem2m/MYAPP1")
 memberList.append("onem2m/MYAPP2")
 memberList.append("onem2m/MYAPP2")
 memberList.append("onem2m/MYAPP3")
 memberList.append("onem2m/MYAPP3")
 memGroup = []
 memGroup.append("onem2m/grp1")

 my_group2 = Group(labels=["keyword1", "keyword2"],resourceName="grp2",memberType=9,maxNrOfMembers=3,memberIDs=memGroup,consistencyStrategy=3)
 my_group = Group(labels=["keyword1", "keyword2"],memberType=2,resourceName="grp1",maxNrOfMembers=4,memberIDs=memberList,consistencyStrategy=3)
 try:
     print my_group.memberIDs
     #onem2m_request = OneM2MRequest("create", to="onem2m", ty=AE, pc=my_app)
     onem2m_request = OneM2MRequest("create", to="onem2m", ty=Group, pc=my_group)
     #onem2m_request = OneM2MRequest("create", to="onem2m", ty=Group, pc=my_group2)
     #onem2m_request = OneM2MRequest("retrieve", to="onem2m/group-EhiWIDf6h4CpsUTv")
     #onem2m/group-sTJ25bw8fyGNLkoY
     #onem2m_request = OneM2MRequest("update", to="onem2m/MYAPP2", ty=AE, pc=tmp_app)
     promise= client.send_onem2m_request(onem2m_request)
     onem2m_response = promise.get()
     print onem2m_response.content
     '''
   
     onem2m_request = OneM2MRequest("retrieve", to="onem2m")

    onem2m_request = OneM2MRequest("create", to="onem2m", ty=AE, pc=my_app)
  
    onem2m_request3 = OneM2MRequest("create", to="onem2m", ty=Group, pc=my_group)

    '''
 except OneM2MErrorResponse as e:
    print "CSE reported an error:", e
    raise
 except OpenMTCError as e:
    print "Failed to reach the CSE:", e
    raise
 else:
    pass

# no exception was raised, the method returned normally.
 print onem2m_response
#>>> onem2m
 print onem2m_response.response_status_code
#>>> STATUS(numeric_code=2000, description='OK', http_status_code=200)
 print onem2m_response.content
#>>> CSEBase(path='None', id='cb0')
 '''
 client.port = 18000
 onem2m_request = OneM2MRequest("retrieve", to="~/mn-cse-1/onem2m")
 onem2m_response = client.send_onem2m_request(onem2m_request).get()
 print "---> Request to: http://localhost:18000" + "/" + onem2m_request.to
 print onem2m_response
 # >>> ~/mn-cse-1/onem2m
 print onem2m_response.response_status_code
 # >>> STATUS(numeric_code=2000, description='OK', http_status_code=200)
 print onem2m_response.content
 # >>> CSEBase(path='None', id='cb0')
'''
request()
