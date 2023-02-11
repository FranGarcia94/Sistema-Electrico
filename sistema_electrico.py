#============================= Sistema Eléctrico =============================#
#                                                                             #
#             GUI para obteenr datos del sistema eléctrico Español            #
#                                                                             #
#                                                             @FranGarcia94   #
#=============================================================================#


from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import requests
import json
import datetime
import time
import matplotlib.pyplot as plt
from dateutil import parser, relativedelta


def mainframe_fun(cont: int):

    global main_frame, mimg, mbg_image, mbg_label

    main_frame = Frame(root, width = 1000, height = aside_height, bg = 'green', highlightthickness = 5, highlightbackground = 'darkblue')
    main_frame.grid(row = 1, column = 1, columnspan = 3)
    main_frame.grid_propagate(0)

    if cont == 0:

        mimg = Image.open(".\images\lba.png")
    elif cont == 1:

        mimg = Image.open(".\images\clear.png")
    elif cont == 2:

        mimg = Image.open(".\images\lbb.png")
    elif cont == 3:

        mimg = Image.open(".\images\abs.png")
    elif cont == 4:

        mimg = Image.open(".\images\lbb.png")

    mimg = mimg.resize((1000, aside_height), Image.Resampling.LANCZOS)
    mbg_image =  ImageTk.PhotoImage(mimg)

    mbg_label = Label(main_frame, image = mbg_image)
    mbg_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)


def pvpc1_fun(n: int):
    
    root_2 = Tk()
    root_2.geometry('300x150+450+200')
    root_2.overrideredirect('True')
    root_2.wm_attributes('-topmost', True)

    bg_gray = '#345'
    root_2.config(bg = bg_gray)


    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_date3 = datetime.datetime.now().strftime('%m-%d')
    
    eje_x = []
    pvpc = []
    pvpc_hour = []

    loading_lb = Label(master = root_2, text = "Loading...", fg ="white", bg = bg_gray, width = 12, height = 2, font = ('Terminal 20 bold'))
    loading_lb.pack(padx = 20, pady = 20)
    
    pb = ttk.Progressbar(root_2, orient = 'horizontal', length = 200, mode = 'determinate')
    pb.pack(padx = 10, pady = 10)
    
    pb['value'] = 100/n

    root_2.update()

    cont_loading = 1

    for i in range(n):
        
        current_date = datetime.datetime.now() - datetime.timedelta(days = i)
        current_date = current_date.strftime('%Y-%m-%d')

        current_date3 = datetime.datetime.now() - datetime.timedelta(days = i)
        current_date3 = current_date3.strftime('%d/%m')
        
        eje_x.append(current_date3)

        url = f'https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real?start_date={current_date}T00:00&end_date={current_date}T23:59&time_trunc=hour&geo_limit=peninsular'

        # Request
        response = requests.get(url)
        data = json.loads(response.text)
        
        
        if cont_loading == 0:

            loading_lb.configure(text = 'Loading...')
            cont_loading += 1
        elif cont_loading == 1:

            loading_lb.configure(text = 'Loading')
            cont_loading += 1
        elif cont_loading == 2:

            loading_lb.configure(text = 'Loading.')
            cont_loading += 1
        elif cont_loading == 3:

            loading_lb.configure(text = 'Loading..')
            cont_loading = 0


        pb['value'] += 100/n

        root_2.update()

        for i in range(24):
            
            pvpc.append(data['included'][0]['attributes']['values'][i]['value'])
            pvpc_hour.append(data['included'][0]['attributes']['values'][i]['datetime'])

    root_2.destroy()
       

    current_date3 = datetime.datetime.now() - datetime.timedelta(days=n)
    current_date3 = current_date3.strftime('%d/%m')
    eje_x.append(current_date3)


    if n != 1:

        x3 = range(0, len(pvpc) + 1, 24)
    else:

        x3 = range(0, 24)
        eje_x = [pvpc_hour[i][11:13] for i, _ in enumerate(pvpc_hour)]

    x = [i for i in range(len(pvpc))]

    matplotlib.use("TkAgg")

    fig = plt.figure(figsize = (9.9, 5.2), dpi = 100)
    plt.subplots_adjust(top = 0.95, left = 0.1, right = 0.95)

    max_time = parser.parse(pvpc_hour[pvpc.index(max(pvpc))]).strftime('%d/%m/%Y - %H:%M')
    min_time = parser.parse(pvpc_hour[pvpc.index(min(pvpc))]).strftime('%d/%m/%Y - %H:%M')
    
    plt.text(-n*1.2, max(pvpc) + 5, 'Max', fontsize = 10, bbox={'facecolor':'red', 'pad':0, 'alpha':0.25})
    plt.text(-n*1.2, min(pvpc) + 5, 'Min', fontsize = 10, bbox={'facecolor':'red', 'pad':0, 'alpha':0.25})
    plt.text(-n*1.2, sum(pvpc)/len(pvpc) + 5, 'Mean', fontsize = 10, bbox={'facecolor':'red', 'pad':0, 'alpha':0.25})

    plt.bar(x, pvpc, align = 'center', color = 'darkblue')
    plt.xticks(x3, eje_x, rotation = -45)
    plt.axhline(y = max(pvpc), color = 'black', linestyle = ':', label = f'Max: {max(pvpc)} €/MWh - {max_time}')
    plt.axhline(y = min(pvpc), color = 'darkorange', linestyle = ':', label = f'Min: {min(pvpc)} €/MWh - {min_time}')
    plt.axhline(y = sum(pvpc)/len(pvpc), color = 'magenta', linestyle = '--', label = f'Mean: {round(sum(pvpc)/len(pvpc),2)} €/MWh')
    
    plt.ylabel('€/MWh')

    if n == 1:

        title_date = datetime.datetime.now().strftime('%d-%m-%Y')
    else:

        title_date = f'last {n} days'

    plt.title(f'PVPC ({title_date})')
    plt.legend(loc = 'best', framealpha = 0.8, shadow = True, fontsize = 8)
    
    plt.close(fig)

    main_frame.destroy()
    mainframe_fun(1)

    canvas = FigureCanvasTkAgg(fig, main_frame)
    canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 1, rowspan = 2)

    toolbar_frame = Frame(main_frame)
    toolbar_frame.grid(row = 2, column = 0, columnspan = 1)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)

    root_2.mainloop()
    

