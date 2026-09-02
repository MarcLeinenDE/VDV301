#!/usr/bin/env python3
"""EV-121: exact official Common V2.3 Deep Read executable evidence."""
from __future__ import annotations
import hashlib, tempfile
from pathlib import Path
from lxml import etree

XS='http://www.w3.org/2001/XMLSchema'; NS={'xs':XS}
COMMON='IBIS-IP_common_V2.3.xsd'; ENUMS='IBIS-IP_Enumerations_V2.2.xsd'
COMMON_BLOB='0d8926c4063c12de9a5e68b6f0addaab35a55dc1'; ENUMS_BLOB='2a23b512379b18e8f122ac1272cef8229fb86283'
class EvidenceError(RuntimeError): pass

def blob(b): return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
def need(v,m):
    if not v: raise EvidenceError(m)
    print('OK ',m)
def ct(r,n):
    x=r.find(f"xs:complexType[@name='{n}']",NS)
    if x is None: raise EvidenceError('missing complexType '+n)
    return x
def el(r,t,n): return ct(r,t).find(f".//xs:element[@name='{n}']",NS)
def occ(x,a): return x.get(a,'1')
def expect(r,t,n,typ=None,mi=None,ma=None):
    x=el(r,t,n); need(x is not None,f'{t}.{n} exists')
    if typ: need(x.get('type')==typ,f'{t}.{n} type={typ}')
    if mi: need(occ(x,'minOccurs')==mi,f'{t}.{n} minOccurs={mi}')
    if ma: need(occ(x,'maxOccurs')==ma,f'{t}.{n} maxOccurs={ma}')
    return x
def absent(r,t,n): need(el(r,t,n) is None,f'{t}.{n} absent')
def enum_values(r,n):
    x=r.find(f"xs:simpleType[@name='{n}']",NS)
    if x is None: raise EvidenceError('missing enum '+n)
    return {e.get('value') for e in x.findall('.//xs:enumeration',NS)}
def probe(s,label,xml,want):
    d=etree.fromstring(xml.encode()); got=bool(s.validate(d))
    if got!=want: raise EvidenceError(f'{label}: got {got}, expected {want}: {s.error_log.last_error}')
    print('OK ',label, 'VALID' if got else 'INVALID')

