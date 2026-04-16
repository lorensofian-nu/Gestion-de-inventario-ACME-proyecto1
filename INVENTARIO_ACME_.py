import datetime
import json
from config import *
inventario_productos=[]
codigo=[]
productos_registrado=[]


bodegas={
    1:"norte",
    2:"centro",
    3:"oriente",
}

try:
    with open(ruta_historial):
        pass
except FileNotFoundError:
    with open(ruta_historial, "x"):
        pass
    
try:
    with open(ruta_inventario):
        pass
except FileNotFoundError:
    with open(ruta_inventario, "x"):
        pass
    

def registar_productos_json(datos):
    productos_registrado={     
    
        "productos registrados": datos
        }
    with open (ruta_registro, "w") as archivos:
        obj_json=json.dumps(productos_registrado)
        print("fggh:",type(obj_json))
        archivos.write(obj_json)
        return obj_json
        print("producto registrado en el inventario")
     
def ingresar_inventario_json():
    datos={
        "productos inventario":inventario_productos
    }
    with open (ruta_inventario,"w")as archivos:
        obj_json=json.dumps(datos)
        archivos.write(obj_json)
        print("inventario agregado a archivo json")

     
def productos_registro():
    datos_registro=[]
    
    producto = input("digite nombre del producto: ")
    codigo_producto = int(input("ingrese el codigo del producto: "))
    proveedor = input("digite el nombre del proveedor: ")
    
    productos_registrado={
        "producto":producto,
        "codigo":codigo_producto,
        "proveedor":proveedor
    }
    datos_registro.append(productos_registrado)
    
    registar_productos_json(datos_registro)
    
    
def inventario_ingresado():
    productos=[]
    print("---ingresar productos a inventario--- ")
    codigo=int(input("ingrese el codigo del producto:"))
    codigo_encontrado=False
    
    with open(ruta_registro)as archivos:
        productos=json.load(archivos)
        
    for  item in productos ["productos registrados"]:
        if item["codigo"]==codigo:
            codigo_encontrado=True
            break
    if codigo_encontrado:
            print("el codigo del producto si existe")
            print("---zonas de bodega disponibles---\n 1.Norte\n 2.Centro\n 3.oriente\n")
            bodega=int(input("ingrese la zona de la bodega:"))
            if bodega in bodegas:
                cantidad=int(input("ingrese la cantidad de producto: "))
                descripcion=input("ingrese la descripcion del producto: ")
                stock=int(input("ingrese el stock de productos: "))
                fecha=str(datetime.datetime.now())
                bodega_datos={
                    "cantidad":cantidad,
                    "descripcion":descripcion,
                    "stock":stock,
                    "codigo":codigo,
                    "bodega":bodegas[bodega]
                }
                
                inventario_productos.append(bodega_datos)
                lista_historial = []
                with open(ruta_historial, "r") as historial:
                    try:
                        lista_historial=json.load(historial)
                    except json.JSONDecodeError:
                        pass
                    else:
                        lista_historial.append({
                            "codigo":codigo,
                            "bodega":bodega,
                            "cantidad":cantidad,
                            "descripcion":descripcion,
                            "fecha":fecha,
                            "movimiento":"ingreso"
                        })
                with open(ruta_historial, "w") as historial:
                   historial.write(json.dumps(lista_historial))

            else:
                 print("zona de bodega no encontrada")
                
            print(f"el stock del producto es:,{stock}")
            print(f"fecha y hora actual:{fecha}")
            print("el producto se ingreso a inventario:")
    ingresar_inventario_json()
             
def sacar_productos():
    codigo=int(input("digite el codigo del producto que quiere reetirar:"))
    inventario = []
    
    with open(ruta_inventario)as archivos:
        try:
            inventario = json.load(archivos)
        except json.JSONDecodeError:
            pass
    codigo_encontrado=False 
    
    if inventario == []:
        return
    
    for items in inventario["productos inventario"]: 
        if items["codigo"]==codigo:
            codigo_encontrado=True
            print("zonas de bodega dsipónibles\n 1.Norte\n 2.Centro\n 3.oriente\n")
            bodega=int(input("digite la bodega en donde quiere retirar producto:"))
            cantidad_retirar=int(input("digite la cantidad que desea retirar:"))
            descripcion_retiro=(input("digite la descripcion del retiro: "))
            stock=items["stock"]
            if cantidad_retirar<=stock:
                items ["stock"]-=cantidad_retirar
                print(f"retiraste {cantidad_retirar}")
            with open (ruta_inventario,"w") as archivos:
                json.dump(inventario,archivos)
        else:
            print("la cantidad es invalida para hacer el retiro ")
