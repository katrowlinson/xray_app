from flask import Blueprint, render_template, request, url_for, make_response
from xray_app.main.forms import Xraylib_Request_Plot
from xray_app.methods.utils import calc_output, all_trans

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO
import base64

import xraylib

from xray_app.methods.routes import cs_dict, trans_S_tup, trans_I_tup, make_tup, validate_int, validate_float

def delete_key(key, _dict):
    if key in _dict:
        del _dict[key]
        
#remove unimplemented functions from possible input
delete_key('CS_KN', cs_dict)
delete_key('CS_Total_Kissel', cs_dict)
delete_key('CS_Photo_Partial', cs_dict)
cs_tup = make_tup(cs_dict, 'cs')

main = Blueprint('main', __name__)

@main.route("/about")
def about():
    return render_template('about.html', title = 'About ')

@main.route("/plot", methods=['GET', 'POST'])
def plot():
    form = Xraylib_Request_Plot()
    form.function.choices = form.function.choices + cs_tup #not all of these are needed delete as necessary
    form.linetype.trans_iupac.choices = trans_I_tup
    form.linetype.trans_siegbahn.choices = trans_S_tup
    
    if request.method == 'POST':        
        #for key in request.form.keys():
        #print(f'key= {key}')
                
        select_input = request.form.get('function')
        range_start = request.form['range_start']
        range_end = request.form['range_end']
        log_boo_x = request.form.get('log_boo_x')
        log_boo_y = request.form.get('log_boo_y')
        
        int_z = request.form['int_z']
        int_z_or_comp = request.form['int_z_or_comp']
        
        linetype_trans_notation = request.form.get('linetype-trans_notation')        
        trans_iupac = request.form.get('linetype-trans_iupac')
        trans_siegbahn = request.form.get('linetype-trans_siegbahn')
        
        if select_input == 'CS_Total' or select_input == 'CS_Photo' or select_input == 'CS_Rayl' or select_input == 'CS_Energy' or select_input == 'CS_Compt':
            #need validation of requests
            plot = make_plot(select_input, 'Energy ($keV$)', r'Cross Section ($cm^{2} g^{-1}$)', range_start, range_end, log_boo_x, log_boo_y, int_z_or_comp)
            return render_template('plot.html', form = form, title = 'Plot', plot=plot)
    
        elif select_input.startswith('CS_FluorLine'):
            if linetype_trans_notation == 'IUPAC':
                plot = make_plot(select_input, 'Energy ($keV$)', r'Cross Section ($cm^{2} g^{-1}$)', range_start, range_end, log_boo_x, log_boo_y, int_z, trans_iupac)
                return render_template('plot.html', form = form, title = 'Plot', plot=plot)
            elif linetype_trans_notation == 'Siegbahn':
                plot = make_plot(select_input, 'Energy ($keV$)', r'Cross Section ($cm^{2} g^{-1}$)', range_start, range_end, log_boo_x, log_boo_y, int_z, trans_siegbahn)
                return render_template('plot.html', form = form, title = 'Plot', plot=plot)          

    return render_template('plot.html', title = 'Plot', form = form)
#-------------------------------------------------------------------------------------
def make_plot(function, xlabel, ylabel, range_start, range_end, log_boo_x, log_boo_y, *variables):
    x = []
    y = []
    t_variables = [] 

    print(variables)
    if validate_float(range_start, range_end):
        for i in range(int(range_start), int(range_end), 1):            
            #print(calc_output(function, *variables, i))
            y.append(float(calc_output(function, *variables, i)))
            x.append(i)        
    else:
        print('invalid range')
        pass

    fig = Figure()
    canvas = FigureCanvas(fig)
            
    fig, ax = plt.subplots()
    ax.plot(x, y)
    
    for variable in variables:
        if validate_int(variable) == True:
            t_variables.append(xraylib.AtomicNumberToSymbol(int(variable)))
        else:
            t_variables.append(str(variable))
    
    t_variables = ', '.join(t_variables)
    ax.set(title = function + ': ' + t_variables, xlabel = xlabel, ylabel = ylabel)            
    
    if validate_int(variable) == True:
        ax.set(title = function + ': ' + xraylib.AtomicNumberToSymbol(int(variable)))
    if log_boo_y != None and log_boo_x != None:
        plt.xscale('log')
        plt.yscale('log')        
        ax.set(xlabel = 'log[ ' + xlabel + ' ]', ylabel = 'log[ ' + ylabel + ' ]')                    
    elif log_boo_x != None:
        plt.xscale('log')
        ax.set(xlabel = 'log[ ' + xlabel + ' ]', ylabel = ylabel)
    elif log_boo_y != None:
        plt.yscale('log')        
        ax.set(ylabel = 'log[ ' + ylabel + ' ]')
                       
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img_bytes = img.getvalue()
    img.close()
    img64 = str(base64.b64encode(img_bytes), encoding='utf-8')
    return img64 