def static(c,e):
    inc=c.find('xs:include',NS); need(inc is not None and inc.get('schemaLocation')==ENUMS,'V2.3 includes exact Enumerations V2.2')
    expect(c,'InternationalTextType','Value','xs:string'); expect(c,'InternationalTextType','Language','xs:language')
    choices=ct(c,'NetexMode').findall('./xs:sequence/xs:choice',NS); need(len(choices)==2 and all(occ(x,'minOccurs')=='0' for x in choices),'NetexMode has two optional top-level choices')
    a=ct(c,'AdditionalAnnouncementStructure').find('.//xs:choice',NS); need(a is not None and occ(a,'minOccurs')=='0','AdditionalAnnouncement choice optional'); need([x.get('name') for x in a.findall('xs:element',NS)]==['ImmediateInformation','PeriodicalInformation','SpecificPoint'],'AdditionalAnnouncement branch names exact')
    expect(c,'ConnectionStructure','TransportMode',mi='0',ma='1'); expect(c,'ConnectionStructure','ConnectionMode',mi='0',ma='1')
    need(ct(c,'DataAcceptedResponseStructure').find('.//xs:choice',NS) is not None,'DataAcceptedResponse uses xs:choice')
    for t,n in [('DataVersionListStructure','DataVersion'),('DeviceSpecificationWithStateListStructure','DeviceSpecificationWithState'),('ServiceIdentificationWithStateListStructure','ServiceIdentificationWithState'),('ServiceSpecificationWithStateListStructure','ServiceSpecificationWithState')]: expect(c,t,n,mi='0',ma='unbounded')
    expect(c,'JourneyStopInformationStructure','Announcement',mi='0',ma='1'); expect(c,'JourneyStopInformationStructure','FareZone',mi='0',ma='1')
    expect(c,'StopInformationRequestStructure','StopName',mi='0',ma='unbounded'); absent(c,'StopInformationRequestStructure','ArrivalExpected'); absent(c,'StopInformationRequestStructure','DepartureExpected')
    expect(c,'StopInformationStructure','ArrivalExpected','IBIS-IP.dateTime',mi='0',ma='1'); expect(c,'StopInformationStructure','DepartureExpected','IBIS-IP.dateTime',mi='0',ma='1')
    for n in ['AdditionalTextMessage']+[f'AdditionalTextMessage{i}' for i in range(1,10)]: expect(c,'TripInformationStructure',n,'InternationalTextType',mi='0',ma='1')
    for n in ['RunNumber','PatternNumber','PathDestinationNumber']: expect(c,'TripInformationStructure',n,'IBIS-IP.int',mi='0',ma='1')
    for n in [f'AdditionalInformation{i}' for i in range(1,10)]: expect(c,'DisplayContentStructure',n,'InternationalTextType',mi='0',ma='unbounded')
    expect(c,'DisplayContentStructure','RunNumber','IBIS-IP.int',mi='0',ma='1'); expect(c,'UnsubscribeResponseStructure','Active',mi='1',ma='1')
    for t,g,b in [('BeaconPointStructure','Desciption','Description'),('TSPPointStructure','Desciption','Description'),('SubscribeRequestStructure','ReplyPath','Reply-Path'),('UnsubscribeRequestStructure','ReplyPath','Reply-Path'),('GlobalCardStatus','GlobalCardStausID','GlobalCardStatusID'),('ZoneType','FareZoneTypeName','FarezoneTypeName'),('LogMessageStructure','Message','MessageBody')]: expect(c,t,g); absent(c,t,b)
    for g in ['FareZoneID','FareZoneType','FareZoneLongName','FareZoneShortName']: expect(c,'FareZoneInformationStructure',g)
    for b in ['FarezoneID','FarezoneType','FarezoneLongName','FarezoneShortName']: absent(c,'FareZoneInformationStructure',b)
    expect(c,'ServiceIdentificationStructure','Service','ServiceSpecificationStructure'); absent(c,'ServiceIdentificationStructure','ServiceName')
    expect(c,'ServiceIdentificationWithStateListStructure','ServiceIdentificationWithState','ServiceIdentificationWithStateStructure',mi='0',ma='unbounded')
    expect(c,'ShortTripStopListStructure','ShortTripStop','ShortTripStopStructure',mi='1',ma='unbounded'); absent(c,'ShortTripStopListStructure','ShortTripStopList')
    checks=[('DeviceStateEnumeration','warning',None),('ServiceNameEnumeration','SystemMonitoringService','SystemDocumentationService'),('ServiceNameEnumeration','SystemMonitoringService','SystemManagementService'),('DoorCountingObjectClassEnumeration','WheelChair','Wheelchair'),('DoorCountingObjectClassEnumeration','Other','Others'),('GNSSTypeEnumeration','other','Other'),('TicketValidationEnumeration','valid','Valid'),('VehicleModeEnumeration','air','Air'),('RailSubmodeEnumeration','specialTrain','specialRail'),('AirSubmodeEnumeration','canalBarge',None),('FunicularSubmodeEnumeration','unknown','Unknown'),('TaxiSubmodeEnumeration','undefined','Undefined'),('TaxiSubmodeEnumeration','miniCab','minicab')]
    for t,p,b in checks:
        v=enum_values(e,t); need(p in v,f'{t} contains {p}')
        if b: need(b not in v,f'{t} excludes {b}')

def harness():
    roots={'I':'InternationalTextType','N':'NetexMode','A':'AdditionalAnnouncementStructure','C':'ConnectionStructure','D':'DataAcceptedResponseStructure','DL':'DataVersionListStructure','DSL':'DeviceSpecificationWithStateListStructure','SIL':'ServiceIdentificationWithStateListStructure','SSL':'ServiceSpecificationWithStateListStructure','J':'JourneyStopInformationStructure','R':'StopInformationRequestStructure','S':'StopInformationStructure','T':'TripInformationStructure','U':'UnsubscribeResponseStructure','F':'FareZoneInformationStructure','G':'GlobalCardStatus','L':'LogMessageStructure','SI':'ServiceIdentificationStructure','DS':'DeviceStateEnumeration','SN':'ServiceNameEnumeration','DC':'DoorCountingObjectClassEnumeration','GT':'GNSSTypeEnumeration','TV':'TicketValidationEnumeration','VM':'VehicleModeEnumeration','RS':'RailSubmodeEnumeration','AS':'AirSubmodeEnumeration','FS':'FunicularSubmodeEnumeration','TX':'TaxiSubmodeEnumeration'}
    return '\n'.join([f'<xs:schema xmlns:xs="{XS}" elementFormDefault="qualified">',f'<xs:include schemaLocation="{COMMON}"/>']+[f'<xs:element name="{k}" type="{v}"/>' for k,v in roots.items()]+['</xs:schema>'])
