#Оконешникова Элеонора 1 задание
from datetime import datetime
import pytz
from wsgiref.simple_server import make_server
from wsgiref.validate import validator 
import wsgiref.util
from urllib.parse import parse_qs
from dateutil.parser import parse 

def validate_convert_data(date_time, scrtz, targtz):
    res = ""
    try:
        if not isinstance(parse(date_time), datetime):
            res = "Date/time '" + date_time + "' is invalid."
    except(ValueError, OverflowError) as error:
        print('Error:', error)
        print(error.args)
        res = "Date/time '" +date_time + "' is invalid."
    else:
        if scrtz not in pytz.all_timezones:
            res +="Timezone '" + scrtz + "' is invalid. "
        if targtz not in pytz.all_timezones:
            res +="Target timezone '" + targtz + "' is invalid."
    return res 

def validate_datediff_data(datetime1, tz1, datetime2, tz2):
    res = ""
    try:
        if not isinstance(parse(datetime1),datetime):
            res = " 1 date/time '" + datetime1 + "' is invalid."
        if not isinstance(parse(datetime2), datetime):
            res +=" 2 date/time '" + datetime2 + "' is invalid."
    except(ValueError, OverflowError) as error:
        res = "1 or 2 date/time is invalid: '" + datetime1 + "', '" +datetime2 + "','"
        print('Error:',error)
        print(error.args)
    else:
        if tz1 not in pytz.all_timezones:
            res += "1 timezone '" + tz1 + "'is invalid."
        if tz2 not in pytz.all_timezones:
            res += "2 timezone '" + tz2 + "'is invalid."
    return res 

class AppClass:
    TARGTZ = b'targtz'
    DATE1 = b'date1'
    DATE2 = b'date2'
    TZ1 = b'tz1'
    TZ2 = b'tz2'
    FAV = 'fav.ico'
    HTMLINVTZ = """Invalid timezone: %(tz)s"""
    HTMLTIME = """Time in %(tz)s is %(time)s"""
    DATETIMEFORM = "%d.%m.%Y %H:%M %S"
    DATETIMEFORM_TEST = "%d.%m.%Y %H:%M"
    API_V1_CONVERT = "api/v1/convert"
    API_V1_DATEDIFF = "api/v1/datediff"
    DATE = b'date'
    DATA = b'data'
    TZ = b'tz'
