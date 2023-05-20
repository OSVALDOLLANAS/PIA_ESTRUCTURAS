import os
import openpyxl
import csv
import pandas as pd
import sqlite3
from sqlite3 import Error
import sys
biblioteca ={'ID':[],'TITULO':[],'AUTOR':[],'GENERO':[],
            'ANIO_PUBLICACION':[],'ISBN':[],'FECHA_ADQUISICION':[],'ID_GENERO':[],'ID_AUTOR':[]}
autor_id={'ID':[],'APELLIDOS':[],'NOMBRES':[]}
genero_id={'ID':[],'NOM_GENERO':[]}
guardado=""
try:
    biblioteca_existente=pd.read_csv('biblioteca.csv')
    print('El archivo biblioteca.csv ya existe')
except FileNotFoundError:
    biblioteca_existente=pd.DataFrame(biblioteca)
    biblioteca_existente.to_csv('biblioteca.csv')
    print('Se genero un archivo llamado biblioteca.csv vacia')
except Exception as e:
    print("Se produjo un error al cargar el archivo CSV:", str(e))

try:
    genero_id_existentes=pd.read_csv('genero_id.csv')
    print('El archivo genero_id.csv ya existe')
except FileNotFoundError:
    genero_id_existentes=pd.DataFrame(genero_id)
    genero_id_existentes.to_csv('genero_id.csv')
    print('Se genero un archivo llamado genero_id.csv vacia')
except Exception as e:
    print("Se produjo un error al cargar el archivo CSV:", str(e))

try:
    autor_id_existentes=pd.read_csv('autor_id.csv')
    print('El archivo autor_id.csv ya existe')
except FileNotFoundError:
    autor_id_existentes=pd.DataFrame(autor_id)
    autor_id_existentes.to_csv('autor_id.csv')
    print('Se genero un archivo llamado autor_id.csv vacia')
except Exception as e:
    print("Se produjo un error al cargar el archivo CSV:", str(e))

try:
    with sqlite3.connect('biblioteca.db') as conn:
        mi_cursor=conn.cursor()
        mi_cursor.execute("CREATE TABLE BIBLIOTECA(ID INTEGER PRIMARY KEY NOT NULL,TITULO TEXT NOT NULL, AUTOR TEXT NOT NULL, GENERO TEXT NOT NULL, ANIO_PUBLICACION INTEGER NOT NULL,\
                          ISBN TEXT NOT NULL, FECHA_ADQUISICION TEXT NOT NULL, ID_GENERO INTEGER NOT NULL, ID_AUTOR INTEGER NOT NULL, FOREIGN KEY(ID_AUTOR)\
                           REFERENCES AUTOR(ID_AUTOR), FOREIGN KEY(ID_GENERO) REFERENCES GENERO(ID_GENERO));")
        mi_cursor.execute("CREATE TABLE AUTOR (ID INTEGER PRIMARY KEY NOT NULL, APELLIDOS TEXT NOT NULL,NOMBRES TEXT NOT NULL);")
        mi_cursor.execute("CREATE TABLE GENERO(ID INTEGER PRIMARY KEY NOT NULL, NOM_GENERO TEXT NOT NULL);")
        print("La base de datos biblioteca.db fue creada")
except Error as e:
    print("La base de datos biblioteca.db ya existe")
except:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

