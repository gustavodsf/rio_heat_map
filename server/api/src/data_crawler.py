import urllib3
import json
from api.src.postgre import Postgres


class DataCrawler:

  def getData(self):
    jsonOndeFoiRoubado = self.getJsonFromOndeFoiRoubado()
    jsonOndeTemTiro = self.getJsonFromOnteTemTiro()
    postgre = Postgres()
    postgre.open()
    postgre.insertOndeFoiRoubado(jsonOndeFoiRoubado)
    postgre.insertOndeTemTiro(jsonOndeTemTiro)
    postgre.close()

  def getJsonFromOndeFoiRoubado(self):
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://www.ondefuiroubado.com.br/rio-de-janeiro/RJ');
    htmlData = str(r.data.decode('utf-8'))
    idxStart = htmlData.find('OndeFuiRoubado.Views.CrimesIndexView.initialize')
    idxEnd = htmlData.find('OndeFuiRoubado.PoliceStations')
    htmlData = htmlData[idxStart:idxEnd]
    htmlData = htmlData.replace('OndeFuiRoubado.Views.CrimesIndexView.initialize(','')
    htmlData = htmlData.strip()
    htmlData = htmlData.replace(');\\n  });\\n\\n  document.addEventListener(\\\'onMainMapLoad\\\', function(data) {\\n','')
    htmlData = htmlData.strip()
    htmlData = htmlData.replace("document.addEventListener('onMainMapLoad', function(data) {",'')
    htmlData = htmlData.replace("\n","")
    htmlData = htmlData.replace(");  });","")
    return json.loads(htmlData)

  def getJsonFromOnteTemTiro(self):
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://www.googleapis.com/fusiontables/v1/query?sql=SELECT%20*%20FROM%201HaQhL95pS0XhFQcifZ6fzKifuCXVdFxl-caH0zDf&key=AIzaSyC1CNeSPJOm5mPzk3kTrXuHJgG5vJP9Tgo');
    htmlData = str(r.data.decode('utf-8'))
    htmlData = htmlData.replace("\\n","#")
    return json.loads(htmlData)