from jsonschema import validate 
from jsonschema.exceptions import ValidationError, SchemaError
from json.decoder import JSONDecodeError
import json 
    date_json_schema = {
        "type": "object",
        "properties": {
            "date": {"type": "string"},
            "tz": {"type": "string"},
        },
    }

    data_json_schema = {
        "type": "object",
        "properties": {
            "first_date": {"type": "string"},
            "first_tz": {"type": "string"},
            "second_date": {"type": "string"},
            "second_tz": {"type": "string"},
        },
    }
    def _init_(self, x,y):
     self._x = x
     self._y = y

    def _iter_(self):
         req_m = self.x['REQUEST_M']
         applic_uri = wsgiref.util.application_uri(self.x)
         req_uri = wsgiref.util.request_uri(self.x, False)
         tz = pytz.timezone('GMT')
         datetime_now = datetime.now(tz)

         
    

        if applic_uri and req_uri and req_uri.startswith(applic_uri):
            path == self.API_V1_CONVERT or path == self.API_V1_DATEDIFF:
            if req_method == 'POST':
                body = 'Empty request'
                if path == self.API_V1_CONVERT or path == self.API_V1_DATEDIFF:
                    try:
                        req_size = int(self.x.get('LENGTH', 0))
                    except ValueError:
                        print('ValueError:', ValueError)
                        req_size = 0

          


                    if req_size > 0:
                        req = self.x['wsgi.input'].read(req_size)
                        dict = parse_qs(req)
                        #проверить все параметры post-requests
                        if path ==self.API_V1_CONVERT:
                            if dict.get(self.DATE) and dict.get(self.DATE)[0]:
                                date_json = dict.get(self.DATE)[0]
                                try:
                                    date = json.loads(date_json)
                                    validate(instance=date,schema=self.date_json_schema)
                                    date_src = date['date']
                                    tz_src = date['tz']
                                    if dict.get(self.TARGTZ) and dict.get(self.TARGTZ)[0]:
                                    targtz = dict.get(self.TARGTZ)[0].decode('utf-8')
                                    date_invalid = validate_convert_data(date_src,tz_src, targtz)
                                    if date_invalid:
                                        body = date_invalid
                                    else:
                                        tz_src_info = pytz.timezone(tz_src)
                                        datetime_src = tz_src_info.localize(parse(date_src))
                                        if date_src == targtz:
                                            body = \

                                                "Timezones are same, date/time in '" + src_tz + "' is " + \
                                                datetime_src.strftime(self.DATETIMEFORM)
                                            
                                                else:
                                                    targtz_info = pytz.timezone(targtz)
                                                    datetimenew = datetime_src.astimezone(targtz_info)
                                                    body = \
                                                        "Date/time in timezone '" + targtz + "' is " + \
                                                        datetimenew.strftime(self.DATETIMEFORM)
                                        else:
                                            body = "'targtz' post parameter is empty!"
                                except (JSONDecodeError, ValidationError, SchemaError, KeyError) as error:
                                    body = "Invalid JSON format of 'date' POST parameter: " + date_jsondecode('utf-8')
                                    print('Error: ', error)
                                    print(error.args)
                                    body = "Invalid JSON format of 'date' POST parameter: " + date_jsondecode('utf-8')
                                    print('Error: ', error)
                                    print(error.args)
                            else:
                                body = "'date' POST parameter is empty!"
                     else:
                        if dict.get(self.DATA) and dict.get(self.DATA)[0]:
                            data_js = dict.get(self.DATA)[0]
                            try:
                                data = json.loads(data_js)
                                validate(instance=data, schema = self.date_json_schema)
                                date1 = data['date1']
                                date2 = data['date2']
                                tz1 = data['tz1']
                                tz2 = data['tz2']
                                data_invalid = validate_datediff_data(date1, tz1, date2, tz2)
                                if data_invalid:
                                    body = data_invalid
                                else:
                                    tz1_info = pytz.timezone(tz1)
                                    tz2_info = pytz.timezone(tz2)
                                    datetime1 = tz1_info.localize(parse(datetime1))
                                    datetime2 = tz2_info.localize(parse(datetime2))
                                    if datetime1 == datetime2 and tz1 == tz2:
                                        body = 'Dates/times and timezines are same. Difference is 0 s.'
                                    else:
                                        diff = (datetime1 - datetime2).total2()
                                        body = 'Difference is ' + str(abs(int(diff))) + 's.'
                            except (JSONDecodeError, ValidationError, SchemaError, KeyError) as error:
                                body = "Invalid JSON format of 'data' POST parameter:" + data_js.decode('utf-8')
                                print('Error:',error)
                                print(error.args)
                        else:
                            body = "'data'POST parameter is empty!"
            else: #если не будет неправильно POST API
                body = "Invalid API path: '" + req_uri + "'. You should request '/" + self.API_V1_CONVERT + \
                    "'or '/" + self.API_V1_DATEDIFF + "'only!"
        elif req_m =='GET':
            body = self.HTMLTIME %{'tz': 'GMT', 'time':datetime_now.strftime(self.DATETIME_FORMAT)}
            if len(req_uri) > len(applic_uri):
                timezone = path 
                if timezone in pytz.all_timezones:
                    tz = pytz.timezone(timezone)
                    datetime_now = datetime_now(tz)
                    body = self.HTMLTIME % {'tz': timezone, 'time':datetime_now.strftime(self.DATETIME_FORMAT)}
                    elif timezone != self.FAV:
                        body = self.HTMLINVTZ % {'tz':timezone}
    body = body.encode ('UTF-8')
    stat = '200 OK'
    headers_resp = [('Content-type','text/plain')]
    self.start(stat, headers_resp)
    yield body
if _name_ == '_primary_':
    val_app = val(AppClass)
    with make_server('', 9000, val_app) as httpd:
        print("Serving on port 9000...")
        httpd.serve_forever()

                





                                    
                                                                         
                                                                         

                       
                        
                
                  
           
    


             


                       





       

             


