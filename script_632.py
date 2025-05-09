import cgi
import os,sys
import logging
import json
WORKLOAD_LOG_ZIP_ARCHIVE_FILE_NAME = "workload_log_{}.zip"
class LogFileJson:
    """ Defines format to upload log file in harness
    Arguments:
    itrLogPath : log path provided by harness to store log data
    logFileType : Type of log file defined in api.agentlogFileType
    workloadID [OPTIONAL] : workload id, if log file is workload specific
    """
    def __init__(self, itrLogPath, logFileType, workloadID = None):
        self.itrLogPath = itrLogPath
        self.logFileType = logFileType
        self.workloadID = workloadID
    def to_json(self):
        return json.dumps(self.__dict__)
    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)
class agentlogFileType():
    """ Defines various log file types to be uploaded by agent
    """
    WORKLOAD_ZIP_LOG = "workloadLogsZipFile"
try:
    logging.basicConfig(filename="/etc/httpd/html/logs/uploader.log",filemode='a', level=logging.ERROR)
except:
    pass
logger = logging.getLogger('log_upload_wsgi.py')
def application(environ, start_response):
    logger.debug("application called")
    if environ['REQUEST_METHOD'] == 'POST':
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=environ,
            keep_blank_values=True
        )
        resultBasePath = "/etc/httpd/html/vpresults"
        try:
            filedata = post["logfile"]
            metaData = post["logMetaData"]
            if metaData.value:
                logFileJson = LogFileJson.from_json(metaData.value)
            if not os.path.exists(os.path.join(resultBasePath, logFileJson.itrLogPath)):
                os.makedirs(os.path.join(resultBasePath, logFileJson.itrLogPath))
            if filedata.file:
                if (logFileJson.logFileType == agentlogFileType.WORKLOAD_ZIP_LOG):
                    filePath = os.path.join(resultBasePath, logFileJson.itrLogPath, WORKLOAD_LOG_ZIP_ARCHIVE_FILE_NAME.format(str(logFileJson.workloadID)))
                else:
                    filePath = os.path.join(resultBasePath, logFileJson.itrLogPath, logFileJson.logFileType)
                with open(filePath, 'wb') as output_file:
                    while True:
                        data = filedata.file.read(1024)
                        if not data:
                            break
                        output_file.write(data)
                body = u" File uploaded successfully."
                start_response(
                    '200 OK',
                    [
                        ('Content-type', 'text/html; charset=utf8'),
                        ('Content-Length', str(len(body))),
                    ]
                )
                return [body.encode('utf8')]
        except Exception as e:
            logger.error("Exception {}".format(str(e)))
            body = u"Exception {}".format(str(e))
    elif environ['REQUEST_METHOD'] == 'OPTIONS':
        PAYLOAD
        body = u"Invalid request"
    else:
        logger.error("Invalid request")
        body = u"Invalid request"
    start_response(
        '400 fail',
        [
            ('Content-type', 'text/html; charset=utf8'),
            ('Content-Length', str(len(body))),
        ]
    )
    return [body.encode('utf8')]