while True:
    print("*"*40)
    print("****         MENU PRICIPAL         ****")
    opcion=int(input("[1]Registrar nuevo ejemplar\n[2]Consultas y reportes\n[3]Resgitrar un autor\n[4]Registrar un genero\n[5]Salir\nElija un opcion: "))
    print("*"*40)

    if opcion==1:
        print("*"*40)
        print("****  REGISTRO DE NUEVO EJEMPLEAR   ****")
        TITULO=input("Ingrese el titulo: ").upper()
        AUTOR=input(f"Indique el autor de {TITULO}: ").upper()
        GENERO=input(f"Indique el genero de {TITULO}: ").upper()
        ANIO_PUBLICACION=int(input(f"Indique el año de publicación de {TITULO}: "))
        ISBN=input(f"Indique el ISBN de {TITULO}: ").upper()
        FECHA_ADQUISICION=input(f"Indique la fecha de adquisición de {TITULO}: ").upper()
        ID_GENERO=int(input(f'Indique el ID de {GENERO}:'))
        ID_AUTOR=int(input(f'Indique el ID de {AUTOR}:'))
        ID=max(biblioteca['ID'],default=0)+1
        biblioteca['ID']=[ID]
        biblioteca['TITULO']=[TITULO]
        biblioteca['AUTOR']=[AUTOR]
        biblioteca['GENERO']=[GENERO]
        biblioteca['ANIO_PUBLICACION']=[ANIO_PUBLICACION]
        biblioteca['ISBN']=[ISBN]
        biblioteca['FECHA_ADQUISICION']=[FECHA_ADQUISICION]
        biblioteca['ID_GENERO']=[ID_GENERO]
        biblioteca['ID_AUTOR']=[ID_AUTOR]
        print("*"*40)
        
        try:
            with sqlite3.connect("Biblioteca.db") as conn:
                mi_cursor = conn.cursor()
                valores ={"ID":ID,"TITULO":TITULO,"AUTOR":AUTOR,"GENERO":GENERO,"ANIO_PUBLICACION":ANIO_PUBLICACION,"ISBN":ISBN,"FECHA_ADQUISICION":FECHA_ADQUISICION,\
                           "ID_GENERO":ID_GENERO,"ID_AUTOR":ID_AUTOR}
                mi_cursor.execute("INSERT INTO BIBLIOTECA(ID,TITULO,AUTOR,GENERO,ANIO_PUBLICACION,\
                                  ISBN,FECHA_ADQUISICION,ID_GENERO,ID_AUTOR) VALUES(:ID,:TITULO,:AUTOR,:GENERO,:ANIO_PUBLICACION,:ISBN,:FECHA_ADQUISICION,\
                                  :ID_GENERO,:ID_AUTOR)", valores)
                biblioteca_existente=pd.DataFrame(biblioteca)
                biblioteca_existente.to_csv('biblioteca.csv')
                print("Registro agregado exitosamente")
        except Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
        continue

    if opcion==2:
        while True:
            print(("*")*40)
            print("****      CONSULTAS Y REPORTES      ****")
            opcion_2=int(input("[1]Consulta de titulo\n[2]Reportes\n[3]Volver al menu de consultas y reportes\nElija una opcion:"))

            if opcion_2==1:
                while True:
                    print(("*")*40)
                    print("****      Consulta de titulo      ****")
                    print("*"*40)
                    opcion2_1=int(input("[1]Por titulo\n[2]Por ISBN\n[3]Volver al menu de consultas y reportes\nElija una opcion: "))
                    print("*"*40)
                    if opcion2_1==1:
                        conn=sqlite3.connect('biblioteca.db')
                        mi_cursor=conn.cursor()
                        mi_cursor.execute("SELECT ID,TITULO FROM BIBLIOTECA")
                        RECOPILACION=mi_cursor.fetchall()
                        DATA=pd.DataFrame(RECOPILACION,columns=['ID','TITULO'])
                        print("*"*40)
                        print(DATA)
                        print("*"*40)

                        conn=sqlite3.connect('biblioteca.db')
                        mi_cursor=conn.cursor()
                        mi_cursor.execute("SELECT*FROM BIBLIOTECA")
                        RECOPILACION=mi_cursor.fetchall()
                        DATA=pd.DataFrame(RECOPILACION,columns={'ID':[],'TITULO':[],'AUTOR':[],'GENERO':[],'ANIO_PUBLICACION':[],'ISBN':[],'FECHA_ADQUISICION':[],'ID_GENERO':[],\
                                                                'ID_AUTOR':[]})
                        print("Elija una opcion para obtener todos los datos del titulo: ")
                        TITULO=str(input()).upper()
                        datos_titulo=DATA.loc[DATA["TITULO"].isin([TITULO])]
                        print(datos_titulo)
                        continue

                    if opcion2_1==2:
                        conn=sqlite3.connect('biblioteca.db')
                        mi_cursor=conn.cursor()
                        mi_cursor.execute("SELECT ID,ISBN FROM BIBLIOTECA")
                        RECOPILACION=mi_cursor.fetchall()
                        DATA=pd.DataFrame(RECOPILACION,columns=['ID','ISBN'])
                        print("*"*40)
                        print(DATA)
                        print("*"*40)

                        conn=sqlite3.connect('biblioteca.db')
                        mi_cursor=conn.cursor()
                        mi_cursor.execute("SELECT*FROM BIBLIOTECA")
                        RECOPILACION=mi_cursor.fetchall()
                        DATA=pd.DataFrame(RECOPILACION,columns={'ID':[],'TITULO':[],'AUTOR':[],'GENERO':[],'ANIO_PUBLICACION':[],'ISBN':[],'FECHA_ADQUISICION':[],'ID_GENERO':[],\
                                                                'ID_AUTOR':[]})
                        print("Elija una opcion para obtener todos los datos del ISBN: ")
                        ISBN=str(input()).upper()
                        datos_titulo=DATA.loc[DATA["ISBN"].isin([ISBN])]
                        print(datos_titulo)
                        continue
                    if opcion2_1==3:
                        break

                continue
            if opcion_2==2:
                while True:
                    print("*"*40)
                    print("****            REPORTES            ****")
                    print("*"*40)
                    opcion2_2=int(input("[1]Catalago completo\n[2]Reporte por autor\n[3]Reporte por género\n[4]Por año de publicación\n[5]Volver al menú de reportes\nElija una opcion: "))
                    print("")
                    if opcion2_2==1:
                        while True:
                            print("*"*40)
                            conn=sqlite3.connect('biblioteca.db')
                            mi_cursor=conn.cursor()
                            mi_cursor.execute("SELECT*FROM BIBLIOTECA")
                            RECOPILACION=mi_cursor.fetchall()
                            DATA=pd.DataFrame(RECOPILACION,columns=['ID','TITULO','AUTOR','GENERO','ANIO_PUBLICACION','ISBN','FECHA_ADQUISICION','ID_GENERO','ID_AUTOR'])
                            print("*"*40)
                            print(DATA)
                            print("*"*40)
                            print(("*")*40)
                            print("****      Catalogo completo      ****")
                            opcion2_2_1=int(input("[1]Exportar reporte en formato CSV\n[2]Exportar reporte en formato MsExcel\n[3]No exportar nada\n Elija una opcion:"))
                            if opcion2_2_1==1:
                                DATA.to_csv('Catalago_completo.csv', index=False)
                                print('El archivo csv se nombro Catalago_completo.csv')
                                continue
                            if opcion2_2_1==2:
                                DATA.to_excel('Catalago_completo.xlsx', index=False)
                                print('El archivo xlsx se nombro Catalago_completo.xlsx')
                                continue
                            if opcion2_2_1==3:
                                break

                    if opcion2_2==2:
                        while True:
                            print("*"*40)
                            conn=sqlite3.connect('biblioteca.db')
                            mi_cursor=conn.cursor()
                            mi_cursor.execute("SELECT BIBLIOTECA.ID,BIBLIOTECA.ID_AUTOR,BIBLIOTECA.AUTOR FROM BIBLIOTECA JOIN AUTOR ON AUTOR.ID=BIBLIOTECA.ID_AUTOR")
                            RECOPILACION=mi_cursor.fetchall()
                            DATA=pd.DataFrame(RECOPILACION,columns=['ID','ID_AUTOR','AUTOR'])
                            print(DATA)
                            print("*"*40)
                            conn=sqlite3.connect('biblioteca.db')
                            mi_cursor=conn.cursor()
                            mi_cursor.execute("SELECT*FROM BIBLIOTECA")
                            RECOPILACION=mi_cursor.fetchall()
                            DATA=pd.DataFrame(RECOPILACION,columns={'ID':[],'TITULO':[],'AUTOR':[],'GENERO':[],'ANIO_PUBLICACION':[],'ISBN':[],'FECHA_ADQUISICION':[],'ID_GENERO':[],\
                                                                    'ID_AUTOR':[]})
                            print("Elija una opcion para obtener todos los datos del Autor: ")
                            AUTOR=str(input()).upper()
                            datos_titulo=DATA.loc[DATA["AUTOR"].isin([AUTOR])]
                            print(datos_titulo)
                            print(("*")*40)
                            print(("*")*40)
                            print("****      Reporte por autor      ****")
                            opcion2_2_2=int(input("[1]Exportar reporte en formato CSV\n[2]Exportar reporte en formato MsExcel\n[3]No exportar nada\n Elija una opcion:"))
                            if opcion2_2_2==1:
                                datos_titulo.to_csv('Reporte_por_autor.csv', index=False)
                                print('El archivo csv se nombro Reporte_por_autor.csv')
                                continue
                            if opcion2_2_2==1:
                                datos_titulo.to_excel('Reporte_por_autor.xlsx', index=False)
                                print('El archivo xlsx se nombro Reporte_por_autor.xlsx')
                                continue
                            if opcion2_2_2==1:
                                break

                    if opcion2_2==3:
                        while True:
                            conn=sqlite3.connect('biblioteca.db')
                            mi_cursor=conn.cursor()
                            mi_cursor.execute("SELECT BIBLIOTECA.ID,BIBLIOTECA.ID_GENERO,BIBLIOTECA.GENERO FROM BIBLIOTECA JOIN GENERO ON GENERO.ID=BIBLIOTECA.ID_GENERO")
                            RECOPILACION=mi_cursor.fetchall()
                            DATA=pd.DataFrame(RECOPILACION,columns=['ID','ID_GENERO','GENERO'])
                            print("*"*40)
                            print(DATA)
                            print("*"*40)
                            GENERO=input("Elija una opcion para obtener todos los datos del genero: ").upper()
                            conn=sqlite3.connect('biblioteca.db')
                            mi_cursor=conn.cursor()
                            consulta="SELECT*FROM BIBLOTECA WHERE GENERO = ?"
                            RECOPILACION=mi_cursor.fetchall()
                            DATA=pd.DataFrame(RECOPILACION,columns=['ID','TITULO','AUTOR','GENERO','ANIO_PUBLICACION','ISBN','FECHA_ADQUISICION','ID_GENERO','ID_AUTOR'])
                            print(DATA)
                            print(("*")*40)
                            print("****      Reporte por genero      ****")
                            opcion2_2_3=int(input("[1]Exportar reporte en formato CSV\n[2]Exportar reporte en formato MsExcel\n[3]No exportar nada\n Elija una opcion:"))
                            if opcion2_2_3==1:
                                DATA.to_csv('Reporte_por_genero.csv', index=False)
                                print('El archivo csv se nombro Reporte_por_genero.csv')
                                continue
                            if opcion2_2_3==2:
                                DATA.to_excel('Reporte_por_genero.xlsx', index=False)
                                print('El archivo xlsx se nombro Reporte_por_genero.xlsx')
                                continue
                            if opcion2_2_3==3:
                                break

                    if opcion2_2==4:
                        while True:
                            conn=sqlite3.connect('biblioteca.db')
                            mi_cursor=conn.cursor()
                            mi_cursor.execute("SELECT ID,ANIO_PUBLICACION FROM BIBLIOTECA")
                            RECOPILACION=mi_cursor.fetchall()
                            DATA=pd.DataFrame(RECOPILACION,columns=['ID','ANIO_PUBLICACION'])
                            print("*"*40)
                            print(DATA)
                            print("*"*40)
                            conn=sqlite3.connect('biblioteca.db')
                            print("Elija una opcion para obtener todos los datos del año de publicacion: ")
                            ANIO_PUBLICACION=int(input())
                            mi_cursor=conn.cursor()
                            consulta="SELECT*FROM BIBLIOTECA WHERE ANIO_PUBLICACION = ?"
                            mi_cursor.execute(consulta,(ANIO_PUBLICACION))
                            RECOPILACION=mi_cursor.fetchall()
                            DATA=pd.DataFrame(RECOPILACION,columns=['ID','TITULO','AUTOR','GENERO','ANIO_PUBLICACION','ISBN','FECHA_ADQUISICION','ID_GENERO','ID_AUTOR'])
                            print(DATA)
                            print(("*")*40)
                            print("****      Reporte por año en especifico      ****")
                            opcion2_2_4=int(input("[1]Exportar reporte en formato CSV\n[2]Exportar reporte en formato MsExcel\n[3]No exportar nada\n Elija una opcion:"))
                            if opcion2_2_4==1:
                                DATA.to_csv('Reporte_anio_publicacion.csv', index=False)
                                print('El archivo csv se nombro Reporte_anio_publicacion.csv')
                                continue
                            if opcion2_2_4==2:
                                DATA.to_excel('Reporte_anio_publicacion.xlsx', index=False)
                                print('El archivo xlsx se nombro Reporte_anio_publicacion.xlsx')
                                continue
                            if opcion2_2_4==3:
                                break
                    if opcion2_2==5:
                        break

                continue

            if opcion_2==3:
                break

        continue

    if opcion==3:
        print("*"*40)
        print("****  REGISTRAR AUTOR  ****")
        print("Ingrese apellidos: ")
        APELLIDOS=str(input().upper())
        print("Ingrese nombres: ")
        NOMBRES=str(input().upper())
        print("*"*40)
        ID=max(autor_id_existentes['ID'],default=0)+1
        autor_id['ID']=[ID]
        autor_id['APELLIDOS']=[APELLIDOS]
        autor_id['NOMBRES']=[NOMBRES]
        try:
            with sqlite3.connect("biblioteca.db") as conn:
                mi_cursor = conn.cursor()
                valores={"ID":ID,"APELLIDOS":APELLIDOS,"NOMBRES":NOMBRES}
                mi_cursor.execute("INSERT INTO AUTOR VALUES(:ID,:APELLIDOS,:NOMBRES)",valores)
                print("Registro agregado exitosamente")
                autor_id_existentes=pd.DataFrame(autor_id)
                autor_id_existentes.to_csv('autor_id.csv')
        except Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()

        continue

    if opcion==4:
        genero_id_existentes=pd.read_csv('genero_id.csv')
        print("*"*40)
        print("****  REGISTRAR GÉNERO  ****")
        print("Ingrese un genero: ")
        ID=max(genero_id_existentes['ID'],default=0)+1
        NOM_GENERO=input().upper()
        genero_id['ID']=[ID]
        genero_id['NOM_GENERO']=[NOM_GENERO]
        try:
            with sqlite3.connect("biblioteca.db") as conn:
                mi_cursor = conn.cursor()
                valores={"ID":ID,"NOM_GENERO":NOM_GENERO}
                mi_cursor.execute("INSERT INTO GENERO VALUES(:ID,:NOM_GENERO)",valores)
                print("Registro agregado exitosamente")
                genero_id_existentes=pd.DataFrame(genero_id)
                genero_id_existentes.to_csv('genero_id.csv')
        except Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()

        continue

    if opcion==5:
        biblioteca_existente.to_csv('biblioteca.csv')
        genero_id_existentes.to_csv('genero_id.csv')
        autor_id_existentes.to_csv('autor_id.csv')
        conn.close()
        break