import psycopg2
from datetime import datetime
from datetime import date
import calendar

class Postgres:

  def __init__(self):
    self.conn = None;
  
  def open(self):
    try:
        self.conn = psycopg2.connect("dbname='hackathon' user='postgres' host='localhost' password='123456'")
    except:
        print ("I am unable to connect to the database")

  def insertOndeFoiRoubado(self, json):
    cur = self.conn.cursor()
    hashmap = {}

    for idx in range(len(json)):
      strDayOfWeek = calendar.day_name[datetime.now().weekday()];
      shift = self.shift(datetime.now().hour)
      strData = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      if json[idx]['created_at'] != None:
        idxEnd = json[idx]['created_at'].find('.')
        json[idx]['created_at'] = json[idx]['created_at'][:idxEnd]
        date = datetime.strptime(json[idx]['created_at'], '%Y-%m-%dT%H:%M:%S');
        shift = self.shift(date.hour)
        strData = date.strftime('%Y-%m-%d %H:%M:%S')
        strDayOfWeek = calendar.day_name[date.weekday()]
      json[idx]['created_at'] = strData
      json[idx]['day_of_week'] = strDayOfWeek
      json[idx]['shift'] = shift
      hashmap[json[idx]['created_at']]=json[idx]

    for k,violence in hashmap.items():
      violence['titulo']  = (violence['titulo'] if violence['titulo'] != None  else 'Não Informado')
      violence['registrou_bo']  = (str(violence['registrou_bo']) if str(violence['registrou_bo']) != None  else 'Não Informado')
      violence['valor_prejuizo']  = (violence['valor_prejuizo'] if violence['valor_prejuizo'] != None  else 'Não Informado')
      violence['bairro']  = (violence['bairro'] if violence['bairro'] != None  else 'Não Informado')
      violence['nome']  = (violence['nome'] if violence['nome'] != None  else 'Não Informado')
      violence['tipo_assalto_id']  = (str(violence['tipo_assalto_id']) if str(violence['tipo_assalto_id']) != None  else 'Não Informado')
      violence['descricao']  = (violence['descricao'] if violence['descricao'] != None  else 'Não Informado')
      violence['sexo']  = (str(violence['sexo']) if str(violence['sexo']) != None  else 'Não Informado')
      violence['endereco']  = (violence['endereco'] if violence['endereco'] != None  else 'Não Informado')
      violence['municipio_id']  = (str(violence['municipio_id']) if str(violence['municipio_id']) != None  else 'Não Informado')
      
      queryStr = "INSERT INTO violence_data(title, latitude, longitude, event_data, bulletin_occurrence,damage_value, neighborhood, county,name,type,description,sex,address,source,day_of_week,shift) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      try:
        cur.execute(queryStr,(violence['titulo'],str(violence['latitude']),str(violence['longitude']),violence['created_at'], violence['registrou_bo'],violence['valor_prejuizo'],violence['bairro'],violence['municipio_id'],violence['nome'],violence['tipo_assalto_id'],violence['descricao'],str(violence['sexo']),violence['endereco'],'ONDE_FOI_ROUBADO', violence['day_of_week'] ,violence['shift']))
        self.conn.commit()
      except psycopg2.Error as e:
        print(e)
    cur.close()

  def insertOndeTemTiro(self, json):
    cur = self.conn.cursor()
    for violence in json['rows']:
      descriptionArray = violence[0].split("#")
      strData = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      if descriptionArray[1] != None:
        date = datetime.strptime(descriptionArray[1], '%d/%m/%Y às %H:%M');
        strData = date.strftime('%Y-%m-%d %H:%M:%S')
        shift = self.shift(date.hour)
        strDayOfWeek = calendar.day_name[date.weekday()]
      types = self.convertToTypeOfVeolance(violence[2])
        
      queryStr = "INSERT INTO violence_data(title, latitude, longitude, event_data, bulletin_occurrence,damage_value, neighborhood, county,name,type,description,sex,address,source,day_of_week,shift) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      try: 
        cur.execute(queryStr,(descriptionArray[3],str(violence[4]),str(violence[5]),strData, 'Não Informado',0,violence[1].split(',')[1],'Não Informado','Não Informado',types,descriptionArray[3],'Não Informado',violence[1],'ONDE_TEM_TIRO', strDayOfWeek, shift))
        self.conn.commit()
      except psycopg2.Error as e:
        print(e)
    cur.close()
  
  def getType(self):
    cur = self.conn.cursor()
    cur.execute("select id, name from type_violence order by id asc");
    results = cur.fetchall()
    cur.close()
    return results;

  def getViolenceByType(self, type, size):
    cur = self.conn.cursor()
    strLimit = ("" if size == 0 else " limit " + str(size))
    cur.execute("select title, latitude, longitude, event_data, bulletin_occurrence,damage_value,"\
  " neighborhood, county,name,type,description,sex,address,source,day_of_week,shift,source"\
  " from violence_data where type="+type+" order by event_data desc"+ strLimit);
    results = cur.fetchall()
    cur.close()
    return results;
    
  def getAmountOfLost(self):
    cur = self.conn.cursor()
    cur.execute("select sum(damage_value) from violence_data");
    results = cur.fetchall()
    cur.close()
    return results;

  def getLostBySex(self):
    cur = self.conn.cursor()
    cur.execute("select sex, count(sex) from violence_data where sex='1' or sex='0' group by sex");
    results = cur.fetchall()
    cur.close()
    return results;
    
  def getViolenceGroupByType(self):
    cur = self.conn.cursor()
    cur.execute("select t.name, count(t.name) from violence_data v join type_violence t on v.type = t.id group by t.name");
    results = cur.fetchall()
    cur.close()
    return results;

  def getViolenceGroupByNeighborhood(self):
    cur = self.conn.cursor()
    cur.execute("select neighborhood, count(neighborhood) as qtd from violence_data where neighborhood != 'Rio de Janeiro'  group by neighborhood order by qtd desc;");
    results = cur.fetchall()
    cur.close()
    return results;

  def getVeolance(self, size):
    cur = self.conn.cursor()
    strLimit = ("" if size == 0 else " limit " + str(size))
    cur.execute("select title, latitude, longitude, event_data, bulletin_occurrence,damage_value, neighborhood, county,name,type,description,sex,address,source,day_of_week,shift,source from violence_data order by event_data desc"+ strLimit);
    results = cur.fetchall()
    cur.close()
    return results;

  def getVeolanceFilterByType(self, size, tipo):
    cur = self.conn.cursor()
    print(tipo)
    strLimit = ("" if size == 0 else " limit " + str(size))
    cur.execute("select title, latitude, longitude, event_data, bulletin_occurrence,damage_value, neighborhood, county,name,type,description,sex,address,source,day_of_week,shift,source from violence_data where type="+tipo+" order by event_data desc"+ strLimit);
    results = cur.fetchall()
    cur.close()
    return results;

  def shift(self, hour):
    if hour > 0 and hour < 6:
      return 'dawn'
    elif hour >=6  and hour < 12:
      return 'morning'
    elif hour >= 12 and hour < 18:
      return 'afternoon'
    else:
      return 'night'

  def convertToTypeOfVeolance(self, type ):
    if type == "Disparos Ouvidos" and type == "Tiroteio" :
      return 12
    elif type == "Arrastão":
      return 10
      
  def close(self):
    try:
      self.conn.close()
    except:
      print ("I am unable to connect to the database")
