from listener_twitter import TwStreamListener


print("***INICIE***")
sectores = ['Salud', 'Medio ambiente', 'Educación', 'Seguridad']
for nCount in range(0,len(sectores)):
    myStreamListener = TwStreamListener()
    myStreamListener.connect()
    LOCATION_BELLO = [-75.623604,6.303511,-75.493611,6.373763]
    myStreamListener.run(sectores[nCount], LOCATION_BELLO)

print("***TERMINE***")
