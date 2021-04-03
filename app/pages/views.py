from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import ast
from time import time
from datetime import datetime, timedelta
from django.db.models import Sum

max_ts_diff = 5

def dashboard(request):
    args = {
        'current': '-',
        'tot_enery': '-',
        'set_voltage': '-',
        'pwr': '-'
    }

    last_log = EnergyLog.objects.order_by('-pk')[0]
    last_ts = last_log.ts
    current_ts = int(time())
    diff = current_ts - last_ts
    if diff <= max_ts_diff:
        args['current'] = last_log.current
        args['tot_enery'] = last_log.tot_enery
        args['set_voltage'] = last_log.set_voltage
        args['pwr'] = last_log.pwr
    
    print('diff: ', diff)
    print('args: ', args)
    print(last_log.ts)
    return render(request, 'pages/dashboard.html', args)

def log(request, d=''):
    print(d)
    if(d == 'd={}'):
        logs = EnergyLog.objects.all().order_by('-pk')[0:100]
        start = str(logs[len(logs)-1].date.strftime('%m-%d-%Y')).split(' ')[0]
        end = str(logs[0].date.strftime('%m-%d-%Y')).split(' ')[0]
    else: 
        data = ast.literal_eval(d)
        start = datetime.strptime(data['start_timestamp'], '%m-%d-%Y')
        end = datetime.strptime(data['end_timestamp'], '%m-%d-%Y')
        print('........')
        print('end: ', end)
        end += timedelta(days=1)
        print('incrimented: ', end)
        print('........')
        print('start : ', start)
        print('end: ', end)
        logs = EnergyLog.objects.filter(date__gte=start, date__lte=end)
        
        start = str(start.strftime('%m-%d-%Y')).split(' ')[0]
        end += timedelta(days=-1)
        end = str(end.strftime('%m-%d-%Y')).split(' ')[0]
        

    
    try:
        tot_energy_consumed = logs.aggregate(Sum('pwr'))['pwr__sum']/(1000.0*3600)
    except:
        tot_energy_consumed = 0.0

    if tot_energy_consumed > 1:
        tot_energy_consumed = round(tot_energy_consumed, 2)
    else:
        tot_energy_consumed = round(tot_energy_consumed, 6)
    args = {
        'logs': logs,
        'start': start,
        'end': end,
        'tot_energy_consumed': tot_energy_consumed
    }
    return render(request, 'pages/log.html', args)

def log_data(request, d):
    data = ast.literal_eval(d)
    # d={"current": current_rms, 'set_voltage': voltage, 'tot_energy': total_energy, 'pwr': power}
    new_log = EnergyLog()
    new_log.current = data['current']
    new_log.set_voltage = data['set_voltage']
    new_log.tot_enery = data['tot_energy']
    new_log.pwr = data['pwr']
    new_log.ts = time()
    new_log.save()
    for i in data:
        print(i, data[i])
    return JsonResponse({})


def lattest_data(request):
    args = {
        'current': '',
        'tot_enery': '',
        'set_voltage': '',
        'pwr': ''
    }

    last_log = EnergyLog.objects.order_by('-pk')[0]
    last_ts = last_log.ts
    current_ts = int(time())
    diff = current_ts - last_ts
    if diff <= max_ts_diff:
        args['current'] = str(last_log.current) + ' A'
        args['tot_enery'] = str(round(last_log.tot_enery, 2)) + ' kWh'
        args['set_voltage'] = str(last_log.set_voltage) + ' V'
        args['pwr'] = str(round(last_log.pwr, 2)) + ' W'

    return JsonResponse(args)
