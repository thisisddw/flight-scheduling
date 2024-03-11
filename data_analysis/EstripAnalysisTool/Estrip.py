import xml.etree.ElementTree as ET
from datetime import datetime

class Estrip:
## 由字符串生成Estrip类。

    
    ## 字符串样例
    ## XmlString = '<FlightData_Plan SOURCE="ATC_ESTRIP@ZWWW" Time="20240301200150"><PLAN IDENTIFIER="1709014332" TITLE="SFPL"><COM ACID="CUH2642" ADEP="ZHLY" ADES="ZWWW" CSTATUS="LND" DRWY="" ARWY="25" ETD="20240301154500" ATA="" REGID="B1570" SID="" GATE="17" SGATE="" DGATE="" ASSR="A7464" RFL="S1040" SFL="" TXT="" VIP_FLAG="" CSECTOR_NAME="TWR" DSECTOR_NAME="" AIRCRAFT="B738" ATIS="" ATCLD="" ATRDY="" ATPUS="" ATTAX="" ATLIN="" ATOVE="" CTOT="" COBT="" FREQUENCY="" ATBEG_DEICING="" ATRDY_DEICING="" ATEND_DEICING="" ATREQ_DEICING="" DELAY="" WAY_EXIT="" DCL_STATUS="0" CIXU="" MODE_APP="ILS/DME" MODE_PUS="" ATLND="20240301200150" ATREQ="" ATSTR="" AREA_DEICING_ID="0" RVSM_FLAG="W" TURB="M" DCATENTERAREA="" DCATEXITAREA="" DCATENTERAREAHLD="" DCATEXITAREAHLD="" SPCTST="" DCCSTAT="" ROUTE_TAX="" BOUND_TAX="" HDRCT="" MODCTOT="" TAXWAY="" ICEFLAG="0" ATYPE="2"/></PLAN></FlightData_Plan>'
    


    def __init__(self, XmlString):
        root = ET.fromstring(XmlString)        

        self.Time = root.find('.').get('Time')
        self.PlanID = root.find('./PLAN').get('IDENTIFIER')

        planData = root.find('.//COM')
        self.ACID = planData.get('ACID')
        self.AIRCRAFT = planData.get('AIRCRAFT')
        self.TURB = planData.get("TURB")
        self.DRWY = planData.get('DRWY')
        self.ARWY = planData.get('ARWY')
        self.GATE = planData.get("GATE")
        self.ATPUS = planData.get("ATPUS")
        self.ATLIN = planData.get("ATLIN")
        self.CTOT = planData.get("CTOT")
        self.COBT = planData.get("COBT")
        self.ATBEG_DEICING = planData.get("ATBEG_DEICING")
        self.ATEND_DEICING = planData.get("ATEND_DEICING")
        self.AREA_DEICING_ID = planData.get("AREA_DEICING_ID")

        if (self.ATPUS and self.ATLIN):
            self.TaxiTime = str(datetime.strptime(self.ATLIN, "%Y%m%d%H%M%S") - datetime.strptime(self.ATPUS, "%Y%m%d%H%M%S"))
        else: 
            self.TaxiTime = ""



    def getEstrip(self):
        # Return Time; PlanID; ACID; AIRCRAFT; TURB; DRWY; ARWY; GATE; ATPUS; ATLIN; CTOT; COBT; ATBEG_DEICING; ATEND_DEICING; AREA_DEICING_ID; TaxiTime
        # Such as 20240308092314; 1709022145; DKH1256; A20N; M; 25; ; 9; 20240308083134; 20240308084901; 20240308084500; 20240308083200; ; ; 0; 0:17:27
        EstripString = f"{self.Time}; {self.PlanID}; {self.ACID}; {self.AIRCRAFT}; {self.TURB}; {self.DRWY}; {self.ARWY}; {self.GATE}; {self.ATPUS}; {self.ATLIN}; {self.CTOT}; {self.COBT}; {self.ATBEG_DEICING}; {self.ATEND_DEICING}; {self.AREA_DEICING_ID}; {self.TaxiTime}; "
        return EstripString

    def printEstripWithName(self):
        # Print like this: "Time:20240308092314; PlanID:1709022145; ACID:DKH1256; AIRCRAFT:A20N; TURB:M; DRWY:25; ARWY:; GATE:9; ATPUS:20240308083134; ATLIN:20240308084901; CTOT:20240308084500; COBT:20240308083200; ATBEG_DEICING:; ATEND_DEICING:; AREA_DEICING_ID: 0; TaxiTime:0:17:27; "
        print(f"Time:{self.Time}; PlanID:{self.PlanID}; ACID:{self.ACID}; AIRCRAFT:{self.AIRCRAFT}; TURB:{self.TURB}; DRWY:{self.DRWY}; ARWY:{self.ARWY}; GATE:{self.GATE}; ATPUS:{self.ATPUS}; ATLIN:{self.ATLIN}; CTOT:{self.CTOT}; COBT:{self.COBT}; ATBEG_DEICING:{self.ATBEG_DEICING}; ATEND_DEICING:{self.ATEND_DEICING}; AREA_DEICING_ID: {self.AREA_DEICING_ID}; TaxiTime:{self.TaxiTime}; ")      

    def printEstrip(self, withTitle):
        # withTitle is True or False.
        # print like this: Time; PlanID; ACID; AIRCRAFT; TURB; DRWY; ARWY; GATE; ATPUS; ATLIN; CTOT; COBT; ATBEG_DEICING; ATEND_DEICING; AREA_DEICING_ID; TaxiTime; 
        #                  20240308092314; 1709022145; DKH1256; A20N; M; 25; ; 9; 20240308083134; 20240308084901; 20240308084500; 20240308083200; ; ; 0; 0:17:27
        if withTitle:
            print(f"Time; PlanID; ACID; AIRCRAFT; TURB; DRWY; ARWY; GATE; ATPUS; ATLIN; CTOT; COBT; ATBEG_DEICING; ATEND_DEICING; AREA_DEICING_ID; TaxiTime; ")
        print(f"{self.Time}; {self.PlanID}; {self.ACID}; {self.AIRCRAFT}; {self.TURB}; {self.DRWY}; {self.ARWY}; {self.GATE}; {self.ATPUS}; {self.ATLIN}; {self.CTOT}; {self.COBT}; {self.ATBEG_DEICING}; {self.ATEND_DEICING}; {self.AREA_DEICING_ID}; {self.TaxiTime}")