def co2_fun():
    
    countries = {'España' : 'ES'}

    def co2_calcul(countries):

        root_2 = Tk()
        root_2.geometry('300x200+450+200')
        root_2.overrideredirect('True')
        root_2.wm_attributes('-topmost', True)

        bg_gray = '#345'
        root_2.config(bg = bg_gray)

        loading_lb = Label(master = root_2, text = "Loading...", fg = "white", bg = bg_gray, width = 12, height = 2, font = ('Terminal 20 bold'))
        loading_lb.pack(padx = 20, pady = 20)
        
        pb = ttk.Progressbar(root_2, orient = 'horizontal', length = 200, mode = 'determinate')
        pb.pack(padx = 10, pady = 10)
        
        pb['value'] = 100/len(countries)

        country_loading_lb = Label(root_2, text = '', bg = bg_gray, fg = 'darkorange', font = ('Terminal 16 bold'))
        country_loading_lb.pack(padx = 10, pady = 5)

        root_2.update()

        cont_loading = 1

        carbon_intensity = []
        fossil_fuel_percentage = []
        countries_keys = []
        countries_values = []

        for clave, valor in countries.items():

            try:

                url = f'https://api.co2signal.com/v1/latest?countryCode={countries[clave]}&auth-token=KEY-TOKEN-HERE'


                # Request
                response = requests.get(url)
                data_json = json.loads(response.text)

                print(data_json)

                carbon_intensity.append(data_json['data']['carbonIntensity'])
                fossil_fuel_percentage.append(round(data_json['data']['fossilFuelPercentage'], 2))
                carbon_units = data_json['units']['carbonIntensity']
                last_update_co2 = data_json['data']['datetime']

                countries_keys.append(clave)
                countries_values.append(valor)

                if cont_loading == 0:

                    loading_lb.configure(text = 'Loading...')
                    cont_loading += 1
                elif cont_loading == 1:

                    loading_lb.configure(text = 'Loading')
                    cont_loading += 1
                elif cont_loading == 2:

                    loading_lb.configure(text = 'Loading.')
                    cont_loading += 1
                elif cont_loading ==3:

                    loading_lb.configure(text = 'Loading..')
                    cont_loading = 0


                pb['value'] += 100/len(countries)

                country_loading_lb['text'] = f'{clave} : {valor}'

                root_2.update()

                data_json = ''

                time.sleep(1)
            except:

                pass

        root_2.destroy()

        try:

            matplotlib.use("TkAgg")

            fig = plt.figure(figsize = (7, 5), dpi=100)
            
            plt.bar(countries_values, carbon_intensity, color ='darkblue', width = 0.4)

            for i, v in enumerate(carbon_intensity):

                plt.text(i-.1, v + .75 , str(v), color = 'darkorange', fontweight = 'bold')

            current_date = datetime.datetime.now().strftime('%a, %d-%m-%Y')
            
            plt.xlabel(f'Last Update: {current_date}; {last_update_co2[11:16]}')
            plt.xticks(rotation = -25)
            plt.ylabel(carbon_units)
            plt.title("CO2 Emissions")

            plt.close(fig)

            main_frame.destroy()
            mainframe_fun(2)

            canvas = FigureCanvasTkAgg(fig, main_frame)
            canvas.get_tk_widget().grid(row = 0, column = 0, rowspan = 3)

            toolbar_frame = Frame(main_frame, bg = 'red')
            toolbar_frame.grid(row = 3, column = 0)
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        except:

            print('Error')

        datils_lbf = LabelFrame(main_frame, text = 'Country names', bg = 'black', foreground = 'white', font = ('Calibri 16 bold'))
        datils_lbf.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'ne')

        all_countries_url = 'https://api.electricitymap.org/v3/zones'
        response_all = requests.get(all_countries_url)
        data_all = json.loads(response_all.text)

        data_values = list(data_all.values())

        all_countries = sorted([v['zoneName'] for v in data_values])
        all_countries_keys = []


        for i in all_countries:

            for j in data_all:

                if data_all[j]['zoneName'] == i:

                    all_countries_keys.append(j)
                    break

        
        countries_list = ttk.Combobox(datils_lbf, values = all_countries, width = 22, font = ('Arial 12 bold'))
        countries_list.pack(fill = 'both', expand = 1, padx = 10, pady = 5)
        countries_list.bind("<<ComboboxSelected>>", lambda e: print(dict({countries_list.get() : all_countries_keys[all_countries.index(countries_list.get())]})))

        query_country_btn = Button(datils_lbf, text = 'Enviar', bg = 'white', activebackground = 'green', activeforeground = 'black', width = 11, font = ('Rockwell 12 bold'), command = lambda: co2_calcul(dict({countries_list.get() : all_countries_keys[all_countries.index(countries_list.get())]})))
        query_country_btn.pack(padx = 15, pady = 5)
        query_country_btn.bind('<Enter>', lambda e: query_country_btn.config(bg = 'lightgreen', cursor = 'hand2', width = 18))
        query_country_btn.bind('<Leave>', lambda e: query_country_btn.config(bg = 'white', width = 11))

        europe_lb = Label(datils_lbf, text = 'Grupos', foreground = 'white', font = ('Arial 12 bold'), bg = 'limegreen')
        europe_lb.pack(fill = 'both', expand = 1, padx = 10, pady = 5)

        # Crear grupos aquí
        europe_btn = Button(datils_lbf, text = 'Europa', bg = 'white', activebackground = 'green', activeforeground = 'black', width = 11, font = ('Rockwell 12 bold'), command = lambda: co2_calcul({'España' : 'ES', 'Portugal' : 'PT', 'Francia' : 'FR', 'Bélgica' : 'BE', 'Italia' : 'IT', 'Alemania' : 'DE', 'Austria' : 'AT', 'Chequia' : 'CZ', 'Eslovaquia' : 'SK', 'Polonia' : 'PL', 'Ucrania': 'UA', 'Hungría' : 'HU', 'Estonia' : 'EE', 'Letonia' : 'LV', 'Lituania': 'LT', 'Rumanía': 'RO', 'Finlandia' : 'FI', 'Gran Bretaña' : 'GB', 'Dinamarca' : 'DK', 'Grecia' : 'GR', 'Croacia' : 'HR', 'Albania': 'AL', 'Montenegro': 'ME','Países Bajos' : 'NL', 'Suecia' : 'SE', 'Noruega' : 'NO'}))
        europe_btn.pack(padx = 5, pady = 5)
        europe_btn.bind('<Enter>', lambda e: europe_btn.config(bg = 'lightgreen', cursor = 'hand2', width = 18))
        europe_btn.bind('<Leave>', lambda e: europe_btn.config(bg = 'white', width = 11))


        def info_co2():

            root_infoco2 = Tk()
            root_infoco2.title('Información')
            root_infoco2.iconbitmap('.\images\flash_2.ico')
            root_infoco2.config(padx = 30, pady = 30, bg = 'white')
            
            lb_ico2 = Label(root_infoco2, text = 'Intensidad de CO2 debido a la generación eléctrica', justify = 'center', font = ('Arial 12 bold'), fg = 'limegreen', bg = 'white')
            lb_ico2.grid(row = 0, column = 0, columnspan = 3, sticky = 'ns',  pady = 20)

            lb2_ico2 = Label(root_infoco2, text = 'En este apartado se pueden consultar las emisiones de CO2 procedentes de la generación eléctrica'
                ' por cada país.\n\nSe puede elegir cada país individualmente o comparar un grupo de países desde el apartado de grupos '
                'pulsando\ndirectamente en el botón del grupo.\n\nEs posible que uno o varios países no tengan datos disponibles, '
                'ya sea de manera puntual o por un tiempo \nindeterminado, en ese caso, esos valores se omitirán en la gráfica.\n',
                justify = 'left', font = ('Arial 10 bold'), bg = 'white')
            lb2_ico2.grid(row = 1, column = 1, sticky = 'w')

            lb_ico2 = Label(root_infoco2, text='Datos obtenidos de la API de:', justify = 'right', font = ('Arial 8 bold'), bg = 'white')
            lb_ico2.grid(row = 2, column = 0, columnspan = 2, sticky = 'e')
            lb_ico3 = Label(root_infoco2, text = 'https://app.electricitymaps.com/map', justify = 'left', font = ('Arial 8 bold'), fg = 'blue', bg = 'white')
            lb_ico3.grid(row = 2, column = 2, sticky = 'w')

            root_infoco2.mainloop()


        info_lbf = LabelFrame(main_frame, bg = 'black', foreground = 'white')
        info_lbf.grid(row = 3, column = 1, sticky = 'se')

        info_btn = Button(info_lbf, text = 'Info', command = info_co2, padx = 2, pady = 2)
        info_btn.pack(padx = 5, pady = 5)
        info_btn.bind('<Enter>', lambda e: info_btn.config(bg = 'darkblue', fg = 'white', cursor = 'hand2'))
        info_btn.bind('<Leave>', lambda e: info_btn.config(bg = 'white', fg = 'black'))


    co2_calcul(countries)