def intl(x='x'): return f'<Value>{x}</Value><Language>de</Language>'
def display(): return '<DisplayContent><LineInformation><LineRef><Value>L1</Value></LineRef></LineInformation><Destination><DestinationRef><Value>D1</Value></DestinationRef></Destination></DisplayContent>'
def stop(i): return f'<StopPoint><StopIndex><Value>{i}</Value></StopIndex><StopRef><Value>S{i}</Value></StopRef><StopName>{intl()}</StopName>{display()}</StopPoint>'
def connbase(): return '<StopRef><Value>S1</Value></StopRef><ConnectionRef><Value>C1</Value></ConnectionRef><ConnectionType>Interchange</ConnectionType>'

def executable(s):
    probe(s,'InternationalText flat','<I><Value>x</Value><Language>de</Language></I>',True); probe(s,'InternationalText PDF wrapper','<I><Value><Value>x</Value></Value><Language><Value>de</Value></Language></I>',False)
    probe(s,'empty NetexMode','<N/>',True); probe(s,'populated NetexMode','<N><PtMainMode>RailSubmode</PtMainMode><RailSubmode>local</RailSubmode></N>',True)
    probe(s,'AdditionalAnnouncement omitted choice','<A><AnnouncementRef><Value>A1</Value></AnnouncementRef></A>',True); probe(s,'AdditionalAnnouncement PDF-only branch','<A><AnnouncementRef><Value>A1</Value></AnnouncementRef><InformationAtSpecificPoint><PointRef><Value>P1</Value></PointRef><DistanceToPreviousPoint><Value>1</Value></DistanceToPreviousPoint></InformationAtSpecificPoint></A>',False)
    vb='<VehicleTypeRef><Value>V1</Value></VehicleTypeRef>'; cb=connbase(); probe(s,'Connection one TransportMode',f'<C>{cb}<TransportMode>{vb}</TransportMode></C>',True); probe(s,'Connection repeated TransportMode',f'<C>{cb}<TransportMode>{vb}</TransportMode><TransportMode>{vb}</TransportMode></C>',False)
    nm='<ConnectionMode><PtMainMode>RailSubmode</PtMainMode><RailSubmode>local</RailSubmode></ConnectionMode>'; probe(s,'Connection one ConnectionMode',f'<C>{cb}{nm}</C>',True); probe(s,'Connection repeated ConnectionMode',f'<C>{cb}{nm}{nm}</C>',False)
    data='<DataAcceptedResponseData><TimeStamp><Value>2026-01-01T00:00:00Z</Value></TimeStamp><DataAccepted><Value>true</Value></DataAccepted></DataAcceptedResponseData>'; err='<OperationErrorMessage><Value>err</Value></OperationErrorMessage>'; probe(s,'DataAccepted one branch',f'<D>{data}</D>',True); probe(s,'DataAccepted both branches',f'<D>{data}{err}</D>',False)
    for r in ['DL','DSL','SIL','SSL']: probe(s,f'{r} empty',f'<{r}/>',True)
    jb=f'<StopRef><Value>S1</Value></StopRef><StopName>{intl()}</StopName>{display()}'; ann='<Announcement><AnnouncementRef><Value>A1</Value></AnnouncementRef></Announcement>'; probe(s,'Journey one Announcement',f'<J>{jb}{ann}</J>',True); probe(s,'Journey repeated Announcement',f'<J>{jb}{ann}{ann}</J>',False)
    names=f'<StopName>{intl("a")}</StopName><StopName>{intl("b")}</StopName>'; probe(s,'Request repeated StopName',f'<R>{names}{display()}</R>',True); probe(s,'Request ArrivalExpected rejected',f'<R>{display()}<ArrivalExpected><Value>2026-01-01T10:00:00Z</Value></ArrivalExpected></R>',False); probe(s,'Request DepartureExpected rejected',f'<R>{display()}<DepartureExpected><Value>2026-01-01T10:00:00Z</Value></DepartureExpected></R>',False)
    probe(s,'StopInformation expected fields valid',f'<S><StopIndex><Value>1</Value></StopIndex><StopRef><Value>S1</Value></StopRef><StopName>{intl()}</StopName>{display()}<ArrivalExpected><Value>2026-01-01T10:00:00Z</Value></ArrivalExpected><DepartureExpected><Value>2026-01-01T10:01:00Z</Value></DepartureExpected></S>',True)
    seq=f'<StopSequence>{stop(1)}{stop(2)}</StopSequence>'; tb=f'<TripRef><Value>T1</Value></TripRef>{seq}'; m=f'<AdditionalTextMessage>{intl()}</AdditionalTextMessage>'; m1=f'<AdditionalTextMessage1>{intl()}</AdditionalTextMessage1>'; probe(s,'Trip base message once',f'<T>{tb}{m}</T>',True); probe(s,'Trip base message repeated',f'<T>{tb}{m}{m}</T>',False); probe(s,'Trip numbered message once',f'<T>{tb}{m1}</T>',True); probe(s,'Trip numbered message repeated',f'<T>{tb}{m1}{m1}</T>',False); probe(s,'Trip V2.3 numeric additions',f'<T>{tb}<RunNumber><Value>1</Value></RunNumber><PatternNumber><Value>2</Value></PatternNumber><PathDestinationNumber><Value>3</Value></PathDestinationNumber></T>',True)
    probe(s,'Unsubscribe Active present','<U><Active><Value>true</Value></Active></U>',True); probe(s,'Unsubscribe missing Active','<U/>',False)
    probe(s,'FareZone exact','<F><FareZoneID><Value>Z1</Value></FareZoneID></F>',True); probe(s,'Farezone PDF case','<F><FarezoneID><Value>Z1</Value></FarezoneID></F>',False); probe(s,'Global exact spelling','<G><GlobalCardStausID><Value>1</Value></GlobalCardStausID></G>',True); probe(s,'Global PDF spelling','<G><GlobalCardStatusID><Value>1</Value></GlobalCardStatusID></G>',False)
    for root,val,want in [('DS','warning',True),('SN','SystemMonitoringService',True),('SN','SystemDocumentationService',False),('SN','SystemManagementService',False),('DC','WheelChair',True),('DC','Wheelchair',False),('GT','other',True),('GT','Other',False),('TV','valid',True),('TV','Valid',False),('VM','air',True),('VM','Air',False),('RS','specialTrain',True),('RS','specialRail',False),('AS','canalBarge',True),('FS','unknown',True),('FS','Unknown',False),('TX','miniCab',True),('TX','minicab',False)]: probe(s,f'{root}={val}',f'<{root}>{val}</{root}>',want)

def main():
    repo=Path(__file__).resolve().parents[1]
    try:
        cb=(repo/COMMON).read_bytes(); eb=(repo/ENUMS).read_bytes(); need(blob(cb)==COMMON_BLOB,'exact official Common V2.3 blob'); need(blob(eb)==ENUMS_BLOB,'exact official Enumerations V2.2 blob'); c=etree.fromstring(cb); e=etree.fromstring(eb); static(c,e)
        with tempfile.TemporaryDirectory(prefix='vdv301_ev121_') as td:
            p=Path(td); (p/COMMON).write_bytes(cb); (p/ENUMS).write_bytes(eb); (p/'h.xsd').write_text(harness(),encoding='utf-8'); schema=etree.XMLSchema(etree.parse(str(p/'h.xsd'))); print('OK  EV-121 exact harness compiled'); executable(schema)
    except (OSError,etree.XMLSyntaxError,etree.XMLSchemaParseError,EvidenceError) as ex:
        print('FAILED: EV-121 Common V2.3 evidence check:',ex); return 1
    print('PASSED: EV-121 exact official Common V2.3 authority and Deep Read boundaries confirmed'); return 0
if __name__=='__main__': raise SystemExit(main())