def buscar_productos():
    print("---buscar productos---") 
    codigo=int(input("ingrese el codigo del producto que desea buscar:"))
    inventario=[]
    with open(ruta_inventario) as archivos:
        try:
            inventario=json.load(archivos)
        except json.JSONDecodeError:
            print("no hay productos en el inventario")
            pass
    codigo_encontrado=False
    for items in inventario["productos inventario"]:
        if items ["codigo"]==codigo:
            codigo_encontrado=True
            print ("---producto encontrado en inventario---")
            print(f"codigo:items{codigo},bodega:{items['bodega']},cantidad:{items['cantidad']},descripcion:{items['descripcion']},stock:{items['stock']}")
            
        
def historial_productos():
    print("---historial de productos de inventario---")
    codigo=int(input("ingrese el codigo:"))
    bodega=int(input("digite la bodega que quiere revisar:"))
    historial = []
    
    with open(ruta_historial) as archivo:
        try:
            historial = list(json.load(archivo))
        except json.JSONDecodeError:
            pass
    
    for item in historial:
        print(item)
    
    
def reporte_inventario():
    print("---reporte de inventario---")
    inventario=[]
    with open (ruta_inventario) as archivos:
        try:
            inventario=json.load(archivos)
        except json.JSONDecodeError:
            print("no hay productos en el inventario..")
            pass
    texto_reporte=""
    productos_totales={}
    for items in inventario["productos inventario"]:
        codigo=items['codigo']
        bodega=items['bodega']
        cantidad=items['cantidad']
        
        if codigo not in productos_totales:
            productos_totales[codigo]={
            "norte":0,
            "centro":0,
            "oriente":0,
            "total":0
        }
    productos_totales[codigo]['total']+=cantidad
    productos_totales[codigo][bodega]+=cantidad
     
    for codigo,datos in productos_totales.items():
         print(f"codigo del producto:{codigo}\n")
         print(f"cantidad total:{datos['total']}")
         print(f"norte:{datos['norte']}")
         print(f"centro:{datos['centro']}")
         print(f"oriente:{datos['oriente']}")
        
    texto_reporte+=(f"codigo del producto:{codigo},cantidad total:{datos['total']}norte:{datos['norte']},centro:{datos['centro']},oriente:{datos['oriente']}")
    guardar_archivo=input("quiere guardar el reporte en un archivo? si/no")
    if guardar_archivo.capitalize()=="SI":
        with open (ruta_reporte,"w")as archivo:
         archivo.write(texto_reporte)  
         print("su reporte se ha guardado en el archivo")
         
def tranferir_productos_bodegas():
    datos= ingresar_inventario_json()
    inventario=0
    codigo_producto=int(input("digite el codigo del producto:"))
    bodega_origen=int(input("digite la bodega de origen del producto:"))
    bodega_destino=int(input("ingrese el numero de la bodega a la que quiere tranferir el producto:"))
    cantidad=int(input("ingrese la cantidad del producto:"))
    
    with open(ruta_inventario)as archivos:
        inventario=json.load(archivos)
    print(inventario)
    for item in inventario:
        if item["codigo"]==codigo_producto and item["bodega"]==bodega_origen:
                if item["stock"]< cantidad:
                    print("no puedes retirar hay stock insuficiente")
                
                
        if ["stock"]>= cantidad:
            destino_encontrado=True
            for item in inventario:
               if item ["codigo"]==codigo and  item["bodega"]==bodega_destino:
                       destino_encontrado=item
                       break
        if destino_encontrado:
            destino_encontrado["stock"]+= cantidad
        else:
            inventario_productos.append({
                "bodega":bodega_destino,
                "stock":cantidad,
                "codigo":codigo,
                "descripcion":item["descripcion"]
            })
            ingresar_inventario_json()
            print("su producto fue tranferido a la nueva bodega")
        
    
    
    
while True:
    print("---BIENVENIDO AL GESTOR DE INVENTARIO ACME----")
    print("---MENU PRINCIPAL---:\n--1.registrar producto\n  --2.Ingresar inventario\n  --3.sacar producto de inventario\n  --4.Buscar producto\n  --5.historial de productos\n   --6.reporte\n  -- 7.salir\n  -- 8.regresar al inicio\n ----9.tranferir productos entre bodegas")       
    opciones=(input("ingrese la opcion que desea: "))   
      
    match opciones:   
        case "1":
            productos_registro()
            
        case "2":
            inventario_ingresado()
        
        case "3":
            sacar_productos()    
        
        case "4":
            buscar_productos() 
        
        case "5":
            historial_productos()
        case "6":
            reporte_inventario()
        case "7":
            print("ha salido del progrma")
            break
        case "8":
            print("regresando al menu principal")
            continue
        case "9":
            tranferir_productos_bodegas()
            
    
        
        
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    