def pot_instalada():

    current_date = datetime.datetime.now()
    current_date = current_date.strftime('%Y-%m-%d')

    start_date = datetime.datetime.now() - relativedelta.relativedelta(years = 5)
    start_date = start_date.strftime('%Y-%m-%d')
    url = f'https://apidatos.ree.es/es/datos/generacion/potencia-instalada?start_date={start_date}T23:59&end_date={current_date}T00:00&time_trunc=year'

    response = requests.get(url)
    data = json.loads(response.text)


    def autolabel(rectangle_group):

        for rect in rectangle_group:

            height = rect.get_height()


    names = [v['type'] for _,v in enumerate(data['included'])]
    names.pop()
    a18 = [vv['attributes']['values'][0]['value']/1000 for _, vv in enumerate(data['included'])]
    a18.pop()
    a19 = [vv['attributes']['values'][1]['value']/1000 for _, vv in enumerate(data['included'])]
    a19.pop()
    a20 = [vv['attributes']['values'][2]['value']/1000 for _, vv in enumerate(data['included'])]
    a20.pop()
    a21 = [vv['attributes']['values'][3]['value']/1000 for _, vv in enumerate(data['included'])]
    a21.pop()
    a22 = [vv['attributes']['values'][4]['value']/1000 for _, vv in enumerate(data['included'])]
    a22.pop()


    aux_plt = []
    for i,_ in enumerate(a18):

        aux_plt.append(i)

    width = 0.15
    x_18 = [x - width*2 for x in range(len(a18))]
    x_19 = [x - width for x in range(len(a19))]
    x_20 = [x for x in range(len(a20))]
    x_21 = [x + width for x in range(len(a21))]
    x_22 = [x + width*2 for x in range(len(a22))]

    matplotlib.use("TkAgg")
    
    fig,ax = plt.subplots()
    fig.set_size_inches(9.9,5.2)
    plt.subplots_adjust(top = 0.95, left = 0.07, right = 0.98, bottom = 0.38)
    
    rect1 = ax.bar(x_18, a18,width,label = data['included'][0]['attributes']['values'][0]['datetime'][0:4],color = '#1D1E1C')
    rect2 = ax.bar(x_19,a19,width, label = data['included'][0]['attributes']['values'][1]['datetime'][0:4],color = '#4A503C')
    rect3 = ax.bar(x_20,a20,width, label = data['included'][0]['attributes']['values'][2]['datetime'][0:4],color = '#7B8E49')
    rect4 = ax.bar(x_21,a21,width, label = data['included'][0]['attributes']['values'][3]['datetime'][0:4],color = '#9DC33B')
    rect5 = ax.bar(x_22,a22,width, label = data['included'][0]['attributes']['values'][4]['datetime'][0:4],color = '#B6F905')

    ax.set_title('Potencia Instalada')
    ax.set_ylabel('MW')
    
    plt.xticks(aux_plt,names)
    plt.xticks(rotation = - 90)
    ax.legend()

    autolabel(rect1)
    autolabel(rect2)
    autolabel(rect3)
    autolabel(rect4)
    autolabel(rect5)

    plt.close(fig)

    main_frame.destroy()
    mainframe_fun(3)

    canvas = FigureCanvasTkAgg(fig, main_frame)
    canvas.get_tk_widget().grid(row = 1, column = 0, columnspan = 2)

    toolbar_frame = Frame(main_frame)
    toolbar_frame.grid(row = 2, column = 0, columnspan = 2)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)


def estructura_generacion():

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    start_date = datetime.datetime.now() - relativedelta.relativedelta(years = 5)
    start_date = start_date.strftime('%Y-%m-%d')

    url = f'https://apidatos.ree.es/es/datos/generacion/estructura-generacion?start_date={start_date}T23:59&end_date={current_date}T00:00&time_trunc=year'

    response = requests.get(url)
    data = json.loads(response.text)

    def autolabel(rectangle_group):

        for rect in rectangle_group:

            height = rect.get_height()


    names = [v['type'] for _,v in enumerate(data['included'])]
    names.pop()
    a18 = [vv['attributes']['values'][0]['value']/1000 for _, vv in enumerate(data['included'])]
    a18.pop()
    a19 = [vv['attributes']['values'][1]['value']/1000 for _, vv in enumerate(data['included'])]
    a19.pop()
    a20 = [vv['attributes']['values'][2]['value']/1000 for _, vv in enumerate(data['included'])]
    a20.pop()
    a21 = [vv['attributes']['values'][3]['value']/1000 for _, vv in enumerate(data['included'])]
    a21.pop()

    a22 = []
    for _,v in enumerate(data['included']):

        try:

            a22.append(v['attributes']['values'][4]['value']/1000)
        except:

            a22.append(0)

    a22.pop()

    pot_mean = []
    aux_plt = []
    for i,_ in enumerate(a18):

        pot_mean.append(str(i))
        aux_plt.append(i)

    matplotlib.use("TkAgg")

    width = 0.15
    x_18 = [x - width*2 for x in range(len(a18))]
    x_19 = [x - width for x in range(len(a19))]
    x_20 = [x for x in range(len(a20))]
    x_21 = [x + width for x in range(len(a21))]
    x_22 = [x + width*2 for x in range(len(a22))]

    fig,ax = plt.subplots()
    fig.set_size_inches(9.9,5.2)
    plt.subplots_adjust(top = 0.95, left = 0.08, right = 0.98, bottom = 0.38)

    rect1 = ax.bar(x_18, a18, width, label = '2018', color = '#c299ff')
    rect2 = ax.bar(x_19, a19, width, label = '2019', color = '#8533ff')
    rect3 = ax.bar(x_20, a20, width, label = '2020', color = '#5200cc')
    rect4 = ax.bar(x_21, a21, width, label = '2021', color = '#25035c')
    rect5 = ax.bar(x_22, a22, width, label = '2022', color = '#0a001a')

    ax.set_title('Estructura de Generación')
    ax.set_ylabel('MWh')

    plt.xticks(aux_plt,names)
    plt.xticks(rotation = - 90)
    ax.legend()

    autolabel(rect1)
    autolabel(rect2)
    autolabel(rect3)
    autolabel(rect4)
    autolabel(rect5)

    plt.close(fig)

    main_frame.destroy()
    mainframe_fun(3)

    canvas = FigureCanvasTkAgg(fig, main_frame)
    canvas.get_tk_widget().grid(row = 1, column = 0, columnspan = 2)

    toolbar_frame = Frame(main_frame)
    toolbar_frame.grid(row = 2, column = 0, columnspan = 2)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)


def demanda():

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    url = f'https://apidatos.ree.es/en/datos/demanda/demanda-tiempo-real?start_date={current_date}T00:00&end_date={current_date}T23:59&time_trunc=hour&geo_trunc=electric_system&geo_limit=peninsular&geo_ids=8741'

    response = requests.get(url)
    data = json.loads(response.text)

    x_prog=[]
    y_prog=[]
    x_fore=[]
    y_fore=[]
    x_axis=[]
    x_real = []
    y_real = []

    for j in range(0,3):

        for i in data['included'][j]['attributes']['values']:

            if j == 0:

                x_real.append(i['datetime'][11:16])
                y_real.append(i['value'])
            elif j == 1:

                x_prog.append(i['datetime'][11:16])
                y_prog.append(i['value'])  
            elif j==2:

                x_fore.append(i['datetime'][11:16])
                y_fore.append(i['value'])
            
    x_axis = [v['datetime'][11:13] for _, v in enumerate(data['included'][1]['attributes']['values'])]
    x_cont = []

    for i, v in enumerate(x_axis):

        if v in x_cont:

            x_axis[i]=''
        else:

            x_cont.append(v)

    matplotlib.use("TkAgg")

    fig, ax = plt.subplots()
    fig.set_size_inches(9.9,5.2)
    plt.subplots_adjust(left = 0.09, right = 0.96)

    ax.plot(x_prog, y_prog, label = "Programada", color = 'crimson')
    ax.plot(x_fore, y_fore, label = "Prevista", color = 'orange')
    ax.plot(x_real, y_real, label = "Real", color = 'blue')

    ax.legend(loc = 2)

    title_date = datetime.datetime.now().strftime('%d-%m-%Y')
    ax.set_title (f'Demanda {title_date}')

    plt.xticks(x_fore, x_axis)
    plt.xticks(rotation = - 90)

    plt.ylabel("kWh")

    plt.grid(axis = 'y')

    plt.close(fig)

    main_frame.destroy()
    mainframe_fun(1)

    canvas = FigureCanvasTkAgg(fig, main_frame)
    canvas.get_tk_widget().grid(row = 1, column = 0)

    toolbar_frame = Frame(main_frame)
    toolbar_frame.grid(row = 2, column = 0)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)


def intercambios():

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    start_date = datetime.datetime.now() - relativedelta.relativedelta(years = 5)
    start_date = start_date.strftime('%Y-%m-%d')

    url = f'https://apidatos.ree.es/es/datos/intercambios/todas-fronteras-fisicos?start_date={start_date}T23:59&end_date={current_date}T00:00&time_trunc=year'


    response = requests.get(url)
    data = json.loads(response.text)

    aux = [round(int(v['attributes']['content'][2]['attributes']['values'][j]['value'])/1000, 2) for j in range(5) for _, v in enumerate(data['included'])]
    
    aux2 = aux

    def autolabel(rectangle_group):

        for rect in rectangle_group:

            height = rect.get_height()


    names = ['Francia', 'Portugal', 'Marruecos', 'Andorra']
    a18 = aux2[0:4]
    a19 = aux2[4:8]
    a20 = aux2[8:12]
    a21 = aux2[12:16]
    a22 = aux2[16:20]

    pot_mean = []
    aux_plt = []

    for i,_ in enumerate(a18):

        pot_mean.append(str(i))
        aux_plt.append(i)

    matplotlib.use("TkAgg")  

    width = 0.15
    x_18 = [x - width*2 for x in range(len(a18))]
    x_19 = [x - width for x in range(len(a19))]
    x_20 = [x for x in range(len(a20))]
    x_21 = [x + width for x in range(len(a21))]
    x_22 = [x + width*2 for x in range(len(a22))]

    fig,ax = plt.subplots()
    fig.set_size_inches(9.9,5.2)
    plt.subplots_adjust(top = 0.95, left = 0.09, right = 0.98)

    rect1 = ax.bar(x_18, a18, width, label = '2018',color = '#1D1E1C')
    rect2 = ax.bar(x_19, a19, width, label = '2019',color = '#4A503C')
    rect3 = ax.bar(x_20, a20, width, label = '2020',color = '#7B8E49')
    rect4 = ax.bar(x_21, a21, width, label = '2021',color = '#9DC33B')
    rect5 = ax.bar(x_22, a22, width, label = '2022',color = '#B6F905')

    ax.set_title('Intercambios')
    ax.set_ylabel('GWh')

    ax.set_xticks(aux_plt)
    ax.set_xticklabels(names)

    plt.grid(1, axis = 'y')
    ax.legend()

    autolabel(rect1)
    autolabel(rect2)
    autolabel(rect3)
    autolabel(rect4)
    autolabel(rect5)

    plt.close(fig)

    main_frame.destroy()
    mainframe_fun(3)

    canvas = FigureCanvasTkAgg(fig, main_frame)
    canvas.get_tk_widget().grid(row = 1, column = 0, columnspan = 2)

    toolbar_frame = Frame(main_frame)
    toolbar_frame.grid(row = 2, column = 0, columnspan = 2)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)




# ! =======================================================MAIN=================================================================== ! #
if __name__ == '__main__':

    root = Tk()
    root.title('Sistema Eléctrico Español')
    root.iconbitmap('.\images\flash_2.ico')
    root.config(bg = 'red')

    # ? HEADER SECTION

    head_width = 1150
    head_height = 100

    head_frame = Frame(root, width = head_width, height = head_height)
    head_frame.grid(row = 0, column = 0, columnspan = 2)

    img = Image.open(".\images\head.png")
    img = img.resize((head_width, head_height), Image.Resampling.LANCZOS)
    bg_image =  ImageTk.PhotoImage(img)

    bg_label = Label(head_frame, image = bg_image)
    bg_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    head_label = Label(head_frame, text = 'Bienvenido', bg = 'white', font = ('Rockwell 18 bold'))
    head_label.place(x = 535, y = 10)


    ############################################################################################################################################


    # ? ASIDE SECTION 

    def bind_fun(bind_btn):

        def enter_fun(e):

                bind_btn.config(bg = 'lightgreen')

        def leave_fun(e):

                bind_btn.config(bg = 'white')
                
        bind_btn.bind('<Enter>', enter_fun)
        bind_btn.bind('<Leave>', leave_fun)

    def btn_style(btn_list: list):

        for i in btn_list:

            i.config(cursor = 'hand2', bg = 'white', activebackground = 'green', activeforeground = 'black', width = 11, font = ('Rockwell 12 bold'))
            bind_fun(i)


    aside_width = 150
    aside_height = 575

    aside_frame = Frame(root, bg = '#1d2d2e', highlightthickness = 5, highlightbackground = 'darkblue')
    aside_frame.grid(row = 1, column = 0)
    aside_frame.config(width = aside_width, height = aside_height)
    aside_frame.grid_propagate(0)

    menu_label = Label(aside_frame, text = 'MENU', bg = '#1d2d2e', fg = 'white', font = ('Rockwell 20 bold'))
    menu_label.grid(row = 0, column = 0, padx = 10, pady = 20)

    pvpc_frame = LabelFrame(aside_frame, bg = '#070245')
    pvpc_frame.grid(row = 2, column = 0)


    pvpc1_btn = Button(pvpc_frame, text = 'PVPC 1', command = lambda: pvpc1_fun(1))
    pvpc1_btn.grid(row = 0, column = 0, padx = 5, pady = 10)

    pvpc7_btn = Button(pvpc_frame, text='PVPC 7', command = lambda: pvpc1_fun(7))
    pvpc7_btn.grid(row = 1, column = 0, padx = 5, pady = 0)

    pvpc30_btn = Button(pvpc_frame, text = 'PVPC 30', command = lambda: pvpc1_fun(30))
    pvpc30_btn.grid(row = 2, column = 0, padx = 5, pady = 10)

    live_frame = LabelFrame(aside_frame, bg = '#070245')
    live_frame.grid(row = 3, column = 0, pady = 20)

    demanda_real_btn = Button(live_frame, text = 'Demanda', command = demanda)
    demanda_real_btn.grid(row = 0, column = 0, padx = 5, pady = 5)

    co2_btn = Button(live_frame, text = 'CO2', command = co2_fun)
    co2_btn.grid(row = 1, column = 0, padx = 5, pady = 5)

    sistema_frame = LabelFrame(aside_frame, bg = '#070245')
    sistema_frame.grid(row = 4, column = 0, padx = 3, pady = 5)

    pot_btn = Button(sistema_frame, text = 'Pot. Instalada', command = pot_instalada)
    pot_btn.grid(row=0, column=0, padx = 5, pady = 10)

    est_gen_btn = Button(sistema_frame, text = 'Estruct. Gen', command = estructura_generacion)
    est_gen_btn.grid(row = 1, column = 0, padx = 5)

    intercambios_btn = Button(sistema_frame, text = 'Intercambios', command = intercambios)
    intercambios_btn.grid(row = 2, column = 0, padx = 5, pady = 10)

    btn_list = [pvpc1_btn, pvpc7_btn, pvpc30_btn, demanda_real_btn, co2_btn, pot_btn, est_gen_btn, intercambios_btn]

    btn_style(btn_list)
    ############################################################################################################################################

    # ? MAIN SECTION 
    
    mainframe_fun(0)

    root.mainloop